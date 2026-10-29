import { withStormkitCompat } from "../../lib/stormkit-compat.js";
import { getDb } from "../../lib/db.js";

const BOT_USERNAME = (process.env.TELEGRAM_BOT_USERNAME || "PaidMX_bot").replace(/^@/, "");
const COPY = {
  tr: { title:"PaidMX'e hoş geldin! 🎉", body:"İzle, oyna, görevleri keşfet ve hesabını tek yerden yönet. Başlamak için aşağıdaki düğmeye dokun.", button:"PaidMX'i aç", referral:"Arkadaş davet bağlantın hazır. Uygulamada davetler bölümünden paylaşabilirsin." },
  en: { title:"Welcome to PaidMX! 🎉", body:"Discover tasks, mini games and your account in one place. Tap below to get started.", button:"Open PaidMX", referral:"Your referral link is available in the Invites section of the app." },
  ar: { title:"أهلاً بك في PaidMX! 🎉", body:"اكتشف المهام والألعاب المصغرة وأدر حسابك من مكان واحد. اضغط أدناه للبدء.", button:"افتح PaidMX", referral:"ستجد رابط الدعوة في قسم الدعوات داخل التطبيق." },
  ru: { title:"Добро пожаловать в PaidMX! 🎉", body:"Задания, мини-игры и управление аккаунтом в одном месте. Нажмите ниже, чтобы начать.", button:"Открыть PaidMX", referral:"Ссылка-приглашение доступна в разделе приглашений приложения." },
  es: { title:"¡Te damos la bienvenida a PaidMX! 🎉", body:"Descubre tareas, minijuegos y gestiona tu cuenta desde un solo lugar. Pulsa abajo para empezar.", button:"Abrir PaidMX", referral:"Encontrarás tu enlace de invitación en la sección Invitaciones." },
  pt: { title:"Boas-vindas ao PaidMX! 🎉", body:"Descubra tarefas, minijogos e gerencie sua conta em um só lugar. Toque abaixo para começar.", button:"Abrir PaidMX", referral:"Seu link de convite fica na seção Convites do aplicativo." },
  hi: { title:"PaidMX में आपका स्वागत है! 🎉", body:"टास्क, मिनी गेम और अपना अकाउंट एक ही जगह देखें। शुरू करने के लिए नीचे टैप करें।", button:"PaidMX खोलें", referral:"आपका रेफ़रल लिंक ऐप के आमंत्रण अनुभाग में मिलेगा।" },
  id: { title:"Selamat datang di PaidMX! 🎉", body:"Temukan tugas, mini game, dan kelola akun Anda di satu tempat. Ketuk di bawah untuk mulai.", button:"Buka PaidMX", referral:"Tautan referral tersedia di bagian Undangan aplikasi." },
  zh: { title:"欢迎使用 PaidMX！🎉", body:"在一个地方探索任务、小游戏并管理账户。点击下方开始。", button:"打开 PaidMX", referral:"你可以在应用的邀请页面找到专属邀请链接。" }
};
function languageFor(code) {
  const short = String(code || "en").toLowerCase().split("-")[0];
  return Object.prototype.hasOwnProperty.call(COPY, short) ? short : "en";
}
async function telegram(method, payload) {
  if (!process.env.BOT_TOKEN) throw new Error("BOT_TOKEN is not configured");
  const response = await fetch("https://api.telegram.org/bot" + process.env.BOT_TOKEN + "/" + method, {
    method:"POST", headers:{"content-type":"application/json"}, body:JSON.stringify(payload)
  });
  const data = await response.json();
  if (!response.ok || !data.ok) throw new Error("Telegram API request failed");
  return data.result;
}
async function handler(req, res) {
  if (req.method !== "POST") { res.setHeader("Allow","POST"); return res.status(405).json({error:"Method not allowed"}); }
  const expected = process.env.TELEGRAM_WEBHOOK_SECRET;
  if (!expected || req.headers["x-telegram-bot-api-secret-token"] !== expected) return res.status(401).json({error:"Unauthorized webhook"});
  const update = req.body || {};
  const message = update.message;
  if (!message || !message.chat || message.chat.type !== "private" || typeof message.text !== "string") return res.status(200).json({ok:true,ignored:true});
  const text = message.text.trim();
  if (!/^\/start(?:\s|$)/i.test(text)) return res.status(200).json({ok:true,ignored:true});
  const tg = message.from || {};
  if (!tg.id || !Number.isSafeInteger(Number(tg.id))) return res.status(200).json({ok:true,ignored:true});
  const lang = languageFor(tg.language_code);
  const match = text.match(/^\/start(?:\s+([A-Za-z0-9_-]{1,64}))?/i);
  const payload = match && match[1] ? match[1] : "";
  const referrer = payload.match(/^ref_(\d{1,20})$/);
  try {
    const sql = getDb();
    const existing = await sql`SELECT telegram_id, language, referrer_telegram_id FROM paidmx_users WHERE telegram_id = ${String(tg.id)} LIMIT 1`;
    let selectedLang = existing[0] && existing[0].language ? existing[0].language : lang;
    let referrerId = referrer ? referrer[1] : null;
    if (referrerId === String(tg.id)) referrerId = null;
    if (referrerId) {
      const validReferrer = await sql`SELECT telegram_id FROM paidmx_users WHERE telegram_id = ${referrerId} LIMIT 1`;
      if (!validReferrer.length) referrerId = null;
    }
    await sql`INSERT INTO paidmx_users (telegram_id, username, first_name, language, referrer_telegram_id)
      VALUES (${String(tg.id)}, ${typeof tg.username === "string" ? tg.username.slice(0,64) : null},
        ${typeof tg.first_name === "string" ? tg.first_name.slice(0,128) : ""}, ${selectedLang}, ${referrerId})
      ON CONFLICT (telegram_id) DO UPDATE SET username = EXCLUDED.username,
        first_name = EXCLUDED.first_name, updated_at = NOW()`;
    if (!existing.length && referrerId) {
      await sql`INSERT INTO paidmx_referrals (referrer_telegram_id, referred_telegram_id)
        SELECT ${referrerId}, ${String(tg.id)}
        WHERE EXISTS (SELECT 1 FROM paidmx_users WHERE telegram_id = ${referrerId})
        ON CONFLICT (referred_telegram_id) DO NOTHING`;
      await sql`UPDATE paidmx_users SET referral_count = referral_count + 1 WHERE telegram_id = ${referrerId}
        AND EXISTS (SELECT 1 FROM paidmx_referrals WHERE referrer_telegram_id = ${referrerId} AND referred_telegram_id = ${String(tg.id)})`;
    }
    const copy = COPY[selectedLang] || COPY.en;
    const appUrl = process.env.PUBLIC_APP_URL;
    const replyMarkup = appUrl ? {inline_keyboard:[[{text:copy.button,web_app:{url:appUrl}}]]} : {inline_keyboard:[[{text:copy.button,url:"https://t.me/" + BOT_USERNAME}]]};
    const referralLine = referrerId ? "\n\n" + copy.referral : "";
    await telegram("sendMessage", {chat_id:message.chat.id, text:copy.title + "\n\n" + copy.body + referralLine,
      reply_markup:replyMarkup, disable_web_page_preview:true});
    return res.status(200).json({ok:true});
  } catch (error) {
    console.error("PaidMX Telegram webhook:", error?.message || "unknown");
    return res.status(500).json({error:"Webhook processing failed"});
  }
}

export default withStormkitCompat(handler);
