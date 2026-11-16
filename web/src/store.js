import { rpc } from "./services/api.js";

const state = {
  user: {},
  wallet: {},
  stats: {},
  recentActivity: [],
  admin: false,
  tasks: [],
  tasksLoaded: false,
  faucet: null,
  transactions: [],
  referrals: []
};

const listeners = new Set();

export function getState() {
  return state;
}

export function subscribe(fn) {
  listeners.add(fn);
  return () => listeners.delete(fn);
}

function emit() {
  for (const fn of listeners) fn(state);
}

export function setState(patch) {
  Object.assign(state, patch);
  emit();
}

export async function refreshDashboard() {
  const data = await rpc("getDashboard");
  setState({
    user: data.user || {},
    wallet: data.wallet || {},
    stats: data.stats || {},
    recentActivity: data.recentActivity || [],
    admin: !!data.admin
  });
  return data;
}

export async function loadTasks(force = false) {
  if (state.tasksLoaded && !force) return state.tasks;
  const data = await rpc("getQuickTasks");
  const tasks = Array.isArray(data.tasks) ? data.tasks : [];
  setState({ tasks, tasksLoaded: true });
  return tasks;
}

export async function loadFaucet() {
  const data = await rpc("getFaucet");
  setState({ faucet: data.faucet || null });
  return data.faucet;
}

export async function claimFaucet() {
  const data = await rpc("claimFaucet");
  setState({ faucet: data.faucet || null });
  return data;
}

export async function loadTransactions(limit = 50) {
  const data = await rpc("getTransactions", { limit });
  setState({ transactions: data.transactions || [] });
  return data.transactions;
}

export async function loadReferrals() {
  const data = await rpc("getReferrals");
  setState({ referrals: data.referrals || [] });
  return data.referrals;
}

export async function savePreferences(lang) {
  await rpc("setPreferences", { lang });
}

export async function loadAdminStats() {
  const data = await rpc("adminStats");
  return data.stats;
}
