(() => {
  "use strict";
  const config = window.PAIDMX_CONFIG || {};
  const tg = window.Telegram?.WebApp;
  const $ = (id) => document.getElementById(id);
  let dashboard = null;
  let toastTimer = null;

  if (tg) {
    tg.ready();
    tg.expand();
    try { tg.setHeaderColor("#0b1020"); tg.setBackgroundColor("#0b1020"); } catch (_) {}
  }

  function toast(message) {
    const node = $("toast");
    node.textContent = message;
    node.classList.add("show");
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => node.classList.remove("show"), 2400);
    try { tg?.HapticFeedback?.notificationOccurred("success"); } catch (_) {}
  }

  function showAuthError(message) {
    $("auth-error-text").textContent = message;
    $("auth-error").classList.remove("hidden");
    const bot = String(config.botUsername || "").replace(/^@/, "");
    if (bot) {
      $("open-bot").href = "https://t.me/" + encodeURIComponent(bot);
      $("open-bot").classList.remove("hidden");
    }
  }

  async function rpc(method) {
    if (!config.apiUrl) throw new Error("API adresi yapılandırılmamış.");
    const initData = tg?.initData || "";
    if (!initData) throw new Error("Telegram Mini App oturumu bulunamadı. Uygulamayı botun içinden aç.");
    const response = await fetch(config.apiUrl, {
      method: "POST",
      headers: { "Content-Type": "application/json", "X-Telegram-Init-Data": initData },
      body: JSON.stringify({ rpc: method })
    });
    let data;
    try { data = await response.json(); } catch (_) { throw new Error("Sunucudan geçersiz yanıt alındı."); }
    if (!response.ok || !data.ok) {
      const errors = {
        telegram_auth_expired: "Telegram oturumunun süresi dolmuş. Mini App'i kapatıp tekrar aç.",
        telegram_auth_invalid: "Telegram doğrulaması başarısız. Lütfen yeniden giriş yap.",
        user_banned: "Bu hesap için erişim kapatılmış."
      };
      throw new Error(errors[data.error] || "Sunucu isteği başarısız (" + response.status + ").");
    }
    return data;
  }

  function pmx(micros) {
    const value = Number(micros || 0) / 1000000;
    return value.toLocaleString("tr-TR", { minimumFractionDigits: 0, maximumFractionDigits: 6 });
  }

  function render(data) {
    dashboard = data;
    const user = data.user || {};
    const wallet = data.wallet || {};
    const name = user.firstName || user.username || "PaidMX üyesi";
    $("first-name").textContent = name;
    $("avatar").textContent = (name.trim()[0] || "P").toUpperCase();
    if (user.photoUrl) $("avatar").style.backgroundImage = "url('" + user.photoUrl.replace(/['()\\]/g, "") + "')";
    $("balance").innerHTML = pmx(wallet.balanceMicros) + " <small>PMX</small>";
    $("wallet-balance").textContent = pmx(wallet.balanceMicros) + " PMX";
    $("wallet-debt").textContent = pmx(wallet.debtMicros) + " PMX";
    $("debt-label").textContent = Number(wallet.debtMicros || 0) > 0 ? "Borç: " + pmx(wallet.debtMicros) + " PMX" : "";
    $("ref-count").textContent = Number(user.referralCount || 0).toLocaleString("tr-TR");
    $("invite-total").textContent = Number(user.referralCount || 0).toLocaleString("tr-TR");
    $("ref-earnings").textContent = pmx(user.referralEarningsMicros) + " PMX";
    $("invite-earned").textContent = pmx(user.referralEarningsMicros) + " PMX";
    if (data.admin) $("admin-pill").classList.remove("hidden");

    const bot = String(config.botUsername || "").replace(/^@/, "");
    const code = String(user.referralCode || "");
    const link = bot && code ? "https://t.me/" + encodeURIComponent(bot) + "?startapp=ref_" + encodeURIComponent(code) : "";
    $("ref-link").textContent = link || "Bot kullanıcı adı config.js dosyasına eklenmeli.";
    $("copy-ref").disabled = !link;
    $("share-ref").disabled = !link;
    $("copy-ref").dataset.link = link;
    $("share-ref").dataset.link = link;
  }

  function switchTab(tab) {
    ["home", "tasks", "invite", "wallet"].forEach(name => {
      const panel = $(name + "-panel");
      if (panel) panel.classList.toggle("hidden", name !== tab);
    });
    document.querySelectorAll(".nav-item").forEach(button => button.classList.toggle("active", button.dataset.tab === tab));
    try { tg?.HapticFeedback?.selectionChanged(); } catch (_) {}
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  document.querySelectorAll("[data-tab]").forEach(button => button.addEventListener("click", () => switchTab(button.dataset.tab)));
  $("copy-ref").addEventListener("click", async () => {
    const link = $("copy-ref").dataset.link;
    if (!link) return;
    try {
      if (navigator.clipboard?.writeText) await navigator.clipboard.writeText(link);
      else if (tg?.shareUrl) { tg.shareUrl(link); return; }
      else throw new Error("copy");
      toast("Davet bağlantısı kopyalandı.");
    } catch (_) { toast("Bağlantı kopyalanamadı; uzun basarak seçebilirsin."); }
  });
  $("share-ref").addEventListener("click", () => {
    const link = $("share-ref").dataset.link;
    if (!link) return;
    const text = "PaidMX'e katıl, görevleri keşfet ve birlikte büyüyelim!";
    const shareUrl = "https://t.me/share/url?url=" + encodeURIComponent(link) + "&text=" + encodeURIComponent(text);
    if (tg?.openTelegramLink) tg.openTelegramLink(shareUrl);
    else window.open(shareUrl, "_blank", "noopener,noreferrer");
  });

  async function boot() {
    if (!tg?.initData) {
      showAuthError("Bu arayüz Telegram Mini App olarak açılmalıdır. Botun menüsündeki uygulama butonunu kullan.");
      return;
    }
    try {
      const data = await rpc("getDashboard");
      render(data);
    } catch (error) {
      showAuthError(error.message || "PaidMX API bağlantısı kurulamadı.");
    }
  }

  boot();
})();
