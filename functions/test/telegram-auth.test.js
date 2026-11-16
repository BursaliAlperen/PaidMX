"use strict";

const test = require("node:test");
const assert = require("node:assert/strict");
const crypto = require("node:crypto");
const { verifyTelegramInitData } = require("../lib/telegram-auth");
const token = "123456:unit-test-token";
const now = 1800000000;

function signedInitData(authDate = now, user = { id: 42, first_name: "Test" }) {
  const values = new URLSearchParams({ auth_date: String(authDate), query_id: "AAE-test", user: JSON.stringify(user) });
  const check = [...values.entries()].sort(([a], [b]) => a.localeCompare(b)).map(([k, v]) => k + "=" + v).join("\n");
  const secret = crypto.createHmac("sha256", "WebAppData").update(token).digest();
  values.set("hash", crypto.createHmac("sha256", secret).update(check).digest("hex"));
  return values.toString();
}

test("accepts valid Telegram initData and normalizes user ID", () => {
  const user = verifyTelegramInitData(signedInitData(), token, now);
  assert.equal(user.id, "42");
  assert.equal(user.first_name, "Test");
});
test("rejects modified initData", () => {
  const values = new URLSearchParams(signedInitData());
  values.set("query_id", "tampered");
  assert.throws(() => verifyTelegramInitData(values.toString(), token, now), { message: "telegram_auth_invalid" });
});
test("rejects expired and future-dated initData", () => {
  assert.throws(() => verifyTelegramInitData(signedInitData(now - 3601), token, now), { message: "telegram_auth_expired" });
  assert.throws(() => verifyTelegramInitData(signedInitData(now + 61), token, now), { message: "telegram_auth_expired" });
});
test("rejects invalid user identity and empty initData", () => {
  assert.throws(() => verifyTelegramInitData(signedInitData(now, {}), token, now), { message: "telegram_user_invalid" });
  assert.throws(() => verifyTelegramInitData("", token, now), { message: "telegram_auth_required" });
});
test("rejects missing bot token", () => {
  assert.throws(() => verifyTelegramInitData(signedInitData(), "", now), { message: "telegram_auth_config_missing" });
});
