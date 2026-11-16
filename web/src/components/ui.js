import { h, clear } from "../utils/dom.js";
import { t } from "../i18n.js";
import { haptic } from "../services/telegram.js";

/* ---------------- Toast ---------------- */
let toastTimer = null;

export function toast(message, type = "success") {
  const root = document.getElementById("toast-root");
  if (!root) return;
  clear(root);
  const node = h("div", { class: "toast", html: message });
  root.append(node);
  requestAnimationFrame(() => node.classList.add("show"));
  if (type === "success") haptic("success");
  else if (type === "error") haptic("error");
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => {
    node.classList.remove("show");
    setTimeout(() => node.remove(), 300);
  }, 2300);
}

/* ---------------- Modal ---------------- */
export function openModal({ title, body, footer, onClose }) {
  const root = document.getElementById("modal-root");
  const backdrop = h("div", { class: "modal-backdrop" });
  const closeBtn = h("button", {
    class: "modal-close",
    "aria-label": t("close"),
    onclick: close
  }, "✕");

  const head = h("div", { class: "modal-head" }, h("h3", {}, title), closeBtn);
  const panel = h("div", { class: "modal-panel" }, head, h("div", { class: "modal-body" }, body));
  if (footer) panel.append(h("div", { class: "modal-foot" }, footer));
  const wrap = h("div", { class: "modal-root" }, backdrop, panel);

  function close() {
    wrap.classList.remove("open");
    onClose?.();
    setTimeout(() => wrap.remove(), 200);
  }

  backdrop.addEventListener("click", close);
  closeBtn.addEventListener("click", close);
  root.append(wrap);
  requestAnimationFrame(() => wrap.classList.add("open"));
  return close;
}

/* ---------------- States ---------------- */
export function emptyState(icon, title, sub) {
  return h("div", { class: "state-box" },
    h("div", { class: "state-ic" }, icon),
    h("b", {}, title),
    sub ? h("p", {}, sub) : null
  );
}

export function errorState(message, onRetry) {
  const retryBtn = onRetry
    ? h("button", { class: "btn btn-ghost btn-sm", onclick: onRetry }, "↻ " + t("retry"))
    : null;
  return h("div", { class: "state-box" },
    h("div", { class: "state-ic" }, "⚠️"),
    h("b", {}, t("error")),
    h("p", {}, message || t("error")),
    retryBtn
  );
}

export function loadingSkeleton(count = 3) {
  const cards = Array.from({ length: count }, () => h("div", { class: "skeleton skeleton-card" }));
  return h("div", { class: "task-list" }, cards);
}

export function statCard(iconClass, icon, label, value) {
  return h("article", { class: "stat-card" },
    h("span", { class: "stat-ic " + iconClass }, icon),
    h("div", {}, h("small", {}, label), h("strong", {}, value))
  );
}
