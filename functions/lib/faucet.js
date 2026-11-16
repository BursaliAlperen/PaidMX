"use strict";

// Pure helpers for the server-authoritative faucet cooldown. Kept free of
// Firestore/network dependencies so they can be unit-tested in isolation.
function nextClaimAt(lastClaimAtSeconds, cooldownSeconds, nowSeconds) {
  const last = Number(lastClaimAtSeconds) || 0;
  if (last <= 0) return 0; // Never claimed: immediately allowed.
  const cd = Math.max(0, Number(cooldownSeconds) || 0);
  return last + cd;
}

function isClaimAllowed(lastClaimAtSeconds, cooldownSeconds, nowSeconds) {
  return nextClaimAt(lastClaimAtSeconds, cooldownSeconds, nowSeconds) <= (Number(nowSeconds) || 0);
}

function secondsUntilClaim(lastClaimAtSeconds, cooldownSeconds, nowSeconds) {
  const next = nextClaimAt(lastClaimAtSeconds, cooldownSeconds, nowSeconds);
  return Math.max(0, next - (Number(nowSeconds) || 0));
}

module.exports = { nextClaimAt, isClaimAllowed, secondsUntilClaim };
