#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FruitClaim Enhanced — PRO UI 24/7 Edition (FIXED)
==================================================
- Her cycle'da login → credit'ler sunucudan tazelenir (orijinal gibi)
- Spin loop credit'leri gerçekten harcar
- 7/24 sonsuz döngü + PRO terminal arayüzü
"""

import json
import os
import random
import re
import shutil
import signal
import time
from collections import deque
from datetime import datetime
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

import requests

# ───────────────────────────────────────────────── COLOR PALETTE ───────
RESET    = "\033[0m"
BOLD     = "\033[1m"
DIM      = "\033[2m"
RED      = "\033[31m"
GREEN    = "\033[32m"
YELLOW   = "\033[33m"
BLUE     = "\033[34m"
MAGENTA  = "\033[35m"
CYAN     = "\033[36m"
WHITE    = "\033[37m"
ORANGE   = "\033[38;5;208m"
PINK     = "\033[38;5;213m"
LIME     = "\033[38;5;118m"

ANSI_RE  = re.compile(r"\033\[[0-9;]*m")

# ───────────────────────────────────────────────── CONFIG ──────────────
DEFAULT_EMAIL    = "ankaralironaldo131@gmail.com"
DEFAULT_PASSWORD = "Ankaran#1"

LOGIN_URL = "https://slotfruits.com/api/v1/users/signupFaucetPayLogin"
SPIN_URL  = "https://slotfruits.com/api/v1/users/earnRoll"

ADS_URL = (
    "https://googleads.g.doubleclick.net/mads/gma?submodel=SM-A217F&adid_p=1"
    "&format=interstitial_mb&ini_pn=com.google.android.packageinstaller"
    "&ins_pn=com.google.android.packageinstaller&omid_v=a.1.5.2-google_20241009"
    "&dv=254380203&ev=24.6.0&gl=ID&hl=in&js=afma-sdk-a-v254380999.253410000.1"
    "&kw=clothing%2Cfashion&lv=253410000&ms=CqgFmsA_ATEaQQHY5dWIJ1nnZI0TXJOCrRjxy3"
    "oie3ZsfYBDue5jJF2CTFQQuf7W9C9KnP8xbLx0FI_PC-5wIrw0itcrK2KvDP4iEt0E6Yp1pn72N"
    "O8vWhbzh19JnXz5v7gGWsohjScUvkVohNO_jbecHUPYSmq4yT-WuJZ2EFv8_r-2HeMQg4ZPiq_j"
    "wKyeOrQjsiRXsU8vcZpKSMI0Z7Pn6iha94ABhZW_FbLysDgYt2ox4f_FIffLSbr_vjYntwKQpTg44M"
    "pacMRJ2_Ch0aplBuEzXYGkOTHBpg58oZtEw_3nZ8wsO9jE5lLVvx_cmKmOEpfemdesE_wTXvV0Hv5MW"
    "rZQ2I4ulXfQrY_gKRBI5ivJJLh3XYIzgBBRhoZastP7yEVFBT7Y8iunIsK3VrABvtw9RWUDkE2lET"
    "A0ezNEzwFoAhoGTGHuS2JaZ68x68KZGPFPR1CX4CXbMf1DDtzECiUr12lOsiuPUQ2WWtrjma3PKtkB"
    "k-0B5HoTVviRRPOHqgth3x80sbtwMn4G95El7JP079-e_jUT0oa75oJQC-Ph3zmllppvqq3dJN_RCGb"
    "yELdXc042fsR1fi3Syd6w1SJROO_t2sP3o2Bdzn2_jv1aokWO8NAzbtrWUs64BUiv1-XMv3k6CReZ9"
    "1Ac9T28vbfulD8b_t8WSPrIHmXCGEC4h50U74SHhRxUcOmlR7sWpB2y8WfC7NlfoGCG5r6vXzVpG1o"
    "FOvTYscbEq1GPl1SjpnwS00RVM5_wfwa6GKc53oRubkV-CBhU_KMXUN115FELhAaNab2qn8reOKeN6"
    "xdg_OkZjGgHml1GIlVQity3vBcbzP2yE898LCwcwXVc9oLcH_WHL1eb7K19Z6f5kpquk35qGtTP3xrS"
    "zDcw6t-GAxGg1lTCxlMgBA&mv=84923430.com.android.vending&lft=1&vnm=1.1.6"
    "&plbs=0&plcs=0&u_sd=1.75&request_id=1267448703&target_api=35&carrier=51011"
    "&request_agent=rn-invertase-15.8.0&seq_num=2"
    "&eid=318500618,318486317,318491267,318503826,318509511,318509849,318515546,"
    "318518927,318527162,318482080,318483611,318484497,318484801,318525018,318526145,"
    "318526848&guci=0.0.0.0.0.0.0.0&sdk_apis=7%2C8"
    "&omid_p=Google%2Fafma-sdk-a-v260480999.253410000.1&cap=m&u_w=412&u_h=828"
    "&msid=com.piratebaixe.slotMobile&an=17.android.com.spincoin.appmobile.top"
    "&u_audio=3&net=ed&u_so=p&rbv=1&loeid=44766145%2C318502926&preqs_in_session=1"
    "&preqs=1&time_in_session=70&pcc=0&sst=1766181420000&output=html&region=mobile_app"
    "&u_tz=420&client=ca-app-pub-5674874137587223&slotname=7114498212&kw_type=broad"
    "&gsb=4g&lite=0&app_wp_code=ca-app-pub-5674874137587223&app_code=5186053460"
    "&num_ads=1&vpt=8&vfmt=18&vst=0&sdkv=o.254380999.253410000.1&sdmax=0&dmax=1"
    "&sdki=3c4d&stbg=1&bisch=true&blev=0.16&canm=true&_mv=84923430.com.android.vending"
    "&heap_free=35837248&heap_max=268435456&heap_total=67108864&wv_count=0&rdps=5500"
    "&caps=inlineVideo_interactiveVideo_mraid1_mraid2_mraid3_sdkVideo_exo3_th_autoplay"
    "_mediation_scroll_av_transparentBackground_sdkAdmobApiForAds_di_aso_sfv_dinm_dim"
    "_nav_navc_dinmo_ipdof_gls_gcache_saiMacro_sai_demuxedGcache_xSeconds&is_lat=false"
    "&blob=ABPQqLFPLHz2k6c8n6CqX1sW26j7BjCjFG5-MaUl0CxgLB41Sc1B8kpJWaikL2C_Gp9pl25X"
    "d46LPjDMkuzcNeNk1dvygLdxMwK-Y6rlwJbBvC5njmNuysN-8h288vPObPEuoucf6F2FyhorQbQv9Yb"
    "RKuFGXNMnm3mLs9x1FneK3ofa6gCK_UTEhPBLeTogM4C8tHMwO2a7T816OsKSD0JYRvo61pYUj8Rx-R"
    "sJMnAhHhTzRs3ktQdg-BbwRWiEaPEswxrDeM_GpknK8GoDLzwQ_wuTxQDlAIhl0WIPz9VciYotTXJ8"
    "6Pe3o5uMwqNeQhZ_qFNQWL_Rncwnb9idfxUEGM5ucxxK_zjofg8F"
    "&jsv=sdk_20190107_RC02-production-sdk_20251202_RC00"
)

# ───────────────────────────────────────────────── ASCII BANNER ────────
BANNER = r"""
   ███████╗██████╗ ██╗   ██╗██╗████████╗    ██████╗██╗      █████╗ ██╗███╗   ███╗
   ██╔════╝██╔══██╗██║   ██║██║╚══██╔══╝   ██╔════╝██║     ██╔══██╗██║████╗ ████║
   █████╗  ██████╔╝██║   ██║██║   ██║      ██║     ██║     ███████║██║██╔████╔██║
   ██╔══╝  ██╔══██╗██║   ██║██║   ██║      ██║     ██║     ██╔══██║██║██║╚██╔╝██║
   ██║     ██║  ██║╚██████╔╝██║   ██║      ╚██████╗███████╗██║  ██║██║██║ ╚═╝ ██║
   ╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝   ╚═╝       ╚═════╝╚══════╝╚═╝  ╚═╝╚═╝╚═╝     ╚═╝
"""

# ───────────────────────────────────────────────── HELPERS ────────────
def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def _vis(s: str) -> int:
    return len(ANSI_RE.sub("", s))


def _fit(s: str, width: int) -> str:
    v = _vis(s)
    if v <= width:
        return s + " " * (width - v)
    return ANSI_RE.sub("", s)[: width - 1] + "…"


def _box_width() -> int:
    try:
        return max(68, min(shutil.get_terminal_size().columns - 2, 96))
    except Exception:
        return 78


def _panel(title: str, lines: list, color: str = CYAN, icon: str = "◆") -> None:
    W = _box_width()
    inner = W - 4
    top = color + "╔" + "═" * (W - 2) + "╗" + RESET
    head = (
        color + "║ " + RESET + BOLD + color
        + f"{icon} {title}".center(inner - 2) + RESET
        + " " + color + "║" + RESET
    )
    sep = color + "╟" + "─" * (W - 2) + "╢" + RESET
    bot = color + "╚" + "═" * (W - 2) + "╝" + RESET
    print(top)
    print(head)
    print(sep)
    for line in lines:
        print(color + "║ " + RESET + _fit(line, inner) + color + " ║" + RESET)
    print(bot)


def progress_bar(current: float, total: float, width: int = 22) -> str:
    if total <= 0:
        return DIM + "░" * width + RESET
    filled = int(width * min(max(current / total, 0), 1))
    bar = "█" * filled + "░" * (width - filled)
    return f"{GREEN}{bar}{RESET}"


def hr(char: str = "═", color: str = CYAN) -> str:
    return color + char * _box_width() + RESET


def _ts() -> str:
    return datetime.now().strftime("%H:%M:%S")


def log(msg: str, color: str = WHITE, icon: str = "•") -> None:
    print(f"{DIM}[{_ts()}]{RESET} {color}{icon} {msg}{RESET}")


# ───────────────────────────────────────────────── SPINNER ────────────
_SPIN = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
_FRAME = [0]


def spin_char() -> str:
    _FRAME[0] = (_FRAME[0] + 1) % len(_SPIN)
    return _SPIN[_FRAME[0]]


def spinner_bar(text: str, steps: int = 4) -> None:
    for _ in range(steps):
        print(f"{ORANGE}{spin_char()}{RESET} {YELLOW}{text}{RESET}", end="\r")
        time.sleep(0.18)
    print(" " * (len(text) + 4), end="\r")


# ───────────────────────────────────────────────── STATS ──────────────
class Stats:
    def __init__(self):
        self.started       = datetime.now()
        self.cycles        = 0
        self.spins         = 0
        self.wins          = 0
        self.rewards       = 0.0
        self.ads_hit       = 0
        self.errors        = 0
        self.logins        = 0
        self.last_reward   = 0.0
        self.best_reward   = 0.0

    def uptime(self) -> str:
        return str(datetime.now() - self.started).split(".")[0]

    def success_rate(self) -> str:
        total = self.spins + self.errors
        if total == 0:
            return "100.0%"
        return f"{(self.spins / total) * 100:.1f}%"


STATS = Stats()
LOG_FEED = deque(maxlen=6)
RECENT = deque(maxlen=4)


def feed(msg: str, color: str = WHITE, icon: str = "•") -> None:
    LOG_FEED.append(f"{DIM}{_ts()}{RESET}  {color}{icon} {msg}{RESET}")
    log(msg, color, icon)


# ───────────────────────────────────────────────── SESSIONS ───────────
def api_session() -> requests.Session:
    s = requests.Session()
    s.headers.update({
        "User-Agent": "okhttp/4.12.0",
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
    })
    return s


def browser_session() -> requests.Session:
    s = requests.Session()
    s.headers.update({
        "User-Agent": (
            "Mozilla/5.0 (Linux; Android 12; SM-A217F Build/SP1A.210812.016; wv) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/147.0.7727.111 "
            "Mobile Safari/537.36 (Mobile; afma-sdk-a-v260480999.253410000.1)"
        ),
        "sec-ch-ua-platform": '"Android"',
        "sec-ch-ua": '"Android WebView";v="147", "Not.A/Brand";v="8", "Chromium";v="147"',
        "sec-ch-ua-mobile": "?1",
        "x-requested-with": "com.piratebaixe.slotMobile",
        "sec-fetch-site": "same-origin",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer": "https://googleads.g.doubleclick.net/mads/static/sdk/native/sdk-core-v40.html",
        "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
        "if-none-match": "13022804227014334371",
        "priority": "u=1, i",
        "Cookie": "IDE=AHWqTUmPTIJAy-Z7wZUR-Si3c3uYRcuBwUfjmr_ffdlWQMrcruxMTVUyL8XPtA-y_Dk",
    })
    return s


# ───────────────────────────────────────────────── LOGIN ──────────────
def login(session: requests.Session, email: str, password: str = "", retries: int = 3):
    """Email+password dener; başarısız olursa email-only fallback."""
    payloads = [{"email": email, "password": password}, {"email": email}]
    for attempt in range(1, retries + 1):
        for payload in payloads:
            try:
                r = session.post(LOGIN_URL, data=json.dumps(payload), timeout=20)
                data = r.json()
                token = data.get("token")
                if token:
                    user = data.get("user", {}) or {}
                    STATS.logins += 1
                    return (
                        token,
                        user.get("_id"),
                        user.get("balance", 0),
                        user.get("credits", 0),
                    )
                feed(f"Login reddedildi: {data.get('message','no token')}",
                     YELLOW, "⚠")
            except Exception as e:
                STATS.errors += 1
                feed(f"Login hatası ({attempt}/{retries}): {e}", RED, "✖")
        time.sleep(2 * attempt)
    return None, None, 0, 0


# ───────────────────────────────────────────────── RENDER ─────────────
def render(email, balance, credits, state="IDLE", progress=None, extra=None):
    clear_screen()
    print(CYAN + BANNER + RESET)

    tag = (
        f"{MAGENTA}╭─{RESET} {BOLD}{CYAN}SLOT MOBILE SYNDICATEBOT NET{RESET} "
        f"{MAGENTA}─{RESET} {PINK}PRO UI EDITION{RESET} {MAGENTA}─╮{RESET}"
    )
    print(tag.center(_box_width() + len(tag) - _vis(tag)))

    state_color = {
        "SPINNING": YELLOW, "LOGIN": CYAN, "ADS": ORANGE,
        "IDLE": DIM, "ERROR": RED, "DONE": GREEN, "WAIT": BLUE,
    }.get(state.upper(), WHITE)
    pill = f"{state_color}● {state.upper()}{RESET}"
    print(f"{DIM}State:{RESET} {pill}  {DIM}│{RESET}  "
          f"{DIM}Clock:{RESET} {CYAN}{_ts()}{RESET}  {DIM}│{RESET}  "
          f"{DIM}Spin:{RESET} {ORANGE}{spin_char()}{RESET}")

    acc_lines = [
        f"{GREEN}👤 Email    :{RESET} {WHITE}{email}{RESET}",
        f"{GREEN}💰 Balance  :{RESET} {YELLOW}{balance}{RESET}",
        f"{GREEN}🎰 Credits  :{RESET} {ORANGE}{credits}{RESET}",
    ]
    if extra and extra.get("token"):
        tok = extra["token"]
        tok = tok[:26] + "…" if len(tok) > 26 else tok
        acc_lines.append(f"{GREEN}🔑 Token    :{RESET} {DIM}{tok}{RESET}")
    _panel("ACCOUNT", acc_lines, color=CYAN, icon="👤")

    st_lines = [
        f"{YELLOW}⏱  Uptime    :{RESET} {WHITE}{STATS.uptime():<16}{RESET}"
        f"{YELLOW}🔄 Cycles    :{RESET} {CYAN}{STATS.cycles}{RESET}",
        f"{YELLOW}🎰 Spins     :{RESET} {WHITE}{STATS.spins:<16}{RESET}"
        f"{YELLOW}🏆 Wins      :{RESET} {LIME}{STATS.wins}{RESET}",
        f"{YELLOW}🎁 Rewards   :{RESET} {WHITE}{STATS.rewards:<16.8f}{RESET}"
        f"{YELLOW}📈 Last      :{RESET} {LIME}{STATS.last_reward:.8f}{RESET}",
        f"{YELLOW}📺 Ads Hit   :{RESET} {WHITE}{STATS.ads_hit:<16}{RESET}"
        f"{YELLOW}❌ Errors    :{RESET} {RED}{STATS.errors}{RESET}",
        f"{YELLOW}🔐 Logins    :{RESET} {WHITE}{STATS.logins:<16}{RESET}"
        f"{YELLOW}✅ Success   :{RESET} {GREEN}{STATS.success_rate()}{RESET}",
    ]
    _panel("LIVE STATS", st_lines, color=MAGENTA, icon="📊")

    if progress is not None:
        cur, tot = progress
        bar = progress_bar(cur, tot)
        pct = (cur / tot * 100) if tot > 0 else 0
        prog_lines = [
            f"{CYAN}Credits:{RESET}  {bar}  {BOLD}{cur}/{tot}{RESET} {DIM}({pct:.0f}%){RESET}"
        ]
        _panel("PROGRESS", prog_lines, color=BLUE, icon="⏳")

    if RECENT:
        rl = []
        for i, r in enumerate(RECENT, 1):
            try:
                color = LIME if float(r) > 0 else DIM
            except Exception:
                color = DIM
            rl.append(f"  {DIM}{i}.{RESET} {color}+{r}{RESET}")
        _panel("RECENT REWARDS", rl, color=GREEN, icon="🎁")

    if LOG_FEED:
        _panel("LIVE FEED", list(LOG_FEED), color=YELLOW, icon="📡")

    print(hr())


# ───────────────────────────────────────────────── SPIN ───────────────
def normalize_credit(value) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def run_spin_loop(session, email, token, balance, credits):
    credits = normalize_credit(credits)
    initial = max(credits, 1)
    repeated = 0
    session.headers.update({"authorization": f"Bearer {token}"})

    while credits > 0:
        render(email, balance, credits, "SPINNING",
               progress=(credits, initial), extra={"token": token})
        spinner_bar("🎰 Try To Spin")

        try:
            spin = session.get(SPIN_URL, timeout=20).json()
        except Exception as e:
            STATS.errors += 1
            feed(f"Spin error: {e}", RED, "✖")
            break

        reward = spin.get("total", 0)
        user = spin.get("user", {}) or {}
        balance = user.get("balance", balance)
        new_credits = normalize_credit(user.get("credits", credits))

        try:
            rv = float(reward)
        except (TypeError, ValueError):
            rv = 0.0

        if new_credits == credits:
            repeated += 1
        else:
            repeated = 0
            STATS.spins += 1
            STATS.last_reward = rv
            if rv > 0:
                STATS.wins += 1
                STATS.rewards += rv
                if rv > STATS.best_reward:
                    STATS.best_reward = rv
                RECENT.appendleft(f"{rv:.8f}")
                feed(f"🎰 Spin #{STATS.spins} → +{rv:.8f}", GREEN, "✔")
            else:
                feed(f"🎰 Spin #{STATS.spins} → (no win)", DIM, "·")

        credits = new_credits

        if spin.get("success") is False or repeated >= 2:
            feed("Spin durdu — credits azalmıyor.", YELLOW, "⚠")
            break

        time.sleep(1)

    return balance, credits


# ───────────────────────────────────────────────── ADS ────────────────
def run_ads_loop(user_id: str, attempts: int = 1) -> None:
    if not user_id:
        feed("Ads atlandı: user_id yok.", YELLOW, "⚠")
        return

    feed("🚀 Ads farming başlıyor…", ORANGE, "📺")
    session = browser_session()

    for _ in range(attempts):
        try:
            r = session.get(ADS_URL, timeout=20)
            ctype = r.headers.get("Content-Type", "")
            if "application/json" in ctype:
                data = r.json()
                nets = data.get("ad_networks", [])
                if nets:
                    for url in nets[0].get("video_reward_urls", []):
                        p = urlparse(url)
                        q = parse_qs(p.query, keep_blank_values=True)
                        q["rwd_userid"] = [user_id]
                        updated = urlunparse(p._replace(query=urlencode(q, doseq=True)))
                        rr = session.get(updated, timeout=20)
                        STATS.ads_hit += 1
                        feed(f"📺 Ads Hit {rr.status_code}", GREEN, "✔")
        except Exception as e:
            STATS.errors += 1
            feed(f"Ads error: {e}", RED, "✖")
        time.sleep(3)


# ───────────────────────────────────────────────── MAIN LOOP ──────────
_STOP = False


def _on_sigint(signum, frame):
    global _STOP
    _STOP = True
    print()
    feed("⚠  Durduruluyor… mevcut cycle sonunda çıkış", YELLOW, "⏹")


def final_screen():
    clear_screen()
    print(CYAN + BANNER + RESET)
    print(hr())
    _panel("FINAL REPORT", [
        f"{GREEN}⏱  Uptime      :{RESET} {WHITE}{STATS.uptime()}{RESET}",
        f"{GREEN}🔄 Cycles      :{RESET} {WHITE}{STATS.cycles}{RESET}",
        f"{GREEN}🎰 Spins       :{RESET} {WHITE}{STATS.spins}{RESET}",
        f"{GREEN}🏆 Wins        :{RESET} {LIME}{STATS.wins}{RESET}",
        f"{GREEN}🎁 Total Rew.  :{RESET} {LIME}{STATS.rewards:.8f}{RESET}",
        f"{GREEN}📈 Best Spin   :{RESET} {LIME}{STATS.best_reward:.8f}{RESET}",
        f"{GREEN}📺 Ads Hit     :{RESET} {WHITE}{STATS.ads_hit}{RESET}",
        f"{GREEN}❌ Errors      :{RESET} {RED}{STATS.errors}{RESET}",
        f"{GREEN}🔐 Logins      :{RESET} {WHITE}{STATS.logins}{RESET}",
    ], color=GREEN, icon="🏁")
    print(hr())


def run_forever(email: str = DEFAULT_EMAIL, password: str = DEFAULT_PASSWORD):
    """
    Her cycle'da YENİDEN login olur (orijinal FruitClaim davranışı).
    Bu sayede sunucudan taze 'credits' gelir ve spin loop onları harcar.
    """
    signal.signal(signal.SIGINT, _on_sigint)

    while not _STOP:
        STATS.cycles += 1
        session = api_session()  # her cycle taze session

        try:
            # ── 1) HER CYCLE LOGIN → credits tazelenir ──
            render(email, "—", "—", "LOGIN", extra={})
            spinner_bar("🔐 Logging in")
            token, user_id, balance, credits = login(session, email, password)

            if not token:
                feed("Login fail — 30s retry", RED, "✖")
                time.sleep(30)
                continue

            feed(f"✔ Login OK — user={user_id} credits={credits}", GREEN, "✔")

            # ── 2) SPIN LOOP — credit'leri gerçekten harcar ──
            if normalize_credit(credits) > 0:
                balance, credits = run_spin_loop(
                    session, email, token, balance, credits
                )
                feed(f"✔ Spin done — kalan credits={credits}", GREEN, "✔")
            else:
                feed("Credits=0 — spin atlandı, ads'e geçiliyor", YELLOW, "⚠")

            # ── 3) ADS — sunucuda credit biriktirir ──
            render(email, balance, credits, "ADS", extra={"token": token})
            run_ads_loop(user_id)
            feed("↻ Cycle bitti — yeniden başlıyor", CYAN, "↻")

        except requests.exceptions.RequestException as e:
            STATS.errors += 1
            feed(f"Network error: {e}", RED, "✖")
            time.sleep(15)
        except Exception as e:
            STATS.errors += 1
            feed(f"Unexpected: {e}", RED, "✖")
            time.sleep(10)

        time.sleep(random.uniform(2, 4))

    final_screen()
    log("Temiz çıkış. Bye 👋", MAGENTA, "★")


# ───────────────────────────────────────────────── ENTRY ──────────────
if __name__ == "__main__":
    try:
        clear_screen()
        print(CYAN + BANNER + RESET)
        print(hr())
        _panel("BOOT SEQUENCE", [
            f"{GREEN}👤 Account   :{RESET} {WHITE}{DEFAULT_EMAIL}{RESET}",
            f"{GREEN}🔐 Password  :{RESET} {DIM}{'*' * len(DEFAULT_PASSWORD)}{RESET}",
            f"{GREEN}🎯 Mode      :{RESET} {CYAN}Auto-Login • 24/7 • Infinite{RESET}",
            f"{GREEN}⚙  Engine    :{RESET} {PINK}PRO UI Edition v2.1 (FIXED){RESET}",
            f"{GREEN}🔁 Login     :{RESET} {YELLOW}her cycle (credits refresh){RESET}",
            "",
            f"{YELLOW}▶ Başlamak için 3 saniye… (Ctrl+C durdur){RESET}",
        ], color=CYAN, icon="🚀")
        print(hr())
        time.sleep(3)
        run_forever(DEFAULT_EMAIL, DEFAULT_PASSWORD)
    except KeyboardInterrupt:
        print(f"\n{YELLOW}⏹  Kullanıcı tarafından durduruldu.{RESET}")
        try:
            final_screen()
        except Exception:
            pass
