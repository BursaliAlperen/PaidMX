import { h, clear } from "../utils/dom.js";
import { t } from "../i18n.js";
import { createTaskList } from "../components/TaskList.js";

export function renderTasks(container) {
  clear(container);
  container.append(
    h("div", { class: "page-heading" },
      h("span", { class: "kicker" }, "EARN"),
      h("h1", {}, t("taskCenter")),
      h("p", {}, t("taskDesc"))
    )
  );
  const listHost = h("div", {});
  container.append(listHost);
  createTaskList(listHost);
}
