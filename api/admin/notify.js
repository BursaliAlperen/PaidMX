import { withStormkitCompat } from "../../lib/stormkit-compat.js";
import { getDb } from "../../lib/db.js";
import { readCookie, verifySession } from "../../lib/session.js";

const ALLOWED_EVENTS = new Set(["payout_approved","payout_rejected","payout_paid","payment_failed","deposit"]);
function adminIds() { return new Set(String(process.env.ADMIN_IDS || "").split(",").map(x=>x.trim()).filter(x=>/^\d+$/.test(x))); }
async function sendTelegram(chatId, message) {
  if (!process.env.BOT_TOKEN) throw new Error("BOT_TOKEN is not configured");
  const r = await fetch("https://api.telegram.org/bot"+process.env.BOT_TOKEN+"/sendMessage", {
    method:"POST",headers:{"content-type":"application/json"},body:JSON.stringify({chat_id:chatId,text:message,disable_web_page_preview:true})
  });
  const data=await r.json();
  if(!r.ok||!data.ok) throw new Error("Telegram message delivery failed");
  return data.result;
}
async function handler(req,res) {
  if(req.method!=="POST"){res.setHeader("Allow","POST");return res.status(405).json({error:"Method not allowed"});}
  const session=verifySession(readCookie(req.headers.cookie,"paidmx_session"),process.env.SESSION_SECRET);
  if(!session||!adminIds().has(session.userId))return res.status(403).json({error:"Admin access required"});
  const body=req.body||{};
  const userId=String(body.telegramId||"");
  const type=String(body.eventType||"");
  const amount=Number(body.amount);
  const currency=String(body.currency||"USDT").slice(0,12);
  const note=String(body.note||"").trim().slice(0,400);
  if(!/^\d{1,20}$/.test(userId)||!ALLOWED_EVENTS.has(type)||!Number.isFinite(amount)||amount<0||amount>1e12)
    return res.status(400).json({error:"Invalid user, event type or amount"});
  try{
    const sql=getDb();
    const users=await sql`SELECT telegram_id FROM paidmx_users WHERE telegram_id=${userId} LIMIT 1`;
    if(!users.length)return res.status(404).json({error:"User not found"});
    const status=type==="payout_paid"||type==="deposit"?"succeeded":type==="payout_rejected"||type==="payment_failed"?"failed":"processing";
    const events=await sql`INSERT INTO paidmx_payment_events (telegram_id,provider,event_type,amount,currency,status,note)
      VALUES (${userId},'admin',${type},${amount},${currency},${status},${note||null}) RETURNING id`;
    const messages={
      payout_approved:"✅ Your PaidMX payout request has been approved and is being processed.",
      payout_rejected:"⚠️ Your PaidMX payout request was rejected."+(note?"\nReason: "+note:""),
      payout_paid:"🎉 Your PaidMX payout is marked as paid."+(amount?"\nAmount: "+amount+" "+currency:""),
      payment_failed:"⚠️ A payment event on your PaidMX account failed."+(note?"\nDetails: "+note:""),
      deposit:"✅ A deposit event was recorded on your PaidMX account."+(amount?"\nAmount: "+amount+" "+currency:"")
    };
    let delivery="failed", telegramMessageId=null, deliveryError=null;
    try{
      const sent=await sendTelegram(userId,messages[type]);
      delivery="sent";telegramMessageId=sent.message_id;
    }catch(e){deliveryError=String(e.message||"Delivery failed").slice(0,300);}
    await sql`INSERT INTO paidmx_notifications (telegram_id,kind,message,status,telegram_message_id,error,sent_at)
      VALUES (${userId},${type},${messages[type]},${delivery},${telegramMessageId},${deliveryError},CASE WHEN ${delivery}='sent' THEN NOW() ELSE NULL END)`;
    await sql`INSERT INTO paidmx_admin_audit (admin_telegram_id,action,target_telegram_id,details)
      VALUES (${session.userId},'payment_event_recorded',${userId},${JSON.stringify({eventId:events[0].id,eventType:type,amount,currency,status,delivery})}::jsonb)`;
    return res.status(200).json({ok:true,eventId:events[0].id,status,notification:delivery});
  }catch(error){
    console.error("PaidMX admin notification:",error?.message||"unknown");
    return res.status(503).json({error:"Could not record the event. Check database migration and bot configuration."});
  }
}

export default withStormkitCompat(handler);
