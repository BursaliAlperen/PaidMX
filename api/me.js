import { withStormkitCompat } from "../lib/stormkit-compat.js";
import { getDb } from "../lib/db.js";
import { readCookie, verifySession } from "../lib/session.js";

async function handler(req, res) {
  if (req.method !== "GET") { res.setHeader("Allow", "GET"); return res.status(405).json({ error: "Method not allowed" }); }
  const session = verifySession(readCookie(req.headers.cookie, "paidmx_session"), process.env.SESSION_SECRET);
  if (!session) return res.status(401).json({ authenticated: false });
  try {
    const sql = getDb();
    const rows = await sql`SELECT telegram_id, username, first_name, language, theme, points, usdt_balance, gram_balance
      FROM paidmx_users WHERE telegram_id = ${session.userId} LIMIT 1`;
    if (!rows.length) return res.status(401).json({ authenticated: false });
    const u = rows[0];
    return res.status(200).json({ authenticated: true, onboardingComplete: Boolean(u.language && u.theme),
      user: { id: String(u.telegram_id), username: u.username, firstName: u.first_name,
        language: u.language, theme: u.theme, points: Number(u.points), usdtBalance: Number(u.usdt_balance), gramBalance: Number(u.gram_balance || 0) } });
  } catch (error) {
    console.error("PaidMX profile error:", error?.message || "unknown");
    return res.status(503).json({ error: "Profile storage is unavailable" });
  }
}

export default withStormkitCompat(handler);
