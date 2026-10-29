import { timingSafeEqual } from "node:crypto";
import { getDb } from "../../lib/db.js";

const EVENT_TYPES = new Set(["deposit","payout_approved","payout_rejected","payout_paid","payment_failed"]);
function secretMatches(received, expected) {
  if(typeof received!=="string"||typeof expected!=="string"||!expected)return false;
  const a=Buffer.from(received);const b=Buffer.from(expected);
  return a.length===b.length&&timingSafeEqual(a,b);
}
async function telegram(method,payload) {
  if(!process.env.BOT_TOKEN)throw new Error("BOT_TOKEN is not configured");
  const r=await fetch("https://api.telegram.org/bot"+process.env.BOT_TOKEN+"/"+method,{method:"POST",headers:{"content-type":"application/json"},body:JSON.stringify(payload)});
  const d=await r.json();if(!r.ok||!d.ok)throw new Error("Telegram API request failed");return d.result;
}
function userMessage(type,amount,currency,note) {
  const value=Number(amount)>0?"\nAmount: "+amount+" "+currency:"";
  const reason=note?"\nDetails: "+note:"";
  return ({
    deposit:"✅ A payment provider confirmed a deposit event for your PaidMX account."+value,
    payout_approved:"✅ Your PaidMX payout request has been approved and is processing."+value,
    payout_rejected:"⚠️ Your PaidMX payout request was rejected."+reason,
    payout_paid:"🎉 Your PaidMX payout was confirmed as paid."+value,
    payment_failed:"⚠️ A payment on your PaidMX account failed."+reason
  })[type];
}
export default async function handler(req,res) {
  if(req.method!=="POST"){res.setHeader("Allow","POST");return res.status(405).json({error:"Method not allowed"});}
  if(!secretMatches(req.headers["x-paidmx-webhook-secret"],process.env.PAYMENT_WEBHOOK_SECRET))return res.status(401).json({error:"Invalid payment webhook secret"});
  const body=req.body||{};
  const eventId=String(body.eventId||"").trim().slice(0,180);
  const provider=String(body.provider||process.env.PAYMENT_PROVIDER||"configured-provider").trim().slice(0,80);
  const telegramId=String(body.telegramId||"");
  const eventType=String(body.eventType||"");
  const amount=Number(body.amount);
  const currency=String(body.currency||"USDT").trim().slice(0,12);
  const note=String(body.note||"").trim().slice(0,400);
  if(!eventId||!/^[0-9]{1,20}$/.test(telegramId)||!EVENT_TYPES.has(eventType)||!Number.isFinite(amount)||amount<0||amount>1e12||!currency)
    return res.status(400).json({error:"Invalid normalized payment event"});
  try {
    const sql=getDb();
    const user=await sql`SELECT telegram_id FROM paidmx_users WHERE telegram_id=${telegramId} AND is_blocked=FALSE LIMIT 1`;
    if(!user.length)return res.status(404).json({error:"User not found or blocked"});
    const status=eventType==="deposit"||eventType==="payout_paid"?"succeeded":eventType==="payout_rejected"||eventType==="payment_failed"?"failed":"processing";
    const inserted=await sql`INSERT INTO paidmx_payment_events (telegram_id,provider,provider_event_id,event_type,amount,currency,status,note)
      VALUES (${telegramId},${provider},${eventId},${eventType},${amount},${currency},${status},${note||null})
      ON CONFLICT (provider,provider_event_id) DO NOTHING RETURNING id`;
    if(!inserted.length)return res.status(200).json({ok:true,duplicate:true});
    const message=userMessage(eventType,amount,currency,note);
    let delivery="failed",messageId=null,errorText=null;
    try{const sent=await telegram("sendMessage",{chat_id:telegramId,text:message,disable_web_page_preview:true});delivery="sent";messageId=sent.message_id;}
    catch(e){errorText=String(e.message||"Telegram delivery failed").slice(0,300);}
    await sql`INSERT INTO paidmx_notifications (telegram_id,kind,message,status,telegram_message_id,error,sent_at)
      VALUES (${telegramId},${eventType},${message},${delivery},${messageId},${errorText},CASE WHEN ${delivery}='sent' THEN NOW() ELSE NULL END)`;
    const adminIds=String(process.env.ADMIN_TELEGRAM_IDS||"").split(",").map(x=>x.trim()).filter(x=>/^\d+$/.test(x));
    await Promise.all(adminIds.map(async id=>{try{await telegram("sendMessage",{chat_id:id,text:"PaidMX payment event: "+eventType+"\nUser: "+telegramId+"\nAmount: "+amount+" "+currency+"\nProvider event: "+eventId,disable_web_page_preview:true});}catch(e){console.error("Admin payment alert failed:",e?.message||"unknown");}}));
    return res.status(200).json({ok:true,eventId:inserted[0].id,notification:delivery});
  }catch(error){console.error("PaidMX payment webhook:",error?.message||"unknown");return res.status(503).json({error:"Payment event could not be recorded"});}
}
