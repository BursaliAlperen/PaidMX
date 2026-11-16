import { h, clear } from "../utils/dom.js";
import { t } from "../i18n.js";
import { getState, loadAdminStats } from "../store.js";
import { emptyState, statCard, loadingSkeleton } from "../components/ui.js";
import { fmtBalance, fmtSeconds } from "../utils/format.js";

export function renderAdmin(container) {
  clear(container);

  if (!getState().admin) {
    container.append(
      h("div", { class: "page-heading" },
        h("span", { class: "kicker" }, "ADMIN"),
        h("h1", {}, t("admin")),
        h("p", {}, t("forbidden"))
      ),
      emptyState("🔒", t("forbidden"), "")
    );
    return;
  }

  container.append(
    h("div", { class: "page-heading" },
      h("span", { class: "kicker" }, "ADMIN"),
      h("h1", {}, t("admin")),
      h("p", {}, t("adminStats"))
    )
  );

  const grid = h("div", { class: "admin-grid" });
  const configBox = h("div", { class: "card section-gap" });
  container.append(grid, configBox);

  grid.append(loadingSkeleton(6));

  loadAdminStats().then(stats => {
    clear(grid);
    grid.append(
      statCard("cyan", "👥", t("totalUsers"), String(stats.totalUsers || 0)),
      statCard("green", "🟢", t("activeUsers"), String(stats.activeUsers7d || 0)),
      statCard("violet", "✓", t("totalTaskRewards"), fmtBalance(stats.totalTaskRewardsMicros)),
      statCard("amber", "💧", t("totalFaucetRewards"), fmtBalance(stats.totalFaucetRewardsMicros)),
      statCard("green", "♧", t("totalReferrals"), String(stats.totalReferrals || 0)),
      statCard("amber", "↩", t("totalChargebacks"), fmtBalance(stats.totalChargebacksMicros)),
      statCard("cyan", "⇄", t("providerEvents"), String(stats.providerEvents || 0)),
      statCard("violet", "⇄", t("providerEvents7d"), String(stats.providerEvents7d || 0))
    );
    clear(configBox);
    configBox.append(
      h("div", { class: "section-title" }, h("h2", {}, t("faucetConfig"))),
      h("div", { class: "faucet-stats" },
        h("div", { class: "faucet-stat" }, h("span", {}, t("claimReward")), h("b", {}, fmtBalance(stats.faucetRewardMicros))),
        h("div", { class: "faucet-stat" }, h("span", {}, t("claimCooldown")), h("b", {}, fmtSeconds(stats.faucetCooldownSeconds)))
      )
    );
  }).catch(() => {
    clear(grid);
    grid.append(emptyState("⚠️", t("error"), ""));
  });
}
