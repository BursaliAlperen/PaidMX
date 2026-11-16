const { onRequest } = require("firebase-functions/v2/https");
const { defineSecret } = require("firebase-functions/params");
const { initializeApp } = require("firebase-admin/app");
const { getFirestore, FieldValue } = require("firebase-admin/firestore");
const crypto = require("node:crypto");
const { parseRewardMicros, verifyOfferwallSignature } = require("./lib/offerwall-security");
const { verifyTelegramInitData } = require("./lib/telegram-auth");
const { isClaimAllowed, secondsUntilClaim } = require("./lib/faucet");

initializeApp();
const db = getFirestore();
const BOT_TOKEN = defineSecret("BOT_TOKEN");
const OFFERWALLAPI_SECRET = defineSecret("OFFERWALLAPI_SECRET");
const OFFERWALLAPI_KEY = defineSecret("OFFERWALLAPI_KEY");
const OFFERWALLAPI_BEARER = defineSecret("OFFERWALLAPI_BEARER");

const ADMIN_IDS = new Set((process.env.ADMIN_IDS || "").split(",").map(v => v.trim()).filter(Boolean));

// Server-side faucet economy. Values are configurable via environment variables;
// the defaults below are documented in README_FIREBASE.md and reported in the
// faucet RPC so the frontend never hardcodes them.
function intEnv(name, def) {
  const v = Number(process.env[name]);
  return Number.isFinite(v) && v > 0 ? v : def;
}
const FAUCET_REWARD_MICROS = intEnv("FAUCET_REWARD_MICROS", 100000);   // 0.1 PMX
const FAUCET_COOLDOWN_SECONDS = intEnv("FAUCET_COOLDOWN_SECONDS", 3600); // 60 min

const DAY_MS = 24 * 60 * 60 * 1000;
const ACTIVE_WINDOW_MS = 7 * DAY_MS;

function nowSeconds() {
  return Math.floor(Date.now() / 1000);
}

function txEntry(userId, type, amountMicros, meta = {}) {
  return {
    userId,
    type,
    amountMicros: Number(amountMicros) || 0,
    title: String(meta.title || "").slice(0, 160),
    refId: String(meta.refId || "").slice(0, 200),
    createdAt: FieldValue.serverTimestamp()
  };
}

function offerwallFields(req) {
  if (req.body && typeof req.body === "object" && !Buffer.isBuffer(req.body)) {
    return req.body;
  }
  if (typeof req.body === "string") return Object.fromEntries(new URLSearchParams(req.body));
  if (req.rawBody) return Object.fromEntries(new URLSearchParams(req.rawBody.toString("utf8")));
  return {};
}

async function handleOfferwallApiPostback(req, res) {
  const p = offerwallFields(req);
  const subId = String(p.subId || "");
  const transId = String(p.transId || "");
  const reward = String(p.reward || "");
  const status = String(p.status || "");
  const signature2 = String(p.signature2 || "");
  const signature = String(p.signature || "");
  const secret = OFFERWALLAPI_SECRET.value();

  if (!/^\d{1,20}$/.test(subId) || !transId || transId.length > 200 ||
      !["1", "2"].includes(status)) {
    return send(res, 400, { ok: false, error: "invalid_postback" });
  }

  if (!verifyOfferwallSignature({
    subId, transId, reward, signature2, signature, secret
  })) {
    return send(res, 403, { ok: false, error: "invalid_signature" });
  }

  // Provider test callbacks must never create user earnings.
  if (String(p.debug || "0") === "1" || transId.startsWith("test-")) {
    return res.status(200).type("text/plain").send("ok");
  }

  let rewardMicros;
  try {
    rewardMicros = parseRewardMicros(reward);
  } catch {
    return send(res, 400, { ok: false, error: "invalid_reward" });
  }

  const txKey = crypto.createHash("sha256").update("offerwallapi:" + transId).digest("hex");
  const eventRef = db.collection("providerTransactions").doc(txKey);
  const walletRef = db.collection("wallets").doc(subId);
  const statsRef = db.collection("stats").doc("app");
  const transactionsCol = db.collection("transactions");

  try {
    await db.runTransaction(async tx => {
      const eventSnap = await tx.get(eventRef);
      if (eventSnap.exists) {
        const existing = eventSnap.data();
        if (existing.userId !== subId || Number(existing.rewardMicros) !== rewardMicros) {
          throw new Error("transaction_identity_conflict");
        }
        if (existing.state === "reversed" || existing.state === "reversed_before_credit") return;
        if (status === "1") return; // Duplicate credit delivery.
        if (status !== "2" || existing.state !== "credited") {
          throw new Error("transaction_state_conflict");
        }

        const walletSnap = await tx.get(walletRef);
        if (!walletSnap.exists) throw new Error("user_wallet_not_found");
        const wallet = walletSnap.data();
        const balance = Number(wallet.balanceMicros || 0);
        const debt = Number(wallet.debtMicros || 0);
        if (!Number.isSafeInteger(balance) || !Number.isSafeInteger(debt) || balance < 0 || debt < 0) {
          throw new Error("wallet_state_invalid");
        }
        const debit = Math.min(balance, Number(existing.rewardMicros));
        const debtAdded = Number(existing.rewardMicros) - debit;
        if (!Number.isSafeInteger(debt + debtAdded)) throw new Error("wallet_overflow");
        tx.set(walletRef, {
          balanceMicros: balance - debit,
          debtMicros: debt + debtAdded,
          currency: "PMX",
          updatedAt: FieldValue.serverTimestamp()
        }, { merge: true });
        tx.update(eventRef, {
          state: "reversed", status: 2, debitedMicros: debit,
          debtAddedMicros: debtAdded, reversedAt: FieldValue.serverTimestamp()
        });
        if (debit > 0) {
          tx.create(transactionsCol.doc(), txEntry(subId, "chargeback", -debit, { title: "Offerwall chargeback", refId: transId }));
          tx.set(statsRef, { totalChargebacksMicros: FieldValue.increment(debit) }, { merge: true });
        }
        return;
      }

      // A reversal can arrive before its original credit. Record it so a delayed
      // original callback cannot create spendable funds later.
      if (status === "2") {
        tx.create(eventRef, {
          provider: "offerwallapi", transId, userId: subId, rewardMicros,
          status: 2, state: "reversed_before_credit",
          createdAt: FieldValue.serverTimestamp()
        });
        return;
      }

      const walletSnap = await tx.get(walletRef);
      if (!walletSnap.exists) throw new Error("user_wallet_not_found");
      const wallet = walletSnap.data();
      const balance = Number(wallet.balanceMicros || 0);
      const debt = Number(wallet.debtMicros || 0);
      if (!Number.isSafeInteger(balance) || !Number.isSafeInteger(debt) || balance < 0 || debt < 0) {
        throw new Error("wallet_state_invalid");
      }

      const debtPaid = Math.min(debt, rewardMicros);
      const availableCredit = rewardMicros - debtPaid;
      if (!Number.isSafeInteger(balance + availableCredit)) throw new Error("wallet_overflow");
      tx.set(walletRef, {
        balanceMicros: balance + availableCredit,
        debtMicros: debt - debtPaid,
        currency: "PMX",
        updatedAt: FieldValue.serverTimestamp()
      }, { merge: true });
      tx.create(eventRef, {
        provider: "offerwallapi", transId, userId: subId, rewardMicros,
        creditedMicros: availableCredit, debtPaidMicros: debtPaid,
        status: 1, state: "credited", offerType: String(p.offer_type || "offer").slice(0, 32),
        offerName: String(p.offer_name || "").slice(0, 160),
        payoutUsd: String(p.payout || "").slice(0, 32),
        country: String(p.country || "").slice(0, 2),
        createdAt: FieldValue.serverTimestamp()
      });
      if (availableCredit > 0) {
        tx.create(transactionsCol.doc(), txEntry(subId, "task_reward", availableCredit, { title: p.offer_name || "Task reward", refId: transId }));
        tx.set(statsRef, {
          totalTaskRewardsMicros: FieldValue.increment(availableCredit)
        }, { merge: true });
      }
    });
    return res.status(200).type("text/plain").send("ok");
  } catch (err) {
    if (err.message === "user_wallet_not_found") {
      return send(res, 404, { ok: false, error: "user_not_found" });
    }
    console.error("OfferwallApi postback failed:", err.message);
    return send(res, 500, { ok: false, error: "postback_processing_failed" });
  }
}

function send(res, status, body) {
  res.status(status).set("Content-Type", "application/json").send(body);
}

function allowedOrigin(origin) {
  const configured = (process.env.CORS_ORIGINS || "")
    .split(",").map(v => v.trim()).filter(Boolean);
  return !!origin && configured.includes(origin);
}

async function fetchQuickTasks(userId, userIp) {
  const apiKey = OFFERWALLAPI_KEY.value();
  const bearer = OFFERWALLAPI_BEARER.value();
  if (!apiKey || !bearer) throw new Error("offerwall_credentials_missing");
  const ip = /^\d{1,3}(?:\.\d{1,3}){3}$/.test(userIp) ? userIp : "0.0.0.0";
  const feeds = [["ptc", "ptc-api"], ["video", "video-api"], ["shortlink", "sl-api"]];
  const results = await Promise.all(feeds.map(async ([type, endpoint]) => {
    const url = "https://offerwallapi.com/" + endpoint + "/" + encodeURIComponent(apiKey) + "/" + encodeURIComponent(userId) + "/" + ip;
    const response = await fetch(url, { headers: { Authorization: "Bearer " + bearer, Accept: "application/json" }, signal: AbortSignal.timeout(10000) });
    if (!response.ok) throw new Error("offerwall_feed_http_" + response.status);
    const body = await response.json();
    if (String(body.status) !== "200" || !Array.isArray(body.data)) return [];
    return body.data.map(item => ({ ...item, type }));
  }));
  const blocked = /install|download|deposit|make a purchase|purchase|register|sign.?up|trial|subscription|yükle|indir|yatır|satın al|kayıt ol/i;
  return results.flat().filter(item => {
    const text = String(item.title || "") + " " + String(item.description || "");
    const duration = Number(item.duration || 0);
    if (blocked.test(text) || !["ptc", "video", "shortlink"].includes(item.type)) return false;
    if (item.type !== "shortlink" && (!Number.isFinite(duration) || duration < 1 || duration > 180)) return false;
    try { const target = new URL(String(item.url || "")); return target.protocol === "https:" && target.hostname === "offerwallapi.com"; } catch { return false; }
  }).slice(0, 100);
}

function mapTask(item) {
  return {
    id: String(item.id || ""),
    type: item.type,
    title: String(item.title || "Short task"),
    description: String(item.description || ""),
    reward: String(item.reward || "0"),
    currency: String(item.currency_name || "PMX"),
    duration: Number(item.duration || 0),
    url: String(item.url || "")
  };
}

async function getDashboardData(telegramUser) {
  const userRef = db.collection("users").doc(telegramUser.id);
  const walletRef = db.collection("wallets").doc(telegramUser.id);
  const [profileSnap, walletSnap] = await Promise.all([userRef.get(), walletRef.get()]);
  const profile = profileSnap.data() || {};
  const wallet = walletSnap.data() || {};

  const todayStart = new Date();
  todayStart.setHours(0, 0, 0, 0);

  let todayEarningsMicros = 0;
  let todayTasksCompleted = 0;
  let recentActivity = [];
  try {
    const todaySnap = await db.collection("transactions")
      .where("userId", "==", telegramUser.id)
      .where("createdAt", ">=", todayStart)
      .orderBy("createdAt", "desc")
      .limit(200)
      .get();
    for (const doc of todaySnap.docs) {
      const t = doc.data();
      const amount = Number(t.amountMicros || 0);
      if (amount > 0) todayEarningsMicros += amount;
      if (t.type === "task_reward") todayTasksCompleted += 1;
    }
    const recentSnap = await db.collection("transactions")
      .where("userId", "==", telegramUser.id)
      .orderBy("createdAt", "desc")
      .limit(10)
      .get();
    recentActivity = recentSnap.docs.map(doc => {
      const t = doc.data();
      return {
        id: doc.id,
        type: String(t.type || "adjustment"),
        amountMicros: Number(t.amountMicros || 0),
        title: String(t.title || ""),
        refId: String(t.refId || ""),
        createdAt: t.createdAt ? t.createdAt.toMillis() : 0
      };
    });
  } catch (e) {
    // Transaction index may not exist yet; degrade gracefully.
    console.error("getDashboard transactions query failed:", e.message);
  }

  return {
    user: {
      id: telegramUser.id,
      firstName: String(profile.firstName || ""),
      username: String(profile.username || ""),
      photoUrl: String(profile.photoUrl || ""),
      referralCode: String(profile.referralCode || ""),
      referralCount: Number(profile.referralCount || 0),
      referralEarningsMicros: Number(profile.referralEarningsMicros || 0),
      totalEarnedMicros: Number(profile.totalEarnedMicros || 0),
      totalTasksCompleted: Number(profile.totalTasksCompleted || 0),
      lang: String(profile.lang || "tr"),
      createdAt: profile.createdAt ? profile.createdAt.toMillis() : 0
    },
    wallet: {
      balanceMicros: Number(wallet.balanceMicros || 0),
      debtMicros: Number(wallet.debtMicros || 0),
      currency: "PMX"
    },
    stats: {
      todayEarningsMicros,
      todayTasksCompleted,
      totalEarningsMicros: Number(profile.totalEarnedMicros || 0),
      totalTasksCompleted: Number(profile.totalTasksCompleted || 0),
      totalReferrals: Number(profile.referralCount || 0)
    },
    recentActivity,
    admin: ADMIN_IDS.has(telegramUser.id)
  };
}

async function handleClaimFaucet(telegramUser) {
  const walletRef = db.collection("wallets").doc(telegramUser.id);
  const faucetRef = db.collection("faucetClaims").doc(telegramUser.id);
  const statsRef = db.collection("stats").doc("app");
  const now = nowSeconds();
  const reward = FAUCET_REWARD_MICROS;

  let result;
  await db.runTransaction(async tx => {
    const walletSnap = await tx.get(walletRef);
    if (!walletSnap.exists) throw new Error("user_wallet_not_found");
    const wallet = walletSnap.data();
    const balance = Number(wallet.balanceMicros || 0);
    const debt = Number(wallet.debtMicros || 0);
    if (!Number.isSafeInteger(balance) || !Number.isSafeInteger(debt) || balance < 0 || debt < 0) {
      throw new Error("wallet_state_invalid");
    }

    const faucetSnap = await tx.get(faucetRef);
    const lastClaimAt = faucetSnap.exists ? Number(faucetSnap.data().lastClaimAt || 0) : 0;
    if (!isClaimAllowed(lastClaimAt, FAUCET_COOLDOWN_SECONDS, now)) {
      throw new Error("faucet_cooldown");
    }

    const debtPaid = Math.min(debt, reward);
    const availableCredit = reward - debtPaid;
    if (!Number.isSafeInteger(balance + availableCredit)) throw new Error("wallet_overflow");

    tx.set(walletRef, {
      balanceMicros: balance + availableCredit,
      debtMicros: debt - debtPaid,
      currency: "PMX",
      updatedAt: FieldValue.serverTimestamp()
    }, { merge: true });

    const prevClaims = faucetSnap.exists ? Number(faucetSnap.data().totalClaims || 0) : 0;
    const prevEarned = faucetSnap.exists ? Number(faucetSnap.data().totalEarnedMicros || 0) : 0;
    tx.set(faucetRef, {
      userId: telegramUser.id,
      lastClaimAt: now,
      totalClaims: prevClaims + 1,
      totalEarnedMicros: prevEarned + reward,
      updatedAt: FieldValue.serverTimestamp()
    }, { merge: true });

    tx.create(db.collection("transactions").doc(), txEntry(telegramUser.id, "faucet_claim", reward, { title: "Faucet claim" }));
    tx.set(statsRef, { totalFaucetRewardsMicros: FieldValue.increment(reward) }, { merge: true });

    result = { claimedMicros: reward, creditedMicros: availableCredit, debtPaidMicros: debtPaid };
  });

  return result;
}

async function getFaucetState(telegramUser) {
  const faucetRef = db.collection("faucetClaims").doc(telegramUser.id);
  const snap = await faucetRef.get();
  const data = snap.exists ? snap.data() : {};
  const lastClaimAt = Number(data.lastClaimAt || 0);
  const now = nowSeconds();
  return {
    rewardMicros: FAUCET_REWARD_MICROS,
    cooldownSeconds: FAUCET_COOLDOWN_SECONDS,
    lastClaimAt,
    nextClaimAt: lastClaimAt + FAUCET_COOLDOWN_SECONDS,
    canClaim: isClaimAllowed(lastClaimAt, FAUCET_COOLDOWN_SECONDS, now),
    secondsUntilClaim: secondsUntilClaim(lastClaimAt, FAUCET_COOLDOWN_SECONDS, now),
    totalClaims: Number(data.totalClaims || 0),
    totalEarnedMicros: Number(data.totalEarnedMicros || 0)
  };
}

exports.api = onRequest(
  { region: "us-central1", secrets: [BOT_TOKEN, OFFERWALLAPI_SECRET, OFFERWALLAPI_KEY, OFFERWALLAPI_BEARER], maxInstances: 20, timeoutSeconds: 30 },
  async (req, res) => {
    const origin = req.get("origin");
    if (origin && allowedOrigin(origin)) {
      res.set("Access-Control-Allow-Origin", origin);
      res.set("Vary", "Origin");
      res.set("Access-Control-Allow-Headers", "Content-Type, X-Telegram-Init-Data");
      res.set("Access-Control-Allow-Methods", "POST, OPTIONS");
    }
    if (req.method === "OPTIONS") return res.status(204).send("");
    if (req.method === "GET" && req.path === "/health") {
      return send(res, 200, { ok: true, service: "paidmx-api", project: "paidmx" });
    }
    if (req.method !== "POST") return send(res, 405, { ok: false, error: "method_not_allowed" });
    if (req.path === "/offerwallapi/postback") return handleOfferwallApiPostback(req, res);
    if (origin && !allowedOrigin(origin)) return send(res, 403, { ok: false, error: "origin_not_allowed" });

    try {
      const initData = req.get("X-Telegram-Init-Data") || req.body?.initData;
      const telegramUser = verifyTelegramInitData(initData, BOT_TOKEN.value());
      const body = req.body && typeof req.body === "object" ? req.body : {};
      const rpc = String(body.rpc || "").slice(0, 64);
      const payload = body.payload && typeof body.payload === "object" ? body.payload : {};

      // Create/update the Telegram identity only after cryptographic initData validation.
      const userRef = db.collection("users").doc(telegramUser.id);
      const walletRef = db.collection("wallets").doc(telegramUser.id);
      const generatedReferralCode = crypto.randomBytes(6).toString("hex");
      const referralMatch = /^ref_([A-Za-z0-9_-]{6,20})$/.exec(telegramUser.startParam || "");
      const incomingReferralCode = referralMatch ? referralMatch[1] : null;
      const statsRef = db.collection("stats").doc("app");

      await db.runTransaction(async tx => {
        const snap = await tx.get(userRef);
        const walletSnap = await tx.get(walletRef);
        if (snap.exists && snap.data().banned === true) throw new Error("user_banned");

        const existingProfile = snap.exists ? snap.data() : {};
        const referralCode = String(existingProfile.referralCode || generatedReferralCode);
        const ownCodeRef = db.collection("referralCodes").doc(referralCode);
        const ownCodeSnap = await tx.get(ownCodeRef);

        let incomingCodeSnap = null;
        let referrerSnap = null;
        let referrerRef = null;
        if (!snap.exists && incomingReferralCode) {
          const incomingCodeRef = db.collection("referralCodes").doc(incomingReferralCode);
          incomingCodeSnap = await tx.get(incomingCodeRef);
          if (incomingCodeSnap.exists) {
            const referrerId = String(incomingCodeSnap.data().userId || "");
            if (referrerId && referrerId !== telegramUser.id) {
              referrerRef = db.collection("users").doc(referrerId);
              referrerSnap = await tx.get(referrerRef);
            }
          }
        }

        if (ownCodeSnap.exists && String(ownCodeSnap.data().userId) !== telegramUser.id) {
          throw new Error("referral_code_conflict");
        }

        const safeProfile = {
          telegramId: telegramUser.id,
          firstName: String(telegramUser.first_name || "").slice(0, 128),
          username: String(telegramUser.username || "").slice(0, 64),
          photoUrl: String(telegramUser.photo_url || "").slice(0, 2048),
          referralCode,
          lastSeenAt: FieldValue.serverTimestamp(),
          updatedAt: FieldValue.serverTimestamp()
        };

        if (!snap.exists) {
          tx.create(userRef, {
            ...safeProfile, balanceGr: 0, playsTotal: 0, banned: false,
            referralCount: 0, referralEarningsMicros: 0,
            totalEarnedMicros: 0, totalTasksCompleted: 0,
            lang: "tr", createdAt: FieldValue.serverTimestamp()
          });
          tx.set(statsRef, { totalUsers: FieldValue.increment(1) }, { merge: true });
        } else {
          tx.set(userRef, safeProfile, { merge: true });
        }

        if (!ownCodeSnap.exists) {
          tx.create(ownCodeRef, {
            userId: telegramUser.id,
            createdAt: FieldValue.serverTimestamp()
          });
        }

        if (!snap.exists && incomingCodeSnap?.exists && referrerSnap?.exists &&
            referrerSnap.data().banned !== true) {
          const referralRef = db.collection("referrals").doc(telegramUser.id);
          tx.create(referralRef, {
            referredUserId: telegramUser.id,
            referrerId: String(incomingCodeSnap.data().userId),
            referralCode: incomingReferralCode,
            createdAt: FieldValue.serverTimestamp()
          });
          tx.set(referrerRef, {
            referralCount: FieldValue.increment(1),
            updatedAt: FieldValue.serverTimestamp()
          }, { merge: true });
          tx.set(statsRef, { totalReferrals: FieldValue.increment(1) }, { merge: true });
        }

        if (!walletSnap.exists) {
          tx.create(walletRef, {
            balanceMicros: 0, debtMicros: 0, currency: "PMX",
            createdAt: FieldValue.serverTimestamp(),
            updatedAt: FieldValue.serverTimestamp()
          });
        }
      });

      if (rpc === "getQuickTasks") {
        const forwarded = String(req.get("x-forwarded-for") || "").split(",")[0].trim();
        const remoteIp = String(req.ip || forwarded || "").replace(/^::ffff:/, "");
        const tasks = await fetchQuickTasks(telegramUser.id, remoteIp);
        return send(res, 200, { ok: true, tasks: tasks.map(mapTask) });
      }

      if (rpc === "authCheck" || rpc === "getDashboard") {
        return send(res, 200, { ok: true, ...(await getDashboardData(telegramUser)) });
      }

      if (rpc === "getFaucet") {
        return send(res, 200, { ok: true, faucet: await getFaucetState(telegramUser) });
      }

      if (rpc === "claimFaucet") {
        const { claimedMicros, creditedMicros, debtPaidMicros } = await handleClaimFaucet(telegramUser);
        return send(res, 200, {
          ok: true,
          claimedMicros, creditedMicros, debtPaidMicros,
          faucet: await getFaucetState(telegramUser)
        });
      }

      if (rpc === "getTransactions") {
        const limit = Math.min(Math.max(Number(payload.limit) || 50, 1), 100);
        const snap = await db.collection("transactions")
          .where("userId", "==", telegramUser.id)
          .orderBy("createdAt", "desc")
          .limit(limit)
          .get();
        const transactions = snap.docs.map(doc => {
          const t = doc.data();
          return {
            id: doc.id,
            type: String(t.type || "adjustment"),
            amountMicros: Number(t.amountMicros || 0),
            title: String(t.title || ""),
            refId: String(t.refId || ""),
            createdAt: t.createdAt ? t.createdAt.toMillis() : 0
          };
        });
        return send(res, 200, { ok: true, transactions });
      }

      if (rpc === "getReferrals") {
        const snap = await db.collection("referrals")
          .where("referrerId", "==", telegramUser.id)
          .orderBy("createdAt", "desc")
          .limit(100)
          .get();
        const referrals = await Promise.all(snap.docs.map(async doc => {
          const data = doc.data();
          const refUserSnap = await db.collection("users").doc(String(data.referredUserId || "")).get();
          const refUser = refUserSnap.exists ? refUserSnap.data() : {};
          return {
            referredUserId: String(data.referredUserId || ""),
            firstName: String(refUser.firstName || ""),
            username: String(refUser.username || ""),
            createdAt: data.createdAt ? data.createdAt.toMillis() : 0
          };
        }));
        return send(res, 200, { ok: true, referrals });
      }

      if (rpc === "setPreferences") {
        const lang = String(payload.lang || "").slice(0, 8);
        if (!["tr", "en"].includes(lang)) return send(res, 400, { ok: false, error: "invalid_lang" });
        await userRef.set({ lang }, { merge: true });
        return send(res, 200, { ok: true });
      }

      if (rpc === "adminStats") {
        if (!ADMIN_IDS.has(telegramUser.id)) return send(res, 403, { ok: false, error: "forbidden" });
        const statsSnap = await db.collection("stats").doc("app").get();
        const stats = statsSnap.exists ? statsSnap.data() : {};
        const activeSince = new Date(Date.now() - ACTIVE_WINDOW_MS);
        const [activeUsersSnap, providerCountSnap, recentProviderSnap] = await Promise.all([
          db.collection("users").where("lastSeenAt", ">", activeSince).count().get(),
          db.collection("providerTransactions").count().get(),
          db.collection("providerTransactions").where("createdAt", ">", activeSince).count().get()
        ]);
        return send(res, 200, {
          ok: true,
          stats: {
            totalUsers: Number(stats.totalUsers || 0),
            activeUsers7d: activeUsersSnap.data().count,
            totalTaskRewardsMicros: Number(stats.totalTaskRewardsMicros || 0),
            totalFaucetRewardsMicros: Number(stats.totalFaucetRewardsMicros || 0),
            totalReferrals: Number(stats.totalReferrals || 0),
            totalChargebacksMicros: Number(stats.totalChargebacksMicros || 0),
            providerEvents: providerCountSnap.data().count,
            providerEvents7d: recentProviderSnap.data().count,
            faucetRewardMicros: FAUCET_REWARD_MICROS,
            faucetCooldownSeconds: FAUCET_COOLDOWN_SECONDS
          }
        });
      }

      // Remaining legacy RPCs are deliberately not stubbed with fake success.
      return send(res, 501, { ok: false, error: "rpc_not_migrated", rpc });
    } catch (err) {
      const code = String(err?.message || "internal_error");
      const status = code.startsWith("telegram_") ? 401 : code === "user_banned" ? 403 : code === "faucet_cooldown" ? 409 : code === "forbidden" ? 403 : 500;
      console.error("PaidMX API error:", code);
      return send(res, status, { ok: false, error: code });
    }
  }
);
