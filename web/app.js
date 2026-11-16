(() => {
"use strict";
const cfg=window.PAIDMX_CONFIG||{},tg=window.Telegram?.WebApp,$=id=>document.getElementById(id);
let toastTimer, taskCache=[], taskFilter='all', taskLoaded=false;
if(tg){tg.ready();tg.expand();try{tg.setHeaderColor("#102f53");tg.setBackgroundColor("#07172b");}catch(_){}}
function toast(s){const n=$("toast");n.textContent=s;n.classList.add("show");clearTimeout(toastTimer);toastTimer=setTimeout(()=>n.classList.remove("show"),2200);try{tg?.HapticFeedback?.notificationOccurred("success")}catch(_){}}
function authError(s){$("auth-error-text").textContent=s;$("auth-error").classList.remove("hidden");const bot=String(cfg.botUsername||"").replace(/^@/,"");if(bot){$("open-bot").href="https://t.me/"+encodeURIComponent(bot);$("open-bot").classList.remove("hidden")}}
async function rpc(method){if(!cfg.apiUrl)throw Error("API adresi yapılandırılmamış.");if(!tg?.initData)throw Error("Telegram Mini App oturumu bulunamadı.");const r=await fetch(cfg.apiUrl,{method:"POST",headers:{"Content-Type":"application/json","X-Telegram-Init-Data":tg.initData},body:JSON.stringify({rpc:method})});let d;try{d=await r.json()}catch(_){throw Error("Sunucudan geçersiz yanıt alındı.")}if(!r.ok||!d.ok){const m={telegram_auth_expired:"Telegram oturumunun süresi dolmuş. Mini App'i yeniden aç.",telegram_auth_invalid:"Telegram doğrulaması başarısız.",user_banned:"Bu hesap için erişim kapatılmış."};throw Error(m[d.error]||"API isteği başarısız ("+r.status+").")}return d}
function fmt(v){return (Number(v||0)/1e6).toLocaleString("tr-TR",{maximumFractionDigits:6})}
function render(d){const u=d.user||{},w=d.wallet||{},name=u.firstName||u.username||"PaidMX üyesi";$("first-name").textContent=name;$("profile-avatar").textContent=(name[0]||"P").toUpperCase();if(u.photoUrl)$("profile-avatar").style.backgroundImage="url('"+u.photoUrl.replace(/['()\\]/g,"")+"')";const bal=fmt(w.balanceMicros)+" PMX",debt=fmt(w.debtMicros)+" PMX";$("balance").innerHTML=fmt(w.balanceMicros)+' <small>PMX</small>';$("wallet-balance").textContent=bal;$("wallet-available").textContent=bal;$("wallet-debt").textContent=debt;$("home-wallet").textContent=bal;$("home-debt").textContent=debt;$("debt-label").textContent=Number(w.debtMicros||0)>0?"Borç: "+debt:"";$("ref-count").textContent=Number(u.referralCount||0).toLocaleString("tr-TR");$("invite-total").textContent=$("ref-count").textContent;$("ref-earnings").textContent=fmt(u.referralEarningsMicros)+" PMX";$("invite-earned").textContent=fmt(u.referralEarningsMicros)+" PMX";if(d.admin)$("admin-pill").classList.remove("hidden");const bot=String(cfg.botUsername||"").replace(/^@/,""),code=String(u.referralCode||""),link=bot&&code?"https://t.me/"+encodeURIComponent(bot)+"?startapp=ref_"+encodeURIComponent(code):"";$("ref-link").textContent=link||"Bot kullanıcı adı config.js dosyasına eklenmeli.";$("copy-ref").dataset.link=link;$("share-ref").dataset.link=link;$("copy-ref").disabled=!link;$("share-ref").disabled=!link}
function tab(name){document.querySelectorAll(".screen").forEach(s=>s.classList.toggle("active",s.id==="screen-"+name));document.querySelectorAll(".nav-item").forEach(b=>b.classList.toggle("active",b.dataset.tab===name));try{tg?.HapticFeedback?.selectionChanged()}catch(_){}window.scrollTo({top:0,behavior:"smooth"});if(name==="tasks"&&!taskLoaded)loadTasks()}
function safeText(v){return String(v??"").replace(/[<>]/g,"")}
function taskCard(item){
 const card=document.createElement("article");card.className="live-task-card";
 const top=document.createElement("div");top.className="live-task-top";
 const icon=document.createElement("span");icon.className="live-task-icon "+item.type;icon.textContent=item.type==="video"?"▶":item.type==="shortlink"?"↗":"◉";
 const tag=document.createElement("span");tag.className="live-task-tag";tag.textContent=item.type==="video"?"VİDEO":item.type==="shortlink"?"SHORTLINK":"PTC";
 top.append(icon,tag);
 const title=document.createElement("h3");title.textContent=safeText(item.title||"Kısa görev");
 const desc=document.createElement("p");desc.textContent=safeText(item.description||"Görev ayrıntıları için başlat.");
 const meta=document.createElement("div");meta.className="live-task-meta";
 const duration=document.createElement("span");duration.textContent=item.type==="shortlink"?"Tamamlama: sağlayıcı doğrulaması":("⏱ "+Number(item.duration)+" sn");
 const reward=document.createElement("b");reward.textContent="+"+safeText(item.reward)+" "+safeText(item.currency_name||"PMX");
 meta.append(duration,reward);
 const action=document.createElement("a");action.className="task-start";action.href=item.url;action.target="_blank";action.rel="noopener noreferrer";action.textContent="Görevi başlat ↗";
 card.append(top,title,desc,meta,action);return card;
}
function renderTasks(){
 const list=$("task-list");list.replaceChildren();
 const shown=taskCache.filter(x=>taskFilter==="all"||x.type===taskFilter);
 $("task-count").textContent=shown.length+" uygun görev";
 if(!shown.length){const empty=document.createElement("div");empty.className="task-loading";const b=document.createElement("b");b.textContent=taskLoaded?"Şu anda uygun görev yok":"Görevler yükleniyor";const s=document.createElement("small");s.textContent=taskLoaded?"Yeni kısa görevler geldikçe burada görünecek. Biraz sonra tekrar yenile.":"OfferwallApi bağlantısı kuruluyor.";empty.append(b,s);list.append(empty);return}
 shown.forEach(x=>list.append(taskCard(x)));
}
async function loadTasks(){
 const list=$("task-list");if(!list)return;
 $("task-count").textContent="Görevler alınıyor…";
 try{const data=await rpc("getQuickTasks");taskCache=Array.isArray(data.tasks)?data.tasks:[];taskLoaded=true;renderTasks()}
 catch(e){taskLoaded=true;list.replaceChildren();const empty=document.createElement("div");empty.className="task-loading";const b=document.createElement("b");b.textContent="Görevler şu an alınamadı";const s=document.createElement("small");s.textContent=e.message+" API anahtarı ve Bearer token sunucuda tanımlı olmalı.";empty.append(b,s);list.append(empty);$("task-count").textContent="Bağlantı bekleniyor"}
}
document.querySelectorAll("[data-tab]").forEach(b=>b.addEventListener("click",()=>tab(b.dataset.tab)));
$("copy-ref").addEventListener("click",async()=>{const l=$("copy-ref").dataset.link;if(!l)return;try{if(navigator.clipboard?.writeText)await navigator.clipboard.writeText(l);else throw Error();toast("Davet bağlantısı kopyalandı.")}catch(_){toast("Bağlantıyı kopyalamak için uzun bas.")}});
$("share-ref").addEventListener("click",()=>{const l=$("share-ref").dataset.link;if(!l)return;const u="https://t.me/share/url?url="+encodeURIComponent(l)+"&text="+encodeURIComponent("PaidMX'e katıl!");if(tg?.openTelegramLink)tg.openTelegramLink(u);else window.open(u,"_blank","noopener,noreferrer")});
document.querySelectorAll(".filter").forEach(b=>b.addEventListener("click",()=>{document.querySelectorAll(".filter").forEach(x=>x.classList.toggle("active",x===b));taskFilter=b.dataset.filter==="offer"?"ptc":b.dataset.filter==="survey"?"video":b.dataset.filter==="quick"?"shortlink":b.dataset.filter;renderTasks()}));
$("refresh-tasks").addEventListener("click",()=>{taskLoaded=false;loadTasks()});
async function boot(){if(!tg?.initData){authError("PaidMX'i Telegram botunun Mini App butonundan açmalısın.");return}try{render(await rpc("getDashboard"));loadTasks()}catch(e){authError(e.message||"PaidMX API bağlantısı kurulamadı.")}}
boot();
})();