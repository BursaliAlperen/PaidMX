const TG = window.Telegram && window.Telegram.WebApp;
const KEY = "paidmx:onboarding:v1";
const BOT = "PaidMX_bot";
const root = document.getElementById("app");

const LANGS = [
  ["tr","🇹🇷","Türkçe"],["en","🇬🇧","English"],["ar","🇸🇦","العربية"],["ru","🇷🇺","Русский"],
  ["es","🇪🇸","Español"],["pt","🇧🇷","Português"],["hi","🇮🇳","हिन्दी"],["id","🇮🇩","Indonesia"],["zh","🇨🇳","简体中文"]
];
const THEMES = [
  ["midnight","Midnight","Black · White",["#151517","#fff","#85858e"]],
  ["ocean","Ocean","Blue · White",["#2563eb","#fff","#93c5fd"]],
  ["emerald","Emerald","Green · Deep",["#16a34a","#10251d","#86efac"]],
  ["rose","Rose","Pink · White",["#db2777","#fff","#f9a8d4"]],
  ["violet","Violet","Purple · Dark",["#8b5cf6","#171329","#c4b5fd"]],
  ["sunset","Sunset","Orange · Warm",["#ea580c","#28180f","#fdba74"]]
];
const WORDS = {
  en:{welcome:"Welcome to",tagline:"Watch. Play. Earn.",intro:"Rewards, mini games and tasks — all in one place.",start:"Get started",language:"Choose your language",languageNote:"You can change this later in settings.",continue:"Continue",theme:"Choose your style",themeNote:"Pick the colors that feel like you.",enter:"Enter PaidMX",back:"Back",home:"Home",tasks:"Tasks",arena:"Arena",invites:"Invites",wallet:"Wallet",total:"TOTAL BALANCE",points:"PTS",convert:"Convert",withdraw:"Withdraw",daily:"Daily check-in",streak:"day streak",promo:"Have a promo code?",spin:"Spin",play:"Play",redeem:"Redeem",invite:"Invite",live:"LIVE",openTasks:"Open tasks",allTasks:"All tasks",watch:"Watch",ad:"Rewarded video",adNote:"Connect an ad provider to enable rewards.",soon:"Coming soon",walletNote:"Your balance will appear here when rewards are enabled.",inviteTitle:"Invite friends",inviteNote:"Your personal Telegram invite link",copy:"Copy link",copied:"Copied",preview:"Preview mode",settings:"Settings",changeLanguage:"Change language",changeTheme:"Change theme",error:"Could not save preferences.",promoNote:"Promo codes will be enabled after the rewards backend is configured.",arenaNote:"Mini games are being prepared.",withdrawNote:"Withdrawals are not enabled yet.",noRewards:"No live rewards yet",member:"PaidMX Member"},
  tr:{welcome:"Hoş geldin,",tagline:"İzle. Oyna. Kazan.",intro:"Ödüller, mini oyunlar ve görevler tek yerde.",start:"Başlayalım",language:"Dilini seç",languageNote:"Bu tercihi daha sonra ayarlardan değiştirebilirsin.",continue:"Devam et",theme:"Tarzını seç",themeNote:"Sana en uygun renkleri seç.",enter:"PaidMX'e gir",back:"Geri",home:"Ana sayfa",tasks:"Görevler",arena:"Arena",invites:"Davetler",wallet:"Cüzdan",total:"TOPLAM BAKİYE",points:"PTS",convert:"Dönüştür",withdraw:"Çek",daily:"Günlük giriş",streak:"günlük seri",promo:"Promosyon kodun var mı?",spin:"Çevir",play:"Oyna",redeem:"Kullan",invite:"Davet et",live:"YAYINDA",openTasks:"Açık görevler",allTasks:"Tüm görevler",watch:"İzle",ad:"Ödüllü video",adNote:"Ödül kazanmak için reklam sağlayıcısı bağlanmalı.",soon:"Yakında",walletNote:"Ödül sistemi açıldığında bakiyen burada görünür.",inviteTitle:"Arkadaşlarını davet et",inviteNote:"Kişisel Telegram davet bağlantın",copy:"Bağlantıyı kopyala",copied:"Kopyalandı",preview:"Ön izleme modu",settings:"Ayarlar",changeLanguage:"Dili değiştir",changeTheme:"Temayı değiştir",error:"Tercihler kaydedilemedi.",promoNote:"Ödül sistemi yapılandırılınca promosyon kodları etkinleştirilecek.",arenaNote:"Mini oyunlar hazırlanıyor.",withdrawNote:"Çekim işlemleri henüz etkin değil.",noRewards:"Henüz aktif ödül yok",member:"PaidMX üyesi"},
  ar:{welcome:"مرحبًا بك في",tagline:"شاهد. العب. اكسب.",intro:"المكافآت والألعاب والمهام في مكان واحد.",start:"ابدأ الآن",language:"اختر لغتك",languageNote:"يمكنك تغييرها لاحقًا من الإعدادات.",continue:"متابعة",theme:"اختر مظهرك",themeNote:"اختر الألوان التي تناسبك.",enter:"الدخول إلى PaidMX",back:"رجوع",home:"الرئيسية",tasks:"المهام",arena:"الساحة",invites:"الدعوات",wallet:"المحفظة",total:"إجمالي الرصيد",points:"نقطة",convert:"تحويل",withdraw:"سحب",daily:"تسجيل يومي",streak:"أيام متتالية",promo:"هل لديك رمز ترويجي؟",spin:"دوّر",play:"العب",redeem:"استخدم",invite:"ادعُ",live:"مباشر",openTasks:"المهام المفتوحة",allTasks:"كل المهام",watch:"شاهد",ad:"فيديو بمكافأة",adNote:"يجب ربط مزود إعلانات لتفعيل المكافآت.",soon:"قريبًا",walletNote:"سيظهر رصيدك عند تفعيل المكافآت.",inviteTitle:"ادعُ أصدقاءك",inviteNote:"رابط دعوتك الشخصي",copy:"نسخ الرابط",copied:"تم النسخ",preview:"وضع المعاينة",settings:"الإعدادات",changeLanguage:"تغيير اللغة",changeTheme:"تغيير المظهر",error:"تعذر حفظ الإعدادات.",promoNote:"سيتم تفعيل الرموز بعد إعداد نظام المكافآت.",arenaNote:"يتم تجهيز الألعاب المصغرة.",withdrawNote:"السحب غير متاح بعد.",noRewards:"لا توجد مكافآت نشطة بعد",member:"عضو PaidMX"},
  ru:{welcome:"Добро пожаловать в",tagline:"Смотри. Играй. Зарабатывай.",intro:"Задания, мини-игры и награды в одном месте.",start:"Начать",language:"Выберите язык",languageNote:"Язык можно изменить в настройках.",continue:"Продолжить",theme:"Выберите стиль",themeNote:"Выберите подходящие цвета.",enter:"Войти в PaidMX",back:"Назад",home:"Главная",tasks:"Задания",arena:"Арена",invites:"Приглашения",wallet:"Кошелёк",total:"ОБЩИЙ БАЛАНС",points:"ОЧКИ",convert:"Обменять",withdraw:"Вывести",daily:"Ежедневный вход",streak:"дней подряд",promo:"Есть промокод?",spin:"Крутить",play:"Играть",redeem:"Ввести",invite:"Пригласить",live:"В ЭФИРЕ",openTasks:"Доступные задания",allTasks:"Все задания",watch:"Смотреть",ad:"Рекламное видео",adNote:"Подключите рекламную сеть для наград.",soon:"Скоро",walletNote:"Баланс появится после запуска наград.",inviteTitle:"Пригласить друзей",inviteNote:"Ваша личная ссылка Telegram",copy:"Копировать ссылку",copied:"Скопировано",preview:"Предпросмотр",settings:"Настройки",changeLanguage:"Изменить язык",changeTheme:"Изменить тему",error:"Не удалось сохранить настройки.",promoNote:"Промокоды будут доступны после настройки наград.",arenaNote:"Мини-игры готовятся.",withdrawNote:"Вывод пока недоступен.",noRewards:"Пока нет активных наград",member:"Участник PaidMX"},
  es:{welcome:"Te damos la bienvenida a",tagline:"Mira. Juega. Gana.",intro:"Recompensas, minijuegos y tareas en un solo lugar.",start:"Comenzar",language:"Elige tu idioma",languageNote:"Puedes cambiarlo en ajustes.",continue:"Continuar",theme:"Elige tu estilo",themeNote:"Elige los colores que te gusten.",enter:"Entrar a PaidMX",back:"Atrás",home:"Inicio",tasks:"Tareas",arena:"Arena",invites:"Invitaciones",wallet:"Billetera",total:"SALDO TOTAL",points:"PTS",convert:"Convertir",withdraw:"Retirar",daily:"Registro diario",streak:"días seguidos",promo:"¿Tienes un código?",spin:"Girar",play:"Jugar",redeem:"Canjear",invite:"Invitar",live:"EN VIVO",openTasks:"Tareas abiertas",allTasks:"Todas las tareas",watch:"Ver",ad:"Vídeo recompensado",adNote:"Conecta una red publicitaria para activar recompensas.",soon:"Próximamente",walletNote:"Tu saldo aparecerá al activar las recompensas.",inviteTitle:"Invita a tus amigos",inviteNote:"Tu enlace personal de Telegram",copy:"Copiar enlace",copied:"Copiado",preview:"Vista previa",settings:"Ajustes",changeLanguage:"Cambiar idioma",changeTheme:"Cambiar tema",error:"No se pudieron guardar los cambios.",promoNote:"Los códigos se activarán al configurar las recompensas.",arenaNote:"Estamos preparando los minijuegos.",withdrawNote:"Los retiros aún no están habilitados.",noRewards:"Aún no hay recompensas activas",member:"Miembro de PaidMX"},
  pt:{welcome:"Boas-vindas ao",tagline:"Assista. Jogue. Ganhe.",intro:"Recompensas, minijogos e tarefas em um só lugar.",start:"Começar",language:"Escolha seu idioma",languageNote:"Você pode alterar isso nas configurações.",continue:"Continuar",theme:"Escolha seu estilo",themeNote:"Escolha suas cores favoritas.",enter:"Entrar no PaidMX",back:"Voltar",home:"Início",tasks:"Tarefas",arena:"Arena",invites:"Convites",wallet:"Carteira",total:"SALDO TOTAL",points:"PTS",convert:"Converter",withdraw:"Sacar",daily:"Check-in diário",streak:"dias seguidos",promo:"Tem um código promocional?",spin:"Girar",play:"Jogar",redeem:"Resgatar",invite:"Convidar",live:"AO VIVO",openTasks:"Tarefas abertas",allTasks:"Todas as tarefas",watch:"Assistir",ad:"Vídeo recompensado",adNote:"Conecte uma rede de anúncios para ativar recompensas.",soon:"Em breve",walletNote:"O saldo aparecerá após ativar as recompensas.",inviteTitle:"Convide amigos",inviteNote:"Seu link pessoal do Telegram",copy:"Copiar link",copied:"Copiado",preview:"Prévia",settings:"Configurações",changeLanguage:"Alterar idioma",changeTheme:"Alterar tema",error:"Não foi possível salvar.",promoNote:"Os códigos serão ativados após configurar as recompensas.",arenaNote:"Os minijogos estão sendo preparados.",withdrawNote:"Saques ainda não estão disponíveis.",noRewards:"Ainda não há recompensas ativas",member:"Membro PaidMX"},
  hi:{welcome:"आपका स्वागत है",tagline:"देखें। खेलें। कमाएँ।",intro:"रिवॉर्ड, मिनी गेम और टास्क — सब एक जगह।",start:"शुरू करें",language:"भाषा चुनें",languageNote:"आप इसे बाद में बदल सकते हैं।",continue:"जारी रखें",theme:"अपनी शैली चुनें",themeNote:"अपने पसंदीदा रंग चुनें।",enter:"PaidMX खोलें",back:"वापस",home:"होम",tasks:"टास्क",arena:"एरीना",invites:"आमंत्रण",wallet:"वॉलेट",total:"कुल बैलेंस",points:"PTS",convert:"बदलें",withdraw:"निकालें",daily:"दैनिक चेक-इन",streak:"दिन लगातार",promo:"प्रोमो कोड है?",spin:"घुमाएँ",play:"खेलें",redeem:"रिडीम",invite:"आमंत्रित करें",live:"लाइव",openTasks:"खुले टास्क",allTasks:"सभी टास्क",watch:"देखें",ad:"रिवॉर्ड वीडियो",adNote:"रिवॉर्ड के लिए विज्ञापन प्रदाता जोड़ें।",soon:"जल्द आ रहा है",walletNote:"रिवॉर्ड चालू होने पर बैलेंस दिखेगा।",inviteTitle:"दोस्तों को आमंत्रित करें",inviteNote:"आपका निजी Telegram लिंक",copy:"लिंक कॉपी करें",copied:"कॉपी हो गया",preview:"प्रीव्यू मोड",settings:"सेटिंग्स",changeLanguage:"भाषा बदलें",changeTheme:"थीम बदलें",error:"सेटिंग्स सेव नहीं हुईं।",promoNote:"रिवॉर्ड सिस्टम सेट होने के बाद कोड चालू होंगे।",arenaNote:"मिनी गेम तैयार किए जा रहे हैं।",withdrawNote:"निकासी अभी चालू नहीं है।",noRewards:"अभी कोई लाइव रिवॉर्ड नहीं",member:"PaidMX सदस्य"},
  id:{welcome:"Selamat datang di",tagline:"Tonton. Main. Dapatkan.",intro:"Hadiah, mini game, dan tugas dalam satu tempat.",start:"Mulai",language:"Pilih bahasa",languageNote:"Anda bisa mengubahnya di pengaturan.",continue:"Lanjutkan",theme:"Pilih gaya",themeNote:"Pilih warna yang Anda suka.",enter:"Masuk ke PaidMX",back:"Kembali",home:"Beranda",tasks:"Tugas",arena:"Arena",invites:"Undangan",wallet:"Dompet",total:"TOTAL SALDO",points:"PTS",convert:"Konversi",withdraw:"Tarik",daily:"Check-in harian",streak:"hari beruntun",promo:"Punya kode promo?",spin:"Putar",play:"Main",redeem:"Tukar",invite:"Undang",live:"LIVE",openTasks:"Tugas terbuka",allTasks:"Semua tugas",watch:"Tonton",ad:"Video berhadiah",adNote:"Hubungkan penyedia iklan untuk mengaktifkan hadiah.",soon:"Segera hadir",walletNote:"Saldo muncul setelah hadiah diaktifkan.",inviteTitle:"Undang teman",inviteNote:"Tautan Telegram pribadi Anda",copy:"Salin tautan",copied:"Tersalin",preview:"Mode pratinjau",settings:"Pengaturan",changeLanguage:"Ubah bahasa",changeTheme:"Ubah tema",error:"Preferensi tidak dapat disimpan.",promoNote:"Kode aktif setelah sistem hadiah disiapkan.",arenaNote:"Mini game sedang disiapkan.",withdrawNote:"Penarikan belum tersedia.",noRewards:"Belum ada hadiah aktif",member:"Anggota PaidMX"},
  zh:{welcome:"欢迎使用",tagline:"观看 · 游戏 · 赚取",intro:"任务、小游戏和奖励，一站式体验。",start:"开始使用",language:"选择语言",languageNote:"之后可以在设置中更改。",continue:"继续",theme:"选择界面风格",themeNote:"选择你喜欢的配色。",enter:"进入 PaidMX",back:"返回",home:"首页",tasks:"任务",arena:"竞技场",invites:"邀请",wallet:"钱包",total:"总余额",points:"积分",convert:"兑换",withdraw:"提现",daily:"每日签到",streak:"连续天数",promo:"有优惠码吗？",spin:"转盘",play:"游戏",redeem:"兑换",invite:"邀请好友",live:"进行中",openTasks:"开放任务",allTasks:"全部任务",watch:"观看",ad:"激励视频",adNote:"连接广告平台后即可启用奖励。",soon:"即将推出",walletNote:"奖励功能启用后会显示余额。",inviteTitle:"邀请朋友",inviteNote:"你的专属 Telegram 邀请链接",copy:"复制链接",copied:"已复制",preview:"预览模式",settings:"设置",changeLanguage:"更改语言",changeTheme:"更改主题",error:"无法保存设置，请重试。",promoNote:"奖励系统配置完成后将启用优惠码。",arenaNote:"小游戏正在准备中。",withdrawNote:"提现功能尚未启用。",noRewards:"暂无可用奖励",member:"PaidMX 用户"}
};

let s = { step:"welcome", language:"en", theme:"midnight", page:"home", user:null, authenticated:false, preview:true, settings:false, wallet:null, tonUI:null };

function tr(key) { return (WORDS[s.language] && WORDS[s.language][key]) || WORDS.en[key] || key; }
function safe(value) { return String(value == null ? "" : value).replace(/[&<>"']/g, function(c){return ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"})[c];}); }
function svg(name) {
  const paths = {
    home:'<path d="m3 10 9-7 9 7"/><path d="M5 9v11h14V9"/><path d="M9 20v-6h6v6"/>',
    tasks:'<rect x="5" y="4" width="14" height="17" rx="2"/><path d="M9 4V2h6v2M8 10h8M8 14h8M8 18h4"/>',
    arena:'<path d="M6 10h12a4 4 0 0 1 3.8 5.2l-1 3A2 2 0 0 1 17 19l-3-3h-4l-3 3a2 2 0 0 1-3.8-.8l-1-3A4 4 0 0 1 6 10Z"/><path d="M7 13v4M5 15h4M16 14h.01M18 16h.01"/>',
    users:'<path d="M16 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="10" cy="7" r="4"/><path d="M20 8v6M17 11h6"/>',
    wallet:'<rect x="3" y="5" width="18" height="15" rx="2"/><path d="M3 8h18M16 14h2"/>',
    arrow:'<path d="M5 12h14M13 6l6 6-6 6"/>',
    settings:'<circle cx="12" cy="12" r="3"/><path d="M19 13.5a7 7 0 0 0 0-3l2-1.4-2-3.4-2.3.9a7 7 0 0 0-2.6-1.5L13.7 2h-4l-.4 3.1a7 7 0 0 0-2.6 1.5l-2.3-.9-2 3.4 2 1.4a7 7 0 0 0 0 3l-2 1.4 2 3.4 2.3-.9a7 7 0 0 0 2.6 1.5l.4 3.1h4l.4-3.1a7 7 0 0 0 2.6-1.5l2.3.9 2-3.4Z"/>',
    ticket:'<path d="M3 8a2 2 0 0 0 0 4 2 2 0 0 1 0 4h18a2 2 0 0 0 0-4 2 2 0 0 1 0-4Z"/><path d="M13 8v2m0 3v2"/>',
    sun:'<circle cx="12" cy="12" r="4"/><path d="M12 2v2m0 16v2M4.9 4.9l1.4 1.4m11.4 11.4 1.4 1.4M2 12h2m16 0h2"/>',
    close:'<path d="m6 6 12 12M18 6 6 18"/>'
  };
  return '<svg class="icon" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">' + (paths[name] || paths.home) + '</svg>';
}
function brand() { return '<div class="brand"><div class="brand-mark">P<span>MX</span></div><b>PaidMX</b></div>'; }
function themeApply() {
  document.documentElement.dataset.theme = s.theme;
  document.documentElement.lang = s.language;
  document.documentElement.dir = s.language === "ar" ? "rtl" : "ltr";
  if (TG) { try { TG.setHeaderColor(THEMES.find(function(x){return x[0]===s.theme;})[3][0]); } catch {} }
}
function localPrefs() {
  try {
    const p = JSON.parse(localStorage.getItem(KEY) || "null");
    return p && LANGS.some(function(x){return x[0]===p.language;}) && THEMES.some(function(x){return x[0]===p.theme;}) ? p : null;
  } catch { return null; }
}
function saveLocal() { try { localStorage.setItem(KEY, JSON.stringify({language:s.language,theme:s.theme})); } catch {} }
async function request(url, body) {
  const r = await fetch(url,{method:"POST",headers:{"Content-Type":"application/json"},credentials:"same-origin",body:JSON.stringify(body)});
  const data = await r.json().catch(function(){return {};});
  if (!r.ok) throw new Error(data.error || "Request failed");
  return data;
}
function toast(message) {
  let node = document.getElementById("toast");
  if (!node) { node=document.createElement("div"); node.id="toast"; node.className="toast floating"; document.body.appendChild(node); }
  node.textContent=message; node.classList.add("show");
  clearTimeout(toast.timer); toast.timer=setTimeout(function(){node.classList.remove("show");},2600);
}
async function init() {
  if (TG) { try { TG.ready(); TG.expand(); } catch {} }
  let restored = false;
  try {
    const response = await fetch("/api/me", { method:"GET", credentials:"same-origin", headers:{ "Accept":"application/json" } });
    if (response.ok) {
      const data = await response.json();
      if (data.authenticated && data.user) {
        s.authenticated=true; s.preview=false; s.user=data.user; restored=true;
        if (data.user.language && data.user.theme) { s.language=data.user.language; s.theme=data.user.theme; s.step="app"; }
      }
    }
  } catch {}
  if (!restored && TG && TG.initData) {
    try {
      const data = await request("/api/auth/telegram",{initData:TG.initData});
      s.authenticated=true; s.preview=false; s.user=data.user;
      if (data.user && data.user.language && data.user.theme) { s.language=data.user.language; s.theme=data.user.theme; s.step="app"; }
    } catch (error) {
      s.preview=true;
      const saved=localPrefs();
      if(saved){s.language=saved.language;s.theme=saved.theme;s.step="app";}
    }
  } else if (!restored) {
    const saved=localPrefs();
    if(saved){s.language=saved.language;s.theme=saved.theme;s.step="app";}
  }
  themeApply(); render(); setupTonConnect();
}
function welcome() {
  root.innerHTML='<main class="onboard welcome"><header class="top">'+brand()+'<span class="step">01 / 03</span></header><section class="welcome-card"><div class="hero-icon">'+svg("wallet")+'</div><span class="eyebrow">PAIDMX REWARDS</span><h1>'+tr("welcome")+'<br><em>PaidMX</em></h1><p class="tagline">'+tr("tagline")+'</p><p class="muted intro">'+tr("intro")+'</p><div class="feature-pills"><span>'+svg("tasks")+tr("tasks")+'</span><span>'+svg("arena")+tr("arena")+'</span><span>'+svg("wallet")+tr("wallet")+'</span></div><button class="primary wide" data-action="start">'+tr("start")+svg("arrow")+'</button><p class="fine">Telegram Mini App · @PaidMX_bot</p></section><div class="progress"><i class="on"></i><i></i><i></i></div></main>';
}
function languages() {
  const cards=LANGS.map(function(x){return '<button class="language '+(s.language===x[0]?'chosen':'')+'" data-language="'+x[0]+'"><span class="flag">'+x[1]+'</span><b>'+safe(x[2])+'</b><i>'+ (s.language===x[0]?svg("check"):"") +'</i></button>';}).join("");
  root.innerHTML='<main class="onboard selector"><header class="top">'+brand()+'<button class="icon-button" data-action="welcome">'+svg("close")+'</button></header><div class="heading"><span class="kicker">STEP 02 / 03</span><h1>'+tr("language")+'</h1><p>'+tr("languageNote")+'</p></div><section class="language-grid">'+cards+'</section><footer class="sticky"><button class="primary wide" data-action="language-next">'+tr("continue")+svg("arrow")+'</button><p class="fine">9 LANGUAGES · GLOBAL COMMUNITY</p></footer></main>';
}
function themes() {
  const cards=THEMES.map(function(x){const colors=x[3].map(function(c){return '<i style="background:'+c+'"></i>';}).join("");return '<button class="theme-card '+(s.theme===x[0]?'chosen':'')+'" data-theme-choice="'+x[0]+'"><div class="theme-preview p-'+x[0]+'"><i></i><b></b><em></em><small></small></div><div class="theme-info"><strong>'+x[1]+'</strong><span>'+x[2]+'</span><div class="swatches">'+colors+'</div></div><span class="check">'+(s.theme===x[0]?svg("check"):"")+'</span></button>';}).join("");
  root.innerHTML='<main class="onboard selector"><header class="top">'+brand()+'<button class="text-button" data-action="back-language">'+tr("back")+'</button></header><div class="heading"><span class="kicker">STEP 03 / 03</span><h1>'+tr("theme")+'</h1><p>'+tr("themeNote")+'</p></div><section class="theme-grid">'+cards+'</section><footer class="sticky"><button class="primary wide" data-action="enter">'+tr("enter")+svg("arrow")+'</button><p class="fine">YOUR STYLE. YOUR PAIDMX.</p></footer></main>';
}
function homePage() {
  const points=Number((s.user&&s.user.points)||0).toLocaleString();
  return '<section class="page home-page"><div class="profile"><div class="avatar">P<span>MX</span></div><div class="profile-info"><small>'+tr("welcome")+'</small><b>'+safe((s.user&&s.user.firstName)||tr("member"))+'</b><span>Starter</span></div><button class="circle" data-action="settings">'+svg("settings")+'</button></div>'+
  '<article class="balance"><div class="balance-top"><small>'+tr("total")+'</small><span class="gain">• '+tr("live")+' +0</span></div><div class="amount"><i>✦</i><strong>'+points+'</strong><small>'+tr("points")+'</small></div><p>≈ $'+Number((s.user&&s.user.usdtBalance)||0).toFixed(4)+' <span>· USDT</span></p><div class="chart"><div></div><span>Mon</span><span>Tue</span><span>Wed</span><span>Thu</span><span>Fri</span><span>'+tr("home")+'</span></div><div class="balance-actions"><button data-page="wallet">'+svg("tasks")+tr("convert")+'</button><button class="invert" data-page="wallet">'+svg("wallet")+tr("withdraw")+'</button></div></article>'+
  '<article class="surface checkin"><div class="row-between"><div><h2>'+tr("daily")+'</h2><p>✦ 1 '+tr("streak")+'</p></div><span class="timer">24H</span></div><div class="days"><span>✓<b>100</b></span><span>02<b>100</b></span><span>03<b>175</b></span><span>04<b>250</b></span><span>05<b>300</b></span><span>06<b>400</b></span><span>✧<b>750</b></span></div><small class="subtle">Daily rewards are not enabled yet.</small></article>'+
  '<button class="promo" data-action="promo"><span>'+svg("ticket")+'</span><b>'+tr("promo")+'</b>'+svg("arrow")+'</button>'+
  '<div class="quick-grid"><button data-page="arena"><i>'+svg("sun")+'</i><b>'+tr("spin")+'</b><small>'+tr("soon")+'</small></button><button data-page="arena"><i>'+svg("arena")+'</i><b>'+tr("play")+'</b><small>'+tr("arena")+'</small></button><button data-action="promo"><i>'+svg("ticket")+'</i><b>'+tr("redeem")+'</b><small>'+tr("promo")+'</small></button><button data-page="invites"><i>'+svg("users")+'</i><b>'+tr("invite")+'</b><small>'+tr("invite")+'</small></button></div>'+
  '<div class="activity"><i></i><b>'+tr("live")+'</b><span>PaidMX</span><small>'+tr("noRewards")+'</small></div><div class="row-between task-title"><div><h2>'+tr("openTasks")+'</h2><p>'+tr("soon")+'</p></div><button data-page="tasks">'+tr("allTasks")+svg("arrow")+'</button></div>'+
  '<article class="task"><div class="provider">P</div><div><b>'+tr("ad")+'</b><p>'+tr("adNote")+'</p><small>0 rewards issued</small></div><button data-page="tasks">'+tr("watch")+'</button></article><p class="disclaimer">'+tr("preview")+' · '+tr("adNote")+'</p></section>';
}
function subPage() {
  if(s.page==="home") return homePage();
  if(s.page==="tasks") return '<section class="page subpage"><div class="title-row">'+svg("tasks")+'<div><h1>'+tr("tasks")+'</h1><p>'+tr("allTasks")+'</p></div></div><article class="empty"><i>'+svg("tasks")+'</i><h2>'+tr("noRewards")+'</h2><p>'+tr("adNote")+'</p><span>'+tr("soon")+'</span></article></section>';
  if(s.page==="arena") return '<section class="page subpage"><div class="title-row">'+svg("arena")+'<div><h1>'+tr("arena")+'</h1><p>'+tr("arenaNote")+'</p></div></div><article class="arcade"><small>PAIDMX ARCADE</small><h2>'+tr("spin")+' &amp; '+tr("play")+'</h2><div class="wheel">✦</div><p>'+tr("arenaNote")+'</p><span>'+tr("soon")+'</span></article></section>';
  if(s.page==="invites") return '<section class="page subpage"><div class="title-row">'+svg("users")+'<div><h1>'+tr("inviteTitle")+'</h1><p>'+tr("inviteNote")+'</p></div></div><article class="invite-card"><i>'+svg("users")+'</i><h2>'+tr("inviteTitle")+'</h2><p>'+tr("inviteNote")+'</p><div class="copy-row"><span>https://t.me/'+BOT+'?start=ref</span><button data-action="copy">'+tr("copy")+'</button></div><small>Referral rewards are not configured yet.</small></article></section>';
  return '<section class="page subpage"><div class="title-row">'+svg("wallet")+'<div><h1>'+tr("wallet")+'</h1><p>'+tr("walletNote")+'</p></div></div><article class="wallet-card"><small>'+tr("total")+'</small><strong>
}
function settingsModal() {
  return s.settings?'<div class="scrim" data-action="close-settings"><section class="modal" data-modal><div class="row-between"><h2>'+tr("settings")+'</h2><button class="icon-button" data-action="close-settings">'+svg("close")+'</button></div><button class="setting-row" data-action="change-language">'+svg("tasks")+'<b>'+tr("changeLanguage")+'</b>'+svg("arrow")+'</button><button class="setting-row" data-action="change-theme">'+svg("sun")+'<b>'+tr("changeTheme")+'</b>'+svg("arrow")+'</button><small>@PaidMX_bot</small></section></div>':'';
}
function render() {
  themeApply();
  if(s.step==="welcome") return welcome();
  if(s.step==="language") return languages();
  if(s.step==="theme") return themes();
  const nav=[["home","home"],["tasks","tasks"],["arena","arena"],["invites","invites"],["wallet","wallet"]];
  const navHtml=nav.map(function(x){return '<button class="nav-item '+(s.page===x[0]?'active':'')+'" data-page="'+x[0]+'">'+svg(x[0]==="invites"?"users":x[0])+'<span>'+tr(x[1])+'</span></button>';}).join("");
  root.innerHTML='<main class="dashboard"><header class="dashboard-header">'+brand()+'<button class="points-chip" data-page="wallet">✦ '+Number((s.user&&s.user.points)||0).toLocaleString()+'</button></header>'+subPage()+'<nav class="bottom-nav">'+navHtml+'</nav>'+settingsModal()+'</main>';
}
function setupTonConnect() {
  if (s.tonUI || !window.TON_CONNECT_UI || !window.TON_CONNECT_UI.TonConnectUI) return;
  try {
    s.tonUI = new window.TON_CONNECT_UI.TonConnectUI({ manifestUrl: location.origin + "/api/tonconnect-manifest" });
    s.tonUI.onStatusChange(function(wallet) {
      s.wallet = wallet || null;
      if (s.page === "wallet" && s.step === "app") render();
    });
  } catch (error) { console.warn("TON Connect unavailable", error); }
}
async function finish() {
  saveLocal();
  if(s.authenticated) {
    try { await request("/api/preferences",{language:s.language,theme:s.theme}); }
    catch(error) { toast(tr("error")); return; }
  }
  s.step="app"; s.page="home"; render();
}
root.addEventListener("click",async function(event){
  const el=event.target.closest("button,[data-action]");
  if(!el) return;
  if(el.dataset.language){s.language=el.dataset.language;render();return;}
  if(el.dataset.themeChoice){s.theme=el.dataset.themeChoice;render();return;}
  if(el.dataset.page){s.page=el.dataset.page;s.settings=false;render();return;}
  const action=el.dataset.action;
  if(action==="start"){s.step="language";render();}
  else if(action==="welcome"){s.step="welcome";render();}
  else if(action==="language-next"){s.step="theme";render();}
  else if(action==="back-language"){s.step="language";render();}
  else if(action==="enter"){await finish();}
  else if(action==="settings"){s.settings=true;render();}
  else if(action==="close-settings"){s.settings=false;render();}
  else if(action==="change-language"){s.settings=false;s.step="language";render();}
  else if(action==="change-theme"){s.settings=false;s.step="theme";render();}
  else if(action==="ton-connect"){if(!s.tonUI){setupTonConnect();}if(s.tonUI){try{await s.tonUI.openModal();}catch{toast("TON Connect could not open. Check the app manifest and deployment URL.");}}else{toast("TON Connect SDK is still loading.");}}
  else if(action==="promo"){toast(tr("promoNote"));}
  else if(action==="copy"){try{await navigator.clipboard.writeText("https://t.me/"+BOT+"?start=ref");toast(tr("copied"));}catch{toast("https://t.me/"+BOT+"?start=ref");}}
});
function toast(message){let n=document.getElementById("toast");if(!n){n=document.createElement("div");n.id="toast";n.className="toast floating";document.body.appendChild(n);}n.textContent=message;n.classList.add("show");clearTimeout(toast.timer);toast.timer=setTimeout(function(){n.classList.remove("show");},2600);}
init();
+Number((s.user&&s.user.usdtBalance)||0).toFixed(4)+'</strong><hr><span>'+tr("points")+'</span><b>'+Number((s.user&&s.user.points)||0).toLocaleString()+'</b></article><article class="surface ton-wallet"><div class="ton-badge">TON</div><h2>TON Connect</h2><p>'+(s.wallet&&s.wallet.account?'Connected: '+safe(s.wallet.account.address.slice(0,8))+'…'+safe(s.wallet.account.address.slice(-6)):'Connect Tonkeeper or another TON wallet.')+'</p><button class="primary wide" data-action="ton-connect">'+(s.wallet&&s.wallet.account?'Manage connected wallet':'Connect TON wallet')+'</button><small class="subtle">Wallet connection only. Payouts stay disabled until wallet-proof verification and payout rules are implemented.</small></article><article class="empty"><i>'+svg("wallet")+'</i><h2>'+tr("withdraw")+'</h2><p>'+tr("withdrawNote")+'</p><span>'+tr("soon")+'</span></article></section>';
}
function settingsModal() {
  return s.settings?'<div class="scrim" data-action="close-settings"><section class="modal" data-modal><div class="row-between"><h2>'+tr("settings")+'</h2><button class="icon-button" data-action="close-settings">'+svg("close")+'</button></div><button class="setting-row" data-action="change-language">'+svg("tasks")+'<b>'+tr("changeLanguage")+'</b>'+svg("arrow")+'</button><button class="setting-row" data-action="change-theme">'+svg("sun")+'<b>'+tr("changeTheme")+'</b>'+svg("arrow")+'</button><small>@PaidMX_bot</small></section></div>':'';
}
function render() {
  themeApply();
  if(s.step==="welcome") return welcome();
  if(s.step==="language") return languages();
  if(s.step==="theme") return themes();
  const nav=[["home","home"],["tasks","tasks"],["arena","arena"],["invites","invites"],["wallet","wallet"]];
  const navHtml=nav.map(function(x){return '<button class="nav-item '+(s.page===x[0]?'active':'')+'" data-page="'+x[0]+'">'+svg(x[0]==="invites"?"users":x[0])+'<span>'+tr(x[1])+'</span></button>';}).join("");
  root.innerHTML='<main class="dashboard"><header class="dashboard-header">'+brand()+'<button class="points-chip" data-page="wallet">✦ '+Number((s.user&&s.user.points)||0).toLocaleString()+'</button></header>'+subPage()+'<nav class="bottom-nav">'+navHtml+'</nav>'+settingsModal()+'</main>';
}
async function finish() {
  saveLocal();
  if(s.authenticated) {
    try { await request("/api/preferences",{language:s.language,theme:s.theme}); }
    catch(error) { toast(tr("error")); return; }
  }
  s.step="app"; s.page="home"; render();
}
root.addEventListener("click",async function(event){
  const el=event.target.closest("button,[data-action]");
  if(!el) return;
  if(el.dataset.language){s.language=el.dataset.language;render();return;}
  if(el.dataset.themeChoice){s.theme=el.dataset.themeChoice;render();return;}
  if(el.dataset.page){s.page=el.dataset.page;s.settings=false;render();return;}
  const action=el.dataset.action;
  if(action==="start"){s.step="language";render();}
  else if(action==="welcome"){s.step="welcome";render();}
  else if(action==="language-next"){s.step="theme";render();}
  else if(action==="back-language"){s.step="language";render();}
  else if(action==="enter"){await finish();}
  else if(action==="settings"){s.settings=true;render();}
  else if(action==="close-settings"){s.settings=false;render();}
  else if(action==="change-language"){s.settings=false;s.step="language";render();}
  else if(action==="change-theme"){s.settings=false;s.step="theme";render();}
  else if(action==="promo"){toast(tr("promoNote"));}
  else if(action==="copy"){try{await navigator.clipboard.writeText("https://t.me/"+BOT+"?start=ref");toast(tr("copied"));}catch{toast("https://t.me/"+BOT+"?start=ref");}}
});
function toast(message){let n=document.getElementById("toast");if(!n){n=document.createElement("div");n.id="toast";n.className="toast floating";document.body.appendChild(n);}n.textContent=message;n.classList.add("show");clearTimeout(toast.timer);toast.timer=setTimeout(function(){n.classList.remove("show");},2600);}
init();
