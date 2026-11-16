const tg = window.Telegram?.WebApp;

export function initTelegram() {
  if (!tg) return;
  try {
    tg.ready();
    tg.expand();
    tg.setHeaderColor("#080F1D");
    tg.setBackgroundColor("#080F1D");
    tg.disableVerticalSwipes?.();
  } catch (_) {}
}

export function getInitData() {
  return tg?.initData || "";
}

export function getTelegramUser() {
  return tg?.initDataUnsafe?.user || null;
}

export function haptic(type) {
  try {
    if (type === "success") tg?.HapticFeedback?.notificationOccurred("success");
    else if (type === "error") tg?.HapticFeedback?.notificationOccurred("error");
    else tg?.HapticFeedback?.selectionChanged();
  } catch (_) {}
}

export function openLink(url) {
  if (!url) return;
  try {
    if (tg?.openTelegramLink && url.startsWith("https://t.me")) tg.openTelegramLink(url);
    else if (tg?.openLink) tg.openLink(url);
    else window.open(url, "_blank", "noopener,noreferrer");
  } catch (_) {
    window.open(url, "_blank", "noopener,noreferrer");
  }
}

export function shareLink(url, text) {
  const shareUrl = "https://t.me/share/url?url=" + encodeURIComponent(url) + "&text=" + encodeURIComponent(text || "");
  try {
    if (tg?.openTelegramLink) tg.openTelegramLink(shareUrl);
    else window.open(shareUrl, "_blank", "noopener,noreferrer");
  } catch (_) {
    window.open(shareUrl, "_blank", "noopener,noreferrer");
  }
}

export async function copyText(text) {
  if (navigator.clipboard?.writeText) {
    await navigator.clipboard.writeText(text);
    return;
  }
  throw new Error("clipboard_unavailable");
}
