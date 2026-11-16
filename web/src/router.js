import { h, clear } from "./utils/dom.js";
import { t } from "./i18n.js";
import { onNavigate, onReload } from "./nav.js";
import { getState, subscribe } from "./store.js";
import { renderHome } from "./pages/HomePage.js";
import { renderTasks } from "./pages/TasksPage.js";
import { renderFaucet } from "./pages/FaucetPage.js";
import { renderVideoAds } from "./pages/VideoAdsPage.js";
import { renderPtcAds } from "./pages/PtcAdsPage.js";
import { renderShortlinks } from "./pages/ShortlinksPage.js";
import { renderReferrals } from "./pages/ReferralsPage.js";
import { renderWallet } from "./pages/WalletPage.js";
import { renderProfile } from "./pages/ProfilePage.js";
import { renderSettings } from "./pages/SettingsPage.js";
import { renderAdmin } from "./pages/AdminPage.js";

const PAGES = {
  home: { label: () => t("home"), icon: "⌂", mobile: true, sidebar: true },
  tasks: { label: () => t("taskCenter"), icon: "▤", mobile: true, sidebar: true },
  faucet: { label: () => t("faucet"), icon: "💧", mobile: true, sidebar: true },
  video: { label: () => t("video"), icon: "▶", mobile: false, sidebar: true },
  ptc: { label: () => t("ptc"), icon: "◉", mobile: false, sidebar: true },
  shortlinks: { label: () => t("shortlinks"), icon: "↗", mobile: false, sidebar: true },
  referrals: { label: () => t("referrals"), icon: "♧", mobile: true, sidebar: true },
  wallet: { label: () => t("wallet"), icon: "◈", mobile: true, sidebar: true },
  profile: { label: () => t("profile"), icon: "👤", mobile: false, sidebar: true },
  settings: { label: () => t("settings"), icon: "⚙", mobile: false, sidebar: true },
  admin: { label: () => t("admin"), icon: "🛡", mobile: false, sidebar: true }
};

const RENDERERS = {
  home: renderHome,
  tasks: renderTasks,
  faucet: renderFaucet,
  video: renderVideoAds,
  ptc: renderPtcAds,
  shortlinks: renderShortlinks,
  referrals: renderReferrals,
  wallet: renderWallet,
  profile: renderProfile,
  settings: renderSettings,
  admin: renderAdmin
};

let currentPage = "home";
let sidebarNav, mobileNav, headerTitle, headerCrumb, sidebarFoot;

export function initRouter() {
  const sidebar = document.getElementById("sidebar");
  const header = document.getElementById("header");
  const mobileNav = document.getElementById("mobile-nav");
  const view = document.getElementById("view");

  // Sidebar
  const brand = h("div", { class: "sidebar-brand" },
    h("span", { class: "brand-mark" }, "P"),
    h("span", { class: "brand-name" }, "PAID", h("em", {}, "MX"))
  );
  sidebarNav = h("nav", { class: "sidebar-nav" });
  sidebarFoot = h("div", { class: "sidebar-foot" });
  sidebar.append(brand, sidebarNav, sidebarFoot);

  // Mobile nav
  const mobInner = h("div", { class: "mobile-nav-inner" });
  mobileNav.append(mobInner);
  mobileNav = mobInner;

  // Header
  headerTitle = h("div", { class: "header-title" }, h("b", {}), h("span", {}));
  headerCrumb = headerTitle.querySelector("span");
  const headerActions = h("div", { class: "header-actions" },
    h("button", { class: "icon-btn", "aria-label": t("notifications") }, "🔔"),
    h("button", { class: "header-profile", onclick: () => go("profile") },
      h("span", { class: "avatar", id: "header-avatar" }, "P"),
      h("b", { id: "header-name" }, "")
    )
  );
  header.append(headerTitle, h("div", { class: "header-spacer" }), headerActions);

  buildSidebar();
  buildMobileNav();
  updateShellIdentity();

  onNavigate((name) => go(name));
  onReload(() => {
    buildSidebar();
    buildMobileNav();
    updateShellIdentity();
    go(currentPage);
  });
  subscribe(() => {
    buildSidebar();
    updateShellIdentity();
  });

  go("home");
}

function buildSidebar() {
  clear(sidebarNav);
  const admin = getState().admin;
  const items = ["home", "tasks", "faucet", "video", "ptc", "shortlinks", "referrals", "wallet"];
  const group2 = ["profile", "settings"];
  const group3 = admin ? ["admin"] : [];

  for (const key of items) {
    const p = PAGES[key];
    sidebarNav.append(sideLink(key, p));
  }
  sidebarNav.append(h("div", { class: "nav-label" }, t("account")));
  for (const key of group2) {
    const p = PAGES[key];
    sidebarNav.append(sideLink(key, p));
  }
  if (group3.length) {
    sidebarNav.append(h("div", { class: "nav-label" }, t("admin")));
    for (const key of group3) sidebarNav.append(sideLink(key, PAGES[key]));
  }
}

function sideLink(key, p) {
  const link = h("button", {
    class: "side-link" + (currentPage === key ? " active" : ""),
    onclick: () => go(key)
  }, h("span", { class: "nav-ic" }, p.icon), p.label());
  return link;
}

function buildMobileNav() {
  clear(mobileNav);
  for (const key of ["home", "tasks", "faucet", "referrals", "wallet"]) {
    const p = PAGES[key];
    const link = h("button", {
      class: "mob-link" + (currentPage === key ? " active" : ""),
      onclick: () => go(key)
    }, h("span", { class: "nav-ic" }, p.icon), p.label());
    mobileNav.append(link);
  }
}

function updateShellIdentity() {
  const state = getState();
  const name = state.user.firstName || state.user.username || "PaidMX";
  const avatar = document.getElementById("header-avatar");
  const nameEl = document.getElementById("header-name");
  if (avatar) {
    avatar.textContent = (name[0] || "P").toUpperCase();
    if (state.user.photoUrl) avatar.style.backgroundImage = "url('" + state.user.photoUrl.replace(/['()\\]/g, "") + "')";
  }
  if (nameEl) nameEl.textContent = name;
  if (sidebarFoot) {
    clear(sidebarFoot);
    const footAvatar = h("div", { class: "avatar" }, (name[0] || "P").toUpperCase());
    if (state.user.photoUrl) footAvatar.style.backgroundImage = "url('" + state.user.photoUrl.replace(/['()\\]/g, "") + "')";
    sidebarFoot.append(footAvatar,
      h("div", { class: "side-user" }, h("b", {}, name), h("span", {}, state.user.username ? "@" + state.user.username : "Telegram"))
    );
  }
}

function go(name) {
  if (!RENDERERS[name]) name = "home";
  currentPage = name;
  const p = PAGES[name];

  // Update active states
  document.querySelectorAll(".side-link").forEach(el => el.classList.toggle("active", el.textContent.trim() === p.label()));
  document.querySelectorAll(".mob-link").forEach(el => el.classList.toggle("active", el.textContent.trim() === p.label()));

  headerTitle.querySelector("b").textContent = p.label();
  headerCrumb.textContent = "PaidMX / " + p.label();

  const view = document.getElementById("view");
  clear(view);
  const wrap = h("div", { class: "page-enter" });
  view.append(wrap);
  RENDERERS[name](wrap);
  window.scrollTo({ top: 0 });
}
