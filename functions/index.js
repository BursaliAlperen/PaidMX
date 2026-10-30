const { onRequest } = require("firebase-functions/v2/https");
const { defineSecret } = require("firebase-functions/params");
const { initializeApp } = require("firebase-admin/app");
const { getFirestore, FieldValue } = require("firebase-admin/firestore");
const crypto = require("node:crypto");

initializeApp();
const db = getFirestore();
const BOT_TOKEN = defineSecret("BOT_TOKEN");

const MAX_INIT_DATA_AGE_SECONDS = 24 * 60 * 60;
const ADMIN_IDS = new Set(["7904032877"]);

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
  { region: "us-central1", secrets: [BOT_TOKEN], maxInstances: 20, timeoutSeconds: 30 },
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
    if (origin && !allowedOrigin(origin)) return send(res, 403, { ok: false, error: "origin_not_allowed" });

    try {
      const initData = req.get("X-Telegram-Init-Data") || req.body?.initData;
      const telegramUser = verifyTelegramInitData(initData, BOT_TOKEN.value());
      const rpc = String(req.body?.rpc || "");
      const payload = req.body?.payload && typeof req.body.payload === "object" ? req.body.payload : {};

      // Create/update the Telegram identity only after cryptographic initData validation.
      const userRef = db.collection("users").doc(telegramUser.id);
      await db.runTransaction(async tx => {
        const snap = await tx.get(userRef);
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
