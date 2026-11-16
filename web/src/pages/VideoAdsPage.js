import { h, clear } from "../utils/dom.js";
import { t } from "../i18n.js";
import { createTaskList } from "../components/TaskList.js";

export function renderVideoAds(container) {
  clear(container);
  container.append(
    h("div", { class: "page-heading" },
      h("span", { class: "kicker" }, "VIDEO"),
      h("h1", {}, t("video")),
      h("p", {}, t("taskDesc"))
    )
  );
  const listHost = h("div", {});
  container.append(listHost);
  createTaskList(listHost, { fixedType: "video" });
}
