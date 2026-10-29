import { getDb } from "../../lib/db.js";
import { readCookie, verifySession } from "../../lib/session.js";

function adminIds() {
  return new Set(String(process.env.ADMIN_IDS || process.env.ADMIN_TELEGRAM_IDS || "").split(",").map(x => x.trim()).filter(x => /^\d+$/.test(x)));
}
export default async function handler(req, res) {
  if (req.method !== "GET") { res.setHeader("Allow","GET"); return res.status(405).json({error:"Method not allowed"}); }
  const session = verifySession(readCookie(req.headers.cookie, "paidmx_session"), process.env.SESSION_SECRET);
  if (!session || !adminIds().has(session.userId)) return res.status(403).json({error:"Admin access required"});
  try {
    const sql = getDb();
    const [counts, recentUsers, referrals, payments] = await Promise.all([
      sql`SELECT COUNT(*)::int AS users, COALESCE(SUM(points),0)::text AS points,
        COALESCE(SUM(usdt_balance),0)::text AS usdt_balance,
        COUNT(*) FILTER (WHERE created_at > NOW() - INTERVAL '24 hours')::int AS new_today
        FROM paidmx_users`,
      sql`SELECT telegram_id, username, first_name, language, points, usdt_balance, created_at
        FROM paidmx_users ORDER BY created_at DESC LIMIT 25`,
      sql`SELECT r.id, r.referrer_telegram_id, r.referred_telegram_id, r.status, r.reward_points, r.created_at,
        u.username AS referrer_username, v.username AS referred_username
        FROM paidmx_referrals r LEFT JOIN paidmx_users u ON u.telegram_id=r.referrer_telegram_id
        LEFT JOIN paidmx_users v ON v.telegram_id=r.referred_telegram_id
        ORDER BY r.created_at DESC LIMIT 50`,
      sql`SELECT id, telegram_id, provider, event_type, amount, currency, status, note, created_at
        FROM paidmx_payment_events ORDER BY created_at DESC LIMIT 50`
    ]);
    return res.status(200).json({ok:true,stats:counts[0],users:recentUsers,referrals,payments});
  } catch (error) {
    console.error("PaidMX admin overview:", error?.message || "unknown");
    return res.status(503).json({error:"Admin data unavailable. Run database migrations first."});
  }
}
