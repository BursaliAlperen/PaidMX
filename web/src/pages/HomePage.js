import { h, clear } from "../utils/dom.js";
import { t } from "../i18n.js";
import { getState, loadTasks } from "../store.js";
import { navigate } from "../nav.js";
import { BalanceCard, taskCard } from "../components/cards.js";
import { emptyState, statCard, loadingSkeleton } from "../components/ui.js";
import { fmtBalance, fmtMicros } from "../utils/format.js";

export function renderHome(container) {
  clear(container);
  const state = getState();
  const name = state.user.firstName || state.user.username || "PaidMX";
  const stats = state.stats || {};

  container.append(
    h("div", { class: "page-heading" },
      h("span", { class: "kicker" }, "PAIDMX"),
      h("h1", {}, t("welcomeBack") + ", " + name + " 👋"),
      h("p", {}, t("welcomeSub"))
    ),
    BalanceCard({ balanceMicros: state.wallet.balanceMicros, debtMicros: state.wallet.debtMicros })
  );

  // Quick actions
  const quick = h("div", { class: "quick-grid" });
  const qa = [
    { ic: "▤", label: t("earnTasks"), sub: t("tasks"), page: "tasks" },
    { ic: "💧", label: t("faucet"), sub: t("claimReward"), page: "faucet" },
    { ic: "♧", label: t("referrals"), sub: t("referralLink"), page: "referrals" },
    { ic: "◈", label: t("wallet"), sub: t("walletSummary"), page: "wallet" }
  ];
  for (const q of qa) {
    quick.append(h("button", { class: "quick-action", onclick: () => navigate(q.page) },
      h("span", { class: "qa-ic" }, q.ic),
      h("b", {}, q.label),
      h("small", {}, q.sub)
    ));
  }
  container.append(h("div", { class: "section-gap" }, h("div", { class: "section-title" }, h("h2", {}, t("quickActions"))), quick));

  // Today's overview
  const statGrid = h("div", { class: "stats-grid" });
  statGrid.append(
    statCard("green", "↗", t("todayEarnings"), fmtBalance(stats.todayEarningsMicros)),
    statCard("cyan", "✓", t("completedTasks"), String(stats.todayTasksCompleted || 0)),
    statCard("violet", "◈", t("totalEarnings"), fmtBalance(stats.totalEarningsMicros)),
    statCard("amber", "♧", t("totalReferrals"), String(stats.totalReferrals || 0))
  );
  container.append(h("div", { class: "section-gap" }, h("div", { class: "section-title" }, h("h2", {}, t("todayOverview"))), statGrid));

  // Featured tasks
  const featuredWrap = h("div", { class: "section-gap" });
  const featuredTitle = h("div", { class: "section-title" },
    h("h2", {}, t("featuredTasks")),
    h("button", { class: "link-more", onclick: () => navigate("tasks") }, t("viewAll") + " ↗")
  );
  const featuredList = h("div", { class: "task-list" });
  featuredWrap.append(featuredTitle, featuredList);
  container.append(featuredWrap);

  function renderFeatured() {
    clear(featuredList);
    const { tasks } = getState();
    if (!tasks.length) {
      featuredList.append(emptyState("🗂️", t("emptyTasks"), t("emptyTasksSub")));
      return;
    }
    const picks = [];
    for (const type of ["ptc", "video", "shortlink"]) {
      const found = tasks.find(x => x.type === type);
      if (found) picks.push(found);
    }
    for (const task of picks.slice(0, 3)) featuredList.append(taskCard(task));
  }

  // Recent activity
  const recentWrap = h("div", { class: "section-gap" });
  recentWrap.append(h("div", { class: "section-title" }, h("h2", {}, t("recentActivity"))));
  const recentList = h("div", { class: "transaction-list" });
  recentWrap.append(recentList);
  container.append(recentWrap);

  function renderRecent() {
    clear(recentList);
    const { recentActivity } = getState();
    if (!recentActivity.length) {
      recentList.append(emptyState("📭", t("emptyRecent"), ""));
      return;
    }
    for (const txn of recentActivity.slice(0, 5)) {
      recentList.append(activityRow(txn));
    }
  }

  renderRecent();
  renderFeatured();

  // Load tasks in background to populate featured cards.
  if (!state.tasksLoaded) {
    featuredList.append(loadingSkeleton(2));
    loadTasks().then(renderFeatured).catch(() => {});
  }
}

function activityRow(txn) {
  const amount = Number(txn.amountMicros || 0);
  const isCredit = amount >= 0;
  const icon = txn.type === "faucet_claim" ? "💧" : (txn.type === "chargeback" ? "↩" : "✓");
  const cls = !isCredit ? "debit" : (txn.type === "faucet_claim" ? "neutral" : "credit");
  return h("div", { class: "txn-item" },
    h("div", { class: "txn-ic " + cls }, icon),
    h("div", { class: "txn-body" }, h("b", {}, txn.title || t("txTask")), h("span", {}, t("today"))),
    h("span", { class: "txn-amount " + (isCredit ? "pos" : "neg") }, (isCredit ? "+" : "−") + fmtMicros(Math.abs(amount)) + " PMX")
  );
}
