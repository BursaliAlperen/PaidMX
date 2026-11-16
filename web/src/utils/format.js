import { t } from "../i18n.js";

export function fmtMicros(micros) {
  const v = Number(micros) || 0;
  return (v / 1e6).toLocaleString(undefined, { maximumFractionDigits: 6 });
}

export function fmtBalance(micros) {
  return fmtMicros(micros) + " PMX";
}

export function fmtSeconds(seconds) {
  const s = Math.max(0, Math.floor(Number(seconds) || 0));
  const h = Math.floor(s / 3600);
  const m = Math.floor((s % 3600) / 60);
  const sec = s % 60;
  const pad = n => String(n).padStart(2, "0");
  if (h > 0) return `${h}:${pad(m)}:${pad(sec)}`;
  return `${m}:${pad(sec)}`;
}

export function fmtDate(ms) {
  if (!ms) return "—";
  return new Date(ms).toLocaleDateString(undefined, { day: "2-digit", month: "short", year: "numeric" });
}

export function fmtDateTime(ms) {
  if (!ms) return "—";
  const d = new Date(ms);
  return d.toLocaleDateString(undefined, { day: "2-digit", month: "short" }) + " · " +
    d.toLocaleTimeString(undefined, { hour: "2-digit", minute: "2-digit" });
}

export function timeAgo(ms) {
  if (!ms) return "";
  const diff = Date.now() - ms;
  const min = Math.floor(diff / 60000);
  if (min < 1) return t("today");
  if (min < 60) return `${min} ${min === 1 ? "min" : "min"}`;
  const hours = Math.floor(min / 60);
  if (hours < 24) return `${hours} ${hours === 1 ? "hr" : "hr"}`;
  const days = Math.floor(hours / 24);
  return `${days} ${days === 1 ? "day" : "days"}`;
}

export function clamp(v, min, max) {
  return Math.min(max, Math.max(min, v));
}
