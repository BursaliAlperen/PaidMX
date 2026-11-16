import { h, clear } from "../utils/dom.js";
import { t } from "../i18n.js";
import { getState } from "../store.js";
import { toast } from "../components/ui.js";
import { copyText } from "../services/telegram.js";
import { fmtDate } from "../utils/format.js";

export function renderProfile(container) {
  clear(container);
  const state = getState();
  const user = state.user || {};
  const name = user.firstName || user.username || "PaidMX";

  container.append(
    h("div", { class: "page-heading" },
      h("span", { class: "kicker" }, "ACCOUNT"),
      h("h1", {}, t("profile")),
      h("p", {}, t("accountInfo"))
    )
  );

  const avatar = h("div", { class: "avatar" }, (name[0] || "P").toUpperCase());
  if (user.photoUrl) avatar.style.backgroundImage = "url('" + user.photoUrl.replace(/['()\\]/g, "") + "')";

  container.append(
    h("div", { class: "profile-card" },
      avatar,
      h("div", {}, h("b", {}, name), h("span", {}, user.username ? "@" + user.username : "Telegram"))
    )
  );

  const info = h("div", { class: "info-list section-gap" });

  const codeRow = h("div", { class: "info-row" },
    h("span", {}, t("referralCode")),
    h("div", { style: { display: "flex", alignItems: "center", gap: "8px" } },
      h("b", {}, user.referralCode || "—"),
      h("button", {
        class: "copy-btn",
        onclick: async () => {
          try { await copyText(String(user.referralCode || "")); toast(t("copied")); }
          catch { toast(t("copy") + " ✕", "error"); }
        }
      }, t("copy"))
    )
  );

  info.append(
    h("div", { class: "info-row" }, h("span", {}, t("telegramId")), h("b", {}, user.id || "—")),
    codeRow,
    h("div", { class: "info-row" }, h("span", {}, t("registrationDate")), h("b", {}, fmtDate(user.createdAt))),
    h("div", { class: "info-row" }, h("span", {}, t("accountStatus")), h("span", { class: "badge" }, "● " + t("statusActive")))
  );

  container.append(info);
}
