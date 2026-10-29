import { withStormkitCompat } from "../lib/stormkit-compat.js";
import { getDb } from "../lib/db.js";
import { readCookie, verifySession } from "../lib/session.js";

async function handler(req,res) {
  if(req.method!=="GET"){res.setHeader("Allow","GET");return res.status(405).json({error:"Method not allowed"});}
  const session=verifySession(readCookie(req.headers.cookie,"paidmx_session"),process.env.SESSION_SECRET);
  if(!session)return res.status(401).json({error:"Open PaidMX from Telegram to sign in."});
  try {
    const sql=getDb();
    const rows=await sql`SELECT COUNT(*)::int AS referral_count,
      COUNT(*) FILTER (WHERE status='qualified')::int AS qualified_count,
      COUNT(*) FILTER (WHERE status='rewarded')::int AS rewarded_count
      FROM paidmx_referrals WHERE referrer_telegram_id=${session.userId}`;
    return res.status(200).json({ok:true,...rows[0]});
  } catch(error) {
    console.error("PaidMX referral stats:",error?.message||"unknown");
    return res.status(503).json({error:"Referral data unavailable. Run database migrations first."});
  }
}

export default withStormkitCompat(handler);
