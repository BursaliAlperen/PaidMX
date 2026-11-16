import { h, clear } from "../utils/dom.js";
import { t } from "../i18n.js";
import { getState, loadReferrals } from "../store.js";
import { toast, emptyState } from "../components/ui.js";
import { copyText, shareLink, haptic } from "../services/telegram.js";
import { fmtBalance, fmtDate } from "../utils/format.js";

export function renderReferrals(container) {
  clear(container);
  const cfg = window.PAIDMX_CONFIG || {};
  const bot = String(cfg.botUsername || "").replace(/^@/, "");

  container.append(
    h("div", { class: "page-heading" },
      h("span", { class: "kicker" }, "GROW"),
      h("h1", {}, t("referrals")),
      h("p", {}, t("referralNote"))
    )
  );

  const heroHost = h("div", {});
  const listHost = h("div", { class: "section-gap" });
  container.append(heroHost, listHost);

  function renderHero() {
    clear(heroHost);
    const state = getState();
    const code = String(state.user.referralCode || "");
    const link = bot && code ? "https://t.me/" + encodeURIComponent(bot) + "?startapp=ref_" + encodeURIComponent(code) : "";

    const linkBox = h("div", { class: "ref-link-box" },
      h("code", {}, link || "—"),
      h("button", {
        class: "btn btn-ghost btn-sm",
        disabled: !link ? "" : undefined,
        onclick: async () => {
          try { await copyText(link); toast(t("copied")); } catch { toast(t("copy") + " ✕", "error"); }
        }
      }, t("copy"))
    );

    const actions = h("div", { class: "ref-actions" },
      h("button", {
        class: "btn btn-primary",
        disabled: !link ? "" : undefined,
        onclick: () => { if (link) { shareLink(link, "PaidMX"); haptic("success"); } }
      }, "➤ " + t("shareTelegram"))
    );

    const stats = h("div", { class: "faucet-stats" },
      h("div", { class: "faucet-stat" }, h("span", {}, t("totalInvited")), h("b", {}, String(state.user.referralCount || 0))),
      h("div", { class: "faucet-stat" }, h("span", {}, t("referralEarnings")), h("b", {}, fmtBalance(state.user.referralEarningsMicros))),
      h("div", { class: "faucet-stat" }, h("span", {}, t("referralCode")), h("b", { style: { fontSize: "14px" } }, code || "—"))
    );

    heroHost.append(
      h("div", { class: "ref-hero" },
        h("span", { class: "kicker" }, "YOUR INVITE LINK"),
        h("div", { class: "ref-code" }, code || "—"),
        linkBox,
        actions,
        h("div", { style: { marginTop: "20px" } }, stats)
      )
    );
  }

  function renderList() {
    clear(listHost);
    const { referrals } = getState();
    listHost.append(h("div", { class: "section-title" }, h("h2", {}, t("referralHistory"))));
    const list = h("div", { class: "transaction-list" });
    listHost.append(list);
    if (!referrals.length) {
      list.append(emptyState("♧", t("emptyReferrals"), t("emptyReferralsSub")));
      return;
    }
    for (const r of referrals) {
      list.append(h("div", { class: "txn-item" },
        h("div", { class: "txn-ic neutral" }, "♧"),
        h("div", { class: "txn-body" },
          h("b", {}, r.firstName || r.username || r.referredUserId),
          h("span", {}, "@" + (r.username || r.referredUserId) + " · " + fmtDate(r.createdAt))
        )
      ));
    }
  }

  renderHero();
  renderList();
  loadReferrals().then(renderList).catch(() => {});
}
