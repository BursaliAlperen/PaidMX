"use strict";

const test = require("node:test");
const assert = require("node:assert/strict");
const crypto = require("node:crypto");
const { parseRewardMicros, verifyOfferwallSignature } = require("../lib/offerwall-security");

test("converts decimal PMX rewards to integer micros without floating point", () => {
  assert.equal(parseRewardMicros("1"), 1000000);
  assert.equal(parseRewardMicros("0.000001"), 1);
  assert.equal(parseRewardMicros("12.340005"), 12340005);
});

test("rejects zero, negative, exponent, excess precision and malformed rewards", () => {
  for (const value of ["0", "-1", "1e3", "0.0000001", "01", "1.", "NaN", ""]) {
    assert.throws(() => parseRewardMicros(value), { message: "invalid_reward" });
  }
});

test("verifies recommended HMAC-SHA256 signature", () => {
  const data = { subId: "123", transId: "tx-1", reward: "2.5", secret: "test-secret" };
  const signature2 = crypto.createHmac("sha256", data.secret)
    .update(data.subId + data.transId + data.reward).digest("hex");
  assert.equal(verifyOfferwallSignature({ ...data, signature2 }), true);
});

test("supports legacy MD5 signature during provider migration", () => {
  const data = { subId: "123", transId: "tx-2", reward: "1.25", secret: "test-secret" };
  const signature = crypto.createHash("md5")
    .update(data.subId + data.transId + data.reward + data.secret).digest("hex");
  assert.equal(verifyOfferwallSignature({ ...data, signature }), true);
});

test("rejects altered payloads and malformed signatures", () => {
  const data = { subId: "123", transId: "tx-3", reward: "1", secret: "test-secret", signature2: "xyz" };
  assert.equal(verifyOfferwallSignature(data), false);
  assert.equal(verifyOfferwallSignature({ ...data, reward: "2" }), false);
  assert.equal(verifyOfferwallSignature({ ...data, secret: "" }), false);
});
