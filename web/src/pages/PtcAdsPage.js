import { h, clear } from "../utils/dom.js";
import { t } from "../i18n.js";
import { createTaskList } from "../components/TaskList.js";

export function renderPtcAds(container) {
  clear(container);
  container.append(
    h("div", { class: "page-heading" },
      h("span", { class: "kicker" }, "PTC"),
      h("h1", {}, t("ptc")),
      h("p", {}, t("taskDesc"))
    )
  );
  const listHost = h("div", {});
  container.append(listHost);
  createTaskList(listHost, { fixedType: "ptc" });
}
