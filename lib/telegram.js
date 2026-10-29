import { createHmac, timingSafeEqual } from "node:crypto";

const MAX_AGE_SECONDS = 86400;

export function verifyTelegramInitData(initData, botToken, nowSeconds = Math.floor(Date.now() / 1000)) {
  if (typeof initData !== "string" || !initData || typeof botToken !== "string" || !botToken) {
    throw new Error("Missing Telegram initData or bot token");
  }
  const params = new URLSearchParams(initData);
  const receivedHash = params.get("hash");
  if (!receivedHash || !/^[a-f0-9]{64}$/i.test(receivedHash)) throw new Error("Invalid initData hash");

  const entries = Array.from(params.entries()).filter(([key]) => key !== "hash");
  entries.sort(([a], [b]) => a.localeCompare(b));
  const checkString = entries.map(([key, value]) => key + "=" + value).join("\n");
  const secret = createHmac("sha256", "WebAppData").update(botToken).digest();
  const calculated = createHmac("sha256", secret).update(checkString).digest();
  const received = Buffer.from(receivedHash, "hex");
  if (received.length !== calculated.length || !timingSafeEqual(received, calculated)) {
    throw new Error("Telegram initData signature check failed");
  }

  const authDate = Number(params.get("auth_date"));
  if (!Number.isInteger(authDate) || authDate > nowSeconds + 30 || nowSeconds - authDate > MAX_AGE_SECONDS) {
    throw new Error("Telegram initData is expired");
  }
  let user;
  try { user = JSON.parse(params.get("user") || "null"); }
  catch { throw new Error("Invalid Telegram user payload"); }
  if (!user || !Number.isSafeInteger(Number(user.id)) || Number(user.id) <= 0) throw new Error("Invalid Telegram user ID");
  return {
    id: String(user.id),
    username: typeof user.username === "string" ? user.username.slice(0, 64) : null,
    firstName: typeof user.first_name === "string" ? user.first_name.slice(0, 128) : ""
  };
}
