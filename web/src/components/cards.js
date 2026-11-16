import { h } from "../utils/dom.js";
import { fmtMicros, fmtBalance, fmtDateTime } from "../utils/format.js";
import { t } from "../i18n.js";
import { openModal } from "./ui.js";
import { openLink, haptic } from "../services/telegram.js";

export const TYPE_META = {
  ptc: { icon: "◉", cls: "ptc", label: () => t("ptc") },
  video: { icon: "▶", cls: "video", label: () => t("video") },
  shortlink: { icon: "↗", cls: "shortlink", label: () => t("shortlinks") }
};

export function taskTypeMeta(type) {
  return TYPE_META[type] || { icon: "✦", cls: "ptc", label: () => t("category") };
}

export function BalanceCard({ balanceMicros, debtMicros }) {
  let visible = true;
  const amount = h("div", { class: "balance-amount" }, fmtMicros(balanceMicros), h("small", {}, "PMX"));

  function toggle() {
    visible = !visible;
    amount.replaceChildren(visible ? fmtMicros(balanceMicros) : "••••", h("small", {}, "PMX"));
    eye.textContent = visible ? "👁" : "🙈";
    haptic();
  }

  const eye = h("button", { class: "balance-vis", "aria-label": "toggle", onclick: toggle }, "👁");

  return h("div", { class: "balance-card" },
    h("div", { class: "balance-top" },
      h("span", { class: "balance-label" }, t("totalBalance")),
      h("span", { class: "coin-chip" }, h("i", {}, "◆"), "PMX")
    ),
    amount,
    h("div", { class: "balance-rows" },
      h("div", { class: "balance-row" },
        h("span", {}, t("availableBalance")),
        h("b", {}, fmtBalance(balanceMicros))
      ),
      h("div", { class: "balance-row" },
        h("span", {}, t("debtChargebacks")),
        h("b", { class: Number(debtMicros) > 0 ? "neg" : "pos" }, fmtBalance(debtMicros))
      )
    ),
    eye
  );
}

export function taskCard(task, { onStart } = {}) {
  const meta = taskTypeMeta(task.type);
  const reward = h("div", { class: "task-reward" }, "+" + fmtMicros(task.reward), h("small", {}, task.currency || "PMX"));

  const durationNode = task.type === "shortlink"
    ? h("span", { class: "task-duration" }, "⏱ " + t("estimatedTime").toLowerCase())
    : h("span", { class: "task-duration" }, "⏱ " + Number(task.duration) + " sn");

  function openDetail() {
    const body = h("div", {},
      h("p", {}, task.description || t("taskDesc")),
      h("ul", { class: "rule-list" },
        h("li", {}, t("provider") + ": " + meta.label()),
        h("li", {}, t("reward") + ": +" + fmtMicros(task.reward) + " " + (task.currency || "PMX")),
        h("li", {}, t("estimatedTime") + ": " + (task.type === "shortlink" ? t("shortlinks") : Number(task.duration) + " sn")),
        h("li", {}, t("howVerify"))
      )
    );
    const footer = h("button", {
      class: "btn btn-primary btn-block",
      onclick: () => { openLink(task.url); haptic("success"); }
    }, t("startTask") + " ↗");
    openModal({ title: task.title, body, footer });
  }

  const actions = h("div", { class: "task-actions" },
    reward,
    h("button", { class: "btn btn-primary btn-sm", onclick: () => (onStart ? onStart(task) : openDetail()) }, t("start"))
  );

  return h("article", { class: "task-card" },
    h("div", { class: "task-icon " + meta.cls }, meta.icon),
    h("div", { class: "task-body" },
      h("h3", {}, task.title),
      h("p", {}, task.description || t("taskDesc")),
      h("div", { class: "task-meta" },
        h("span", { class: "tag " + meta.cls }, meta.label()),
        durationNode
      )
    ),
    actions
  );
}

export function TransactionItem(txn) {
  const amount = Number(txn.amountMicros || 0);
  const isCredit = amount >= 0;
  const cls = txn.type === "chargeback" || !isCredit ? "debit" : (txn.type === "faucet_claim" ? "neutral" : "credit");
  const icon = txn.type === "faucet_claim" ? "💧" : (txn.type === "chargeback" ? "↩" : "✓");
  const label = txn.type === "task_reward" ? t("txTask")
    : txn.type === "faucet_claim" ? t("txFaucet")
    : txn.type === "referral_reward" ? t("txReferral")
    : txn.type === "chargeback" ? t("txChargeback")
    : t("txAdjustment");

  return h("div", { class: "txn-item" },
    h("div", { class: "txn-ic " + cls }, icon),
    h("div", { class: "txn-body" },
      h("b", {}, txn.title || label),
      h("span", {}, fmtDateTime(txn.createdAt))
    ),
    h("span", { class: "txn-amount " + (isCredit ? "pos" : "neg") },
      (isCredit ? "+" : "−") + fmtMicros(Math.abs(amount)) + " PMX"
    )
  );
}
