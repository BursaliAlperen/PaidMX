import { h, clear } from "../utils/dom.js";
import { t, getLang, setLang } from "../i18n.js";
import { savePreferences } from "../store.js";
import { requestReload } from "../nav.js";
import { toast } from "../components/ui.js";

export function renderSettings(container) {
  clear(container);

  container.append(
    h("div", { class: "page-heading" },
      h("span", { class: "kicker" }, "PREFERENCES"),
      h("h1", {}, t("settings")),
      h("p", {}, t("aboutText"))
    )
  );

  const panel = h("div", { class: "info-list" });

  // Language
  const langSeg = h("div", { class: "seg" },
    h("button", { class: getLang() === "tr" ? "active" : "", onclick: () => changeLang("tr") }, "Türkçe"),
    h("button", { class: getLang() === "en" ? "active" : "", onclick: () => changeLang("en") }, "English")
  );
  panel.append(settingRow(t("language"), t("language") + " (LNG)", langSeg));

  // Theme
  const themeSwitch = h("button", { class: "switch on" });
  panel.append(settingRow(t("theme"), t("darkTheme"), themeSwitch));

  // Notifications
  const notifSwitch = h("button", { class: "switch on" });
  notifSwitch.addEventListener("click", () => notifSwitch.classList.toggle("on"));
  panel.append(settingRow(t("notificationsPref"), "", notifSwitch));

  // Links
  panel.append(
    linkRow(t("privacyPolicy"), "https://t.me/paidmx"),
    linkRow(t("terms"), "https://t.me/paidmx"),
    linkRow(t("support"), "https://t.me/paidmx"),
    h("div", { class: "setting-row" },
      h("div", { class: "setting-label" }, h("b", {}, t("about")), h("span", {}, t("aboutText")))
    )
  );

  container.append(panel);

  function changeLang(lang) {
    if (lang === getLang()) return;
    setLang(lang);
    savePreferences(lang).catch(() => {});
    toast(t("copied"));
    requestReload();
  }
}

function settingRow(label, sub, control) {
  return h("div", { class: "setting-row" },
    h("div", { class: "setting-label" }, h("b", {}, label), sub ? h("span", {}, sub) : null),
    control
  );
}

function linkRow(label, href) {
  return h("a", { class: "setting-row", href, target: "_blank", rel: "noopener noreferrer" },
    h("div", { class: "setting-label" }, h("b", {}, label)),
    h("span", { style: { color: "var(--primary)" } }, "↗")
  );
}
