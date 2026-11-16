import { h, clear } from "../utils/dom.js";
import { t } from "../i18n.js";
import { getState, loadTransactions } from "../store.js";
import { BalanceCard, TransactionItem } from "../components/cards.js";
import { emptyState, loadingSkeleton } from "../components/ui.js";

export function renderWallet(container) {
  clear(container);
  const state = getState();

  container.append(
    h("div", { class: "page-heading" },
      h("span", { class: "kicker" }, "YOUR MONEY"),
      h("h1", {}, t("wallet")),
      h("p", {}, t("walletSummary"))
    ),
    BalanceCard({ balanceMicros: state.wallet.balanceMicros, debtMicros: state.wallet.debtMicros })
  );

  // Withdrawals (honest "coming soon" state).
  const withdrawalCard = h("div", { class: "card section-gap" },
    h("div", { style: { display: "flex", alignItems: "center", gap: "12px" } },
      h("div", { class: "stat-ic amber" }, "⇄"),
      h("div", {}, h("b", { style: { fontSize: "15px" } }, t("withdrawals")), h("div", { class: "muted", style: { fontSize: "13px" } }, t("withdrawalsComingSoon")))
    )
  );
  container.append(withdrawalCard);

  const txHost = h("div", { class: "section-gap" });
  container.append(txHost);

  function renderTx() {
    clear(txHost);
    const { transactions } = getState();
    txHost.append(h("div", { class: "section-title" }, h("h2", {}, t("transactions"))));
    const list = h("div", { class: "transaction-list" });
    txHost.append(list);
    if (!transactions.length) {
      list.append(emptyState("📭", t("emptyTx"), t("emptyTxSub")));
      return;
    }
    for (const txn of transactions.slice(0, 50)) list.append(TransactionItem(txn));
  }

  renderTx();
  loadTransactions(50).then(renderTx).catch(() => {});
}
