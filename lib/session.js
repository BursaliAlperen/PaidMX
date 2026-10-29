import { createHmac, timingSafeEqual } from "node:crypto";

const DURATION = 7 * 24 * 60 * 60;
function signature(payload, secret) {
  return createHmac("sha256", secret).update(payload).digest("base64url");
}
export function createSession(userId, secret, nowSeconds = Math.floor(Date.now() / 1000)) {
  if (typeof secret !== "string" || secret.length < 32) throw new Error("SESSION_SECRET must have at least 32 characters");
  const payload = Buffer.from(JSON.stringify({ sub: String(userId), exp: nowSeconds + DURATION })).toString("base64url");
  return { token: payload + "." + signature(payload, secret), maxAge: DURATION };
}
export function verifySession(token, secret, nowSeconds = Math.floor(Date.now() / 1000)) {
  if (typeof token !== "string" || typeof secret !== "string" || secret.length < 32) return null;
  const parts = token.split(".");
  if (parts.length !== 2) return null;
  const expected = Buffer.from(signature(parts[0], secret));
  const actual = Buffer.from(parts[1]);
  if (expected.length !== actual.length || !timingSafeEqual(expected, actual)) return null;
  try {
    const payload = JSON.parse(Buffer.from(parts[0], "base64url").toString("utf8"));
    if (typeof payload.sub !== "string" || !payload.sub || !Number.isInteger(payload.exp) || payload.exp <= nowSeconds) return null;
    return { userId: payload.sub, exp: payload.exp };
  } catch { return null; }
}
export function readCookie(header, name) {
  if (typeof header !== "string") return null;
  for (const part of header.split(";")) {
    const pos = part.indexOf("=");
    if (pos >= 0 && part.slice(0, pos).trim() === name) return decodeURIComponent(part.slice(pos + 1).trim());
  }
  return null;
}
export function sessionCookie(token, maxAge, production = process.env.NODE_ENV === "production") {
  return "paidmx_session=" + encodeURIComponent(token) + "; HttpOnly; Path=/; SameSite=Lax; Max-Age=" + maxAge + (production ? "; Secure" : "");
}
