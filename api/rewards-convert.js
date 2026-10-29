import { withStormkitCompat } from "../lib/stormkit-compat.js";
import { getDb } from "../lib/db.js";
import { readCookie, verifySession } from "../lib/session.js";

async function handler(req, res) {
  if (req.method !== "POST") {
    res.setHeader("Allow", "POST");
    return res.status(405).json({ error: "Method not allowed" });
  }
  const session = verifySession(readCookie(req.headers.cookie, "paidmx_session"), process.env.SESSION_SECRET);
  if (!session) return res.status(401).json({ error: "Open PaidMX from Telegram to convert real rewards." });

  const rawAmount = req.body && req.body.amount;
  const amount = Number(rawAmount);
  if (!Number.isSafeInteger(amount) || amount < 100 || amount > 1000000000) {
    return res.status(400).json({ error: "Enter a whole MX amount from 100 to 1,000,000,000." });
  }

  try {
    const sql = getDb();
    // A single PostgreSQL statement debits MX, credits GRAM and writes the ledger atomically.
    const rows = await sql`WITH updated AS (
      UPDATE paidmx_users
      SET points = points - ${amount},
          gram_balance = gram_balance + (${amount}::numeric / 10000),
          updated_at = NOW()
      WHERE telegram_id = ${session.userId} AND points >= ${amount}
      RETURNING telegram_id, points, gram_balance
    ), logged AS (
      INSERT INTO paidmx_reward_conversions
        (telegram_id, mx_amount, gram_amount, points_after, gram_balance_after)
      SELECT telegram_id, ${amount}, (${amount}::numeric / 10000), points, gram_balance
      FROM updated
      RETURNING id
    )
    SELECT updated.points, updated.gram_balance, logged.id AS conversion_id
    FROM updated CROSS JOIN logged`;

    if (!rows.length) {
      const current = await sql`SELECT points FROM paidmx_users WHERE telegram_id = ${session.userId} LIMIT 1`;
      if (!current.length) return res.status(404).json({ error: "PaidMX account not found." });
      return res.status(409).json({ error: "Not enough MX balance for this conversion." });
    }
    const row = rows[0];
    return res.status(200).json({
      ok: true,
      conversionId: String(row.conversion_id),
      mxConverted: amount,
      gramReceived: Number((amount / 10000).toFixed(8)),
      points: Number(row.points),
      gramBalance: Number(row.gram_balance)
    });
  } catch (error) {
    console.error("PaidMX MX-to-GRAM conversion error:", error?.message || "unknown");
    return res.status(503).json({ error: "Conversion service unavailable. Ensure database/schema.sql has been applied." });
  }
}

export default withStormkitCompat(handler);
