import test from "node:test";
import assert from "node:assert/strict";
import { createHmac } from "node:crypto";
import { verifyTelegramInitData } from "../lib/telegram.js";
import { createSession, verifySession } from "../lib/session.js";

const BOT_TOKEN = "test-bot-token";
const NOW = 1800000000;

function makeInitData(user, authDate = NOW) {
  const params = new URLSearchParams();
  params.set("auth_date", String(authDate));
  params.set("query_id", "AAE-test");
  params.set("user", JSON.stringify(user));
  const check = Array.from(params.entries())
    .sort(([a], [b]) => a.localeCompare(b))
    .map(([key, value]) => key + "=" + value).join("\n");
  const secret = createHmac("sha256", "WebAppData").update(BOT_TOKEN).digest();
  params.set("hash", createHmac("sha256", secret).update(check).digest("hex"));
  return params.toString();
}

test("accepts valid Telegram initData", () => {
  const result = verifyTelegramInitData(
    makeInitData({ id: 123456, first_name: "PaidMX", username: "paidmx_user" }),
    BOT_TOKEN,
    NOW
  );
  assert.equal(result.id, "123456");
  assert.equal(result.firstName, "PaidMX");
  assert.equal(result.username, "paidmx_user");
});

test("rejects tampered Telegram initData", () => {
  const input = makeInitData({ id: 123456, first_name: "PaidMX" });
  const changed = input.replace("PaidMX", "PaidMY");
  assert.throws(() => verifyTelegramInitData(changed, BOT_TOKEN, NOW), /signature|hash/i);
});

test("rejects expired Telegram initData", () => {
  const stale = makeInitData({ id: 123456, first_name: "User" }, NOW - 90000);
  assert.throws(() => verifyTelegramInitData(stale, BOT_TOKEN, NOW), /expired/i);
});

test("validates signed session expiry and signature", () => {
  const secret = "this-is-a-sufficiently-long-test-session-secret";
  const session = createSession("123456", secret, NOW);
  assert.equal(verifySession(session.token, secret, NOW).userId, "123456");
  assert.equal(verifySession(session.token, secret, NOW + session.maxAge + 1), null);
  assert.equal(verifySession(session.token + "bad", secret, NOW), null);
});
