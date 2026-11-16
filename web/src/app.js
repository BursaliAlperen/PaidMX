import { initTelegram, getInitData } from "./services/telegram.js";
import { refreshDashboard } from "./store.js";
import { initRouter } from "./router.js";
import { getLang } from "./i18n.js";
import { h } from "./utils/dom.js";

const cfg = window.PAIDMX_CONFIG || {};

function showAuth(message) {
  const screen = document.getElementById("auth-screen");
  screen.classList.remove("hidden");
  const bot = String(cfg.botUsername || "").replace(/^@/, "");
  const botLink = bot
    ? h("a", { class: "btn btn-primary", href: "https://t.me/" + encodeURIComponent(bot), target: "_blank", rel: "noopener noreferrer" }, "↗ Telegram'da aç")
    : null;
  screen.replaceChildren(
    h("span", { class: "brand-mark" }, "P"),
    h("h2", {}, "PaidMX"),
    h("p", {}, message || "Uygulamayı Telegram botunun Mini App butonundan açmalısın."),
    botLink
  );
}

async function boot() {
  if (!getInitData()) {
    showAuth();
    return;
  }
  initTelegram();
  document.documentElement.lang = getLang();
  try {
    await refreshDashboard();
    initRouter();
  } catch (e) {
    showAuth(e.message);
  }
}

boot();
