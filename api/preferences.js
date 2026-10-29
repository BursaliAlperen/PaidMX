import { withStormkitCompat } from "../lib/stormkit-compat.js";
import { getDb } from "../lib/db.js";
import { readCookie, verifySession } from "../lib/session.js";

const LANGUAGES = new Set(["tr", "en", "ar", "ru", "es", "pt", "hi", "id", "zh"]);
const THEMES = new Set(["midnight", "ocean", "emerald", "rose", "violet", "sunset"]);

async function handler(req, res) {
  if (req.method !== "POST") { res.setHeader("Allow", "POST"); return res.status(405).json({ error: "Method not allowed" }); }
  const session = verifySession(readCookie(req.headers.cookie, "paidmx_session"), process.env.SESSION_SECRET);
  if (!session) return res.status(401).json({ error: "Open PaidMX from Telegram to sign in." });
  const language = req.body && req.body.language;
  const theme = req.body && req.body.theme;
  if (!LANGUAGES.has(language) || !THEMES.has(theme)) return res.status(400).json({ error: "Unsupported language or theme" });
  try {
    const sql = getDb();
    const rows = await sql`UPDATE paidmx_users SET language = ${language}, theme = ${theme}, updated_at = NOW()
      WHERE telegram_id = ${session.userId} RETURNING telegram_id`;
    if (!rows.length) return res.status(404).json({ error: "User not found" });
    return res.status(200).json({ saved: true, language: language, theme: theme });
  } catch (error) {
    console.error("PaidMX preferences error:", error?.message || "unknown");
    return res.status(503).json({ error: "Could not save preferences. Check database configuration." });
  }
}

export default withStormkitCompat(handler);
