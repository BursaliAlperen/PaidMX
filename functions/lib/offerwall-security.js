"use strict";

const crypto = require("node:crypto");

function constantTimeHexEqual(expected, supplied) {
  if (typeof supplied !== "string" || !/^[a-f0-9]+$/i.test(supplied)) return false;
  const left = Buffer.from(expected, "hex");
  const right = Buffer.from(supplied, "hex");
  return left.length === right.length && crypto.timingSafeEqual(left, right);
}

function parseRewardMicros(value) {
  const raw = String(value ?? "");
  if (!/^(?:0|[1-9]\\d{0,11})(?:\\.\\d{1,6})?$/.test(raw)) {
    throw new Error("invalid_reward");
  }
  const [whole, fraction = ""] = raw.split(".");
  const micros = BigInt(whole) * 1000000n + BigInt((fraction + "000000").slice(0, 6));
  if (micros <= 0n || micros > BigInt(Number.MAX_SAFE_INTEGER)) {
    throw new Error("invalid_reward");
  }
  return Number(micros);
}

function verifyOfferwallSignature({ subId, transId, reward, signature2, signature, secret }) {
  if (typeof secret !== "string" || secret.length === 0) return false;
  const signed = String(subId) + String(transId) + String(reward);
  const validHmac = constantTimeHexEqual(
    crypto.createHmac("sha256", secret).update(signed).digest("hex"),
    signature2
  );
  const validLegacy = constantTimeHexEqual(
    crypto.createHash("md5").update(signed + secret).digest("hex"),
    signature
  );
  return validHmac || validLegacy;
}

module.exports = { parseRewardMicros, verifyOfferwallSignature };
