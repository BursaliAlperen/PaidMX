import { h, clear } from "../utils/dom.js";
import { t } from "../i18n.js";
import { getState, loadFaucet, claimFaucet, refreshDashboard, loadTransactions } from "../store.js";
import { toast, emptyState, loadingSkeleton } from "../components/ui.js";
import { TransactionItem } from "../components/cards.js";
import { fmtBalance, fmtSeconds } from "../utils/format.js";

export function renderFaucet(container) {
  clear(container);
  let timer = null;

  container.append(
    h("div", { class: "page-heading" },
      h("span", { class: "kicker" }, "FAUCET"),
      h("h1", {}, t("faucet")),
      h("p", {}, t("faucetSub"))
    )
  );

  const cardHost = h("div", {});
  const historyHost = h("div", { class: "section-gap" });
  container.append(cardHost, historyHost);

  function renderCard() {
    clear(cardHost);
    if (timer) { clearInterval(timer); timer = null; }
    const faucet = getState().faucet;
    if (!faucet) {
      cardHost.append(loadingSkeleton(1));
      return;
    }

    const countdownNode = h("div", { class: "countdown" }, h("span", { class: "ic" }, "⏳"), fmtSeconds(faucet.secondsUntilClaim));
    const claimBtn = h("button", {
      class: "btn btn-primary btn-lg btn-block",
      disabled: !faucet.canClaim ? "" : undefined,
      onclick: doClaim
    }, t("claimNow"));

    const card = h("div", { class: "faucet-card" },
      h("span", { class: "kicker" }, "PMX " + t("claimReward")),
      h("div", { class: "faucet-amount" }, fmtBalance(faucet.rewardMicros).replace(" PMX", ""), h("small", {}, " PMX")),
      h("div", { class: "faucet-sub" }, t("faucetSub")),
      h("div", { style: { marginTop: "16px" } }, faucet.canClaim ? claimBtn : countdownNode),
      h("div", { class: "faucet-stats" },
        h("div", { class: "faucet-stat" }, h("span", {}, t("totalClaims")), h("b", {}, String(faucet.totalClaims))),
        h("div", { class: "faucet-stat" }, h("span", {}, t("totalEarned")), h("b", {}, fmtBalance(faucet.totalEarnedMicros))),
        h("div", { class: "faucet-stat" }, h("span", {}, t("claimCooldown")), h("b", {}, fmtSeconds(faucet.cooldownSeconds)))
      )
    );
    cardHost.append(card);

    if (!faucet.canClaim) {
      timer = setInterval(() => {
        const f = getState().faucet;
        if (!f) return;
        const remaining = Math.max(0, f.nextClaimAt - Math.floor(Date.now() / 1000));
        countdownNode.replaceChildren(h("span", { class: "ic" }, "⏳"), fmtSeconds(remaining));
        if (remaining <= 0) {
          clearInterval(timer);
          timer = null;
          renderCard();
        }
      }, 1000);
    }
  }

  async function doClaim() {
    try {
      await claimFaucet();
      await refreshDashboard();
      toast(t("claimSuccess"));
    } catch (e) {
      toast(e.message, "error");
    }
    renderCard();
    renderHistory();
  }

  function renderHistory() {
    clear(historyHost);
    const { transactions } = getState();
    const claims = transactions.filter(x => x.type === "faucet_claim");
    historyHost.append(h("div", { class: "section-title" }, h("h2", {}, t("claimHistory"))));
    const list = h("div", { class: "transaction-list" });
    historyHost.append(list);
    if (!claims.length) {
      list.append(emptyState("💧", t("emptyTx"), t("emptyTxSub")));
      return;
    }
    for (const c of claims.slice(0, 6)) list.append(TransactionItem(c));
  }

  renderCard();
  renderHistory();

  // Load faucet state + transactions.
  loadFaucet().then(() => { renderCard(); }).catch(() => {});
  loadTransactions(50).then(renderHistory).catch(() => {});
}
