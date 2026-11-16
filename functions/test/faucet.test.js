"use strict";

const test = require("node:test");
const assert = require("node:assert/strict");
const { nextClaimAt, isClaimAllowed, secondsUntilClaim } = require("../lib/faucet");

test("first claim is immediately allowed when no prior claim exists", () => {
  assert.equal(isClaimAllowed(0, 3600, 1000), true);
  assert.equal(secondsUntilClaim(0, 3600, 1000), 0);
});

test("claim is blocked while cooldown has not elapsed", () => {
  assert.equal(isClaimAllowed(1000, 3600, 4599), false);
  assert.equal(secondsUntilClaim(1000, 3600, 4599), 1);
});

test("claim becomes allowed exactly when cooldown elapses", () => {
  assert.equal(isClaimAllowed(1000, 3600, 4600), true);
  assert.equal(nextClaimAt(1000, 3600, 4600), 4600);
});

test("cooldown is clamped to non-negative values", () => {
  assert.equal(nextClaimAt(500, -5, 1000), 500);
  assert.equal(isClaimAllowed(500, 0, 1000), true);
});

test("missing or invalid last claim time is treated as never claimed", () => {
  assert.equal(isClaimAllowed(null, 3600, 1000), true);
  assert.equal(isClaimAllowed("", 3600, 1000), true);
  assert.equal(isClaimAllowed(undefined, 3600, 1000), true);
});
