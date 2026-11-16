"use strict";

const crypto = require("node:crypto");
const MAX_INIT_DATA_AGE_SECONDS = 60 * 60;

function verifyTelegramInitData(initData, botToken, nowSeconds = Math.floor(Date.now() / 1000)) {
  if (typeof initData !== "string" || !initData || initData.length > 8192) throw new Error("telegram_auth_required");
  if (typeof botToken !== "string" || !botToken) throw new Error("telegram_auth_config_missing");
  const params = new URLSearchParams(initData);
  const receivedHash = params.get("hash");
  const authDate = Number(params.get("auth_date"));
  if (!receivedHash || !/^[a-f0-9]{64}$/i.test(receivedHash) || !Number.isInteger(authDate)) throw new Error("telegram_auth_invalid");
  if (authDate > nowSeconds + 60 || nowSeconds - authDate > MAX_INIT_DATA_AGE_SECONDS) throw new Error("telegram_auth_expired");
  params.delete("hash");
  const dataCheckString = [...params.entries()].sort(([a], [b]) => a.localeCompare(b)).map(([k, v]) => k + "=" + v).join("\n");
  const secretKey = crypto.createHmac("sha256", "WebAppData").update(botToken).digest();
  const calculated = crypto.createHmac("sha256", secretKey).update(dataCheckString).digest("hex");
  const a = Buffer.from(calculated, "hex");
  const b = Buffer.from(receivedHash, "hex");
  if (a.length !== b.length || !crypto.timingSafeEqual(a, b)) throw new Error("telegram_auth_invalid");
  const rawUser = params.get("user");
  if (!rawUser) throw new Error("telegram_user_missing");
  let user;
  try { user = JSON.parse(rawUser); } catch { throw new Error("telegram_user_invalid"); }
  if (!user || !Number.isSafeInteger(Number(user.id)) || Number(user.id) <= 0) throw new Error("telegram_user_invalid");
  return { ...user, id: String(user.id), authDate, startParam: String(params.get("start_param") || "").slice(0, 64) };
}
module.exports = { verifyTelegramInitData, MAX_INIT_DATA_AGE_SECONDS };
