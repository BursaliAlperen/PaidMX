import { h, clear } from "../utils/dom.js";
import { t } from "../i18n.js";
import { getState, loadTasks } from "../store.js";
import { taskCard } from "./cards.js";
import { emptyState, errorState, loadingSkeleton } from "./ui.js";

export function createTaskList(container, { fixedType = null, onStart } = {}) {
  let filter = fixedType || "all";
  let sort = "default";
  let loading = false;
  let error = "";

  function getFiltered() {
    const { tasks } = getState();
    let list = filter === "all" ? tasks : tasks.filter(x => x.type === filter);
    if (sort === "reward") list = [...list].sort((a, b) => (Number(b.reward) || 0) - (Number(a.reward) || 0));
    else if (sort === "duration") list = [...list].sort((a, b) => (Number(a.duration) || 0) - (Number(b.duration) || 0));
    return list;
  }

  function render() {
    clear(container);
    const { tasksLoaded } = getState();

    const chips = h("div", { class: "filter-row" });
    if (!fixedType) {
      const cats = [["all", t("allTasks")], ["ptc", t("ptc")], ["video", t("video")], ["shortlink", t("shortlinks")]];
      for (const [key, label] of cats) {
        const chip = h("button", {
          class: "chip" + (filter === key ? " active" : ""),
          onclick: () => { filter = key; render(); }
        }, label);
        chips.append(chip);
      }
    }

    const sortSelect = h("select", {
      class: "select",
      onchange: e => { sort = e.target.value; render(); }
    },
      h("option", { value: "default" }, t("sortBy")),
      h("option", { value: "reward" }, t("highestReward")),
      h("option", { value: "duration" }, t("shortestDuration"))
    );
    sortSelect.value = sort;

    const refreshBtn = h("button", { class: "refresh-btn" + (loading ? " spinning" : "") }, h("span", { class: "ic" }, "↻"), t("refresh"));
    refreshBtn.addEventListener("click", async () => {
      loading = true;
      refreshBtn.classList.add("spinning");
      try {
        await loadTasks(true);
        error = "";
      } catch (e) {
        error = e.message;
      } finally {
        loading = false;
        render();
      }
    });

    const count = h("div", { class: "toolbar-count" }, h("b", {}, getFiltered().length), " " + t("availableTasks").toLowerCase());
    const toolbar = h("div", { class: "toolbar" }, count, h("div", { style: { display: "flex", gap: "8px", alignItems: "center" } }, sortSelect, refreshBtn));

    container.append(chips, toolbar);

    const list = h("div", { class: "task-list" });
    container.append(list);

    if (!tasksLoaded && !error) {
      list.append(loadingSkeleton(3));
      return;
    }
    if (error) {
      list.append(errorState(error, async () => {
        error = "";
        render();
        try { await loadTasks(true); } catch (e) { error = e.message; }
        render();
      }));
      return;
    }

    const shown = getFiltered();
    if (!shown.length) {
      list.append(emptyState("🗂️", t("emptyTasks"), t("emptyTasksSub")));
      return;
    }
    for (const task of shown) list.append(taskCard(task, { onStart }));
  }

  render();
  return {
    refresh() {
      loadTasks(true).then(() => render()).catch(e => { error = e.message; render(); });
    }
  };
}
