import { getInitData } from "./telegram.js";
import { t } from "../i18n.js";

const cfg = window.PAIDMX_CONFIG || {};

const ERROR_MESSAGES = {
  telegram_auth_expired: "telegram_auth_expired",
  telegram_auth_invalid: "telegram_auth_invalid",
  telegram_auth_required: "telegram_auth_required",
  user_banned: "user_banned",
  faucet_cooldown: "faucet_cooldown",
  forbidden: "forbidden",
  origin_not_allowed: "origin_not_allowed",
  offerwall_credentials_missing: "offerwall_credentials_missing"
};

export async function rpc(method, payload = {}) {
  if (!cfg.apiUrl) throw new Error("api_url_missing");
  const initData = getInitData();
  if (!initData) throw new Error("telegram_session_missing");

  let res;
  try {
    res = await fetch(cfg.apiUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-Telegram-Init-Data": initData
      },
      body: JSON.stringify({ rpc: method, payload })
    });
  } catch (_) {
    throw new Error("network_error");
  }

  let data;
  try {
    data = await res.json();
  } catch (_) {
    throw new Error("invalid_response");
  }

  if (!res.ok || !data.ok) {
    const code = String(data?.error || "internal_error");
    let message;
    switch (code) {
      case "telegram_auth_expired":
        message = t("telegram_auth_expired");
        break;
      case "telegram_auth_invalid":
        message = t("telegram_auth_invalid");
        break;
      case "telegram_auth_required":
        message = t("telegram_auth_required");
        break;
      case "user_banned":
        message = t("user_banned");
        break;
      case "faucet_cooldown":
        message = t("faucet_cooldown");
        break;
      case "forbidden":
        message = t("forbidden");
        break;
      default:
        message = t("error") + " (" + res.status + ")";
    }
    const err = new Error(message);
    err.code = code;
    err.status = res.status;
    throw err;
  }

  return data;
}
