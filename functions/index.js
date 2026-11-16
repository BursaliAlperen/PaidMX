const { onRequest } = require("firebase-functions/v2/https");
const { defineSecret } = require("firebase-functions/params");
const { initializeApp } = require("firebase-admin/app");
const { getFirestore, FieldValue } = require("firebase-admin/firestore");
const crypto = require("node:crypto");

initializeApp();
const db = getFirestore();
const BOT_TOKEN = defineSecret("BOT_TOKEN");
const OFFERWALLAPI_SECRET = defineSecret("OFFERWALLAPI_SECRET");

const MAX_INIT_DATA_AGE_SECONDS = 24 * 60 * 60;
const ADMIN_IDS = new Set((process.env.ADMIN_IDS || "7904032877").split(",").map(v => v.trim()).filter(Boolean));

function constantTimeHexEqual(expected, supplied) {
  if (typeof supplied !== "string" || !/^[a-f0-9]+$/i.test(supplied)) return false;
  const left = Buffer.from(expected, "hex");
  const right = Buffer.from(supplied, "hex");
  return left.length === right.length && crypto.timingSafeEqual(left, right);
}

function parseRewardMicros(value) {
  const raw = String(value ?? "");
  if (!/^(?:0|[1-9]\d{0,11})(?:\.\d{1,6})?$/.test(raw)) {
    throw new Error("invalid_reward");
  }
  const [whole, fraction = ""] = raw.split(".");
  const micros = BigInt(whole) * 1000000n + BigInt((fraction + "000000").slice(0, 6));
  if (micros <= 0n || micros > BigInt(Number.MAX_SAFE_INTEGER)) {
    throw new Error("invalid_reward");
  }
  return Number(micros);
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

  const signed = subId + transId + reward;
  const validHmac = constantTimeHexEqual(
    crypto.createHmac("sha256", secret).update(signed).digest("hex"),
    signature2
  );
  const validLegacy = constantTimeHexEqual(
    crypto.createHash("md5").update(signed + secret).digest("hex"),
    signature
  );
  if (!validHmac && !validLegacy) {
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

function verifyTelegramInitData(initData, botToken) {
  if (typeof initData !== "string" || !initData || initData.length > 8192) {
    throw new Error("telegram_auth_required");
  }
  const params = new URLSearchParams(initData);
  const receivedHash = params.get("hash");
  const authDate = Number(params.get("auth_date"));
  if (!receivedHash || !Number.isInteger(authDate)) throw new Error("telegram_auth_invalid");
  const now = Math.floor(Date.now() / 1000);
  if (authDate > now + 60 || now - authDate > MAX_INIT_DATA_AGE_SECONDS) {
    throw new Error("telegram_auth_expired");
  }
  params.delete("hash");
  const dataCheckString = [...params.entries()]
    .sort(([a], [b]) => a.localeCompare(b))
    .map(([k, v]) => `${k}=${v}`).join("\n");
  const secretKey = crypto.createHmac("sha256", "WebAppData").update(botToken).digest();
  const calculated = crypto.createHmac("sha256", secretKey).update(dataCheckString).digest("hex");
  const a = Buffer.from(calculated, "hex");
  const b = Buffer.from(receivedHash, "hex");
  if (a.length !== b.length || !crypto.timingSafeEqual(a, b)) {
    throw new Error("telegram_auth_invalid");
  }
  const rawUser = params.get("user");
  if (!rawUser) throw new Error("telegram_user_missing");
  const user = JSON.parse(rawUser);
  if (!user || !Number.isSafeInteger(Number(user.id))) throw new Error("telegram_user_invalid");
  return { ...user, id: String(user.id), authDate };
}

exports.api = onRequest(
  { region: "us-central1", secrets: [BOT_TOKEN, OFFERWALLAPI_SECRET], maxInstances: 20, timeoutSeconds: 30 },
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
      const rpc = String(req.body?.rpc || "");
      const payload = req.body?.payload && typeof req.body.payload === "object" ? req.body.payload : {};

      // Create/update the Telegram identity only after cryptographic initData validation.
      const userRef = db.collection("users").doc(telegramUser.id);
      const walletRef = db.collection("wallets").doc(telegramUser.id);
      await db.runTransaction(async tx => {
        const snap = await tx.get(userRef);
        const walletSnap = await tx.get(walletRef);
        const safeProfile = {
          telegramId: telegramUser.id,
          firstName: String(telegramUser.first_name || "").slice(0, 128),
          username: String(telegramUser.username || "").slice(0, 64),
          photoUrl: String(telegramUser.photo_url || "").slice(0, 2048),
          lastSeenAt: FieldValue.serverTimestamp(),
          updatedAt: FieldValue.serverTimestamp()
        };
        if (!snap.exists) {
          tx.create(userRef, {
            ...safeProfile, balanceGr: 0, playsTotal: 0, banned: false,
            lang: "tr", createdAt: FieldValue.serverTimestamp()
          });
        } else {
          tx.set(userRef, safeProfile, { merge: true });
        }
        if (!walletSnap.exists) {
          tx.create(walletRef, {
            balanceMicros: 0, debtMicros: 0, currency: "PMX",
            createdAt: FieldValue.serverTimestamp(),
            updatedAt: FieldValue.serverTimestamp()
          });
        }
      });

      if (rpc === "authCheck") {
        return send(res, 200, { ok: true, user: { id: telegramUser.id }, admin: ADMIN_IDS.has(telegramUser.id) });
      }

      // Remaining legacy RPCs are deliberately not stubbed with fake success.
      // Implement each action against Firestore transactions before switching the live frontend.
      return send(res, 501, { ok: false, error: "rpc_not_migrated", rpc });
    } catch (err) {
      const code = String(err?.message || "internal_error");
      const status = code.startsWith("telegram_") ? 401 : 500;
      console.error("PaidMX API error:", code);
      return send(res, status, { ok: false, error: status === 401 ? code : "internal_error" });
    }
  }
);
