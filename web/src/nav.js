const listeners = [];
const reloadListeners = [];

export function onNavigate(fn) {
  listeners.push(fn);
}

export function navigate(name, params) {
  for (const fn of listeners) fn(name, params);
}

export function onReload(fn) {
  reloadListeners.push(fn);
}

export function requestReload() {
  for (const fn of reloadListeners) fn();
}
