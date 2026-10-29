import { withStormkitCompat } from "../../lib/stormkit-compat.js";
import { getDb } from "../../lib/db.js";
import { verifyTelegramInitData } from "../../lib/telegram.js";
import { createSession, sessionCookie } from "../../lib/session.js";

async function handler(req, res) {
  if (req.method !== "POST") {
    res.setHeader("Allow", "POST");
    return res.status(405).json({ error: "Method not allowed" });
  }
  const initData = req.body && req.body.initData;
  if (typeof initData !== "string" || initData.length > 8192) return res.status(400).json({ error: "Missing or invalid Telegram initData" });
  if (!process.env.BOT_TOKEN || !process.env.SESSION_SECRET || process.env.SESSION_SECRET.length < 32) {
    return res.status(503).json({ error: "Authentication service is not configured" });
  }
  let tgUser;
  try { tgUser = verifyTelegramInitData(initData, process.env.BOT_TOKEN); }
  catch { return res.status(401).json({ error: "Telegram verification failed. Reopen PaidMX from Telegram." }); }

  try {
    const sql = getDb();
    const rows = await sql`INSERT INTO paidmx_users (telegram_id, username, first_name)
      VALUES (${tgUser.id}, ${tgUser.username}, ${tgUser.firstName})
      ON CONFLICT (telegram_id) DO UPDATE SET username = EXCLUDED.username,
        first_name = EXCLUDED.first_name, updated_at = NOW()
      RETURNING telegram_id, username, first_name, language, theme, points, usdt_balance`;
    const user = rows[0];
    const session = createSession(tgUser.id, process.env.SESSION_SECRET);
    res.setHeader("Set-Cookie", sessionCookie(session.token, session.maxAge));
    return res.status(200).json({
      authenticated: true,
      onboardingComplete: Boolean(user.language && user.theme),
      user: { id: String(user.telegram_id), username: user.username, firstName: user.first_name,
        language: user.language, theme: user.theme, points: Number(user.points), usdtBalance: Number(user.usdt_balance) }
    });
  } catch (error) {
    console.error("PaidMX auth/database error:", error?.message || "unknown");
    return res.status(503).json({ error: "Storage unavailable. Check DATABASE_URL and run database/schema.sql." });
  }
}

export default withStormkitCompat(handler);
