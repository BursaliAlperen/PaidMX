#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FruitClaim Enhanced — Auto-Login 24/7 Edition
==============================================
Deobfuscated FruitClaim payload, enhanced WITHOUT breaking original behavior.

Added:
  * Automatic login with configured credentials
  * 24/7 uninterrupted cycling with retry + backoff
  * Full ASCII-art UI with live statistics
  * Persistent session reuse
  * Graceful Ctrl+C shutdown
"""

import json
import os
import random
import shutil
import signal
import sys
import time
from datetime import datetime
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

import requests

# ─────────────────────────────────────────────────────────── ANSI ───────
RESET   = "\033[0m"
RED     = "\033[31m"
GREEN   = "\033[32m"
YELLOW  = "\033[33m"
BLUE    = "\033[34m"
MAGENTA = "\033[35m"
CYAN    = "\033[36m"
WHITE   = "\033[37m"
BOLD    = "\033[1m"
DIM     = "\033[2m"

# ───────────────────────────────────────────────────── CONFIG ───────────
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

BANNER = r"""
   ███████╗██╗      ██████╗ ████████╗    ███╗   ███╗ ██████╗ ██████╗
   ██╔════╝██║     ██╔═══██╗╚══██╔══╝    ████╗ ████║██╔═══██╗██╔══██╗
   ███████╗██║     ██║   ██║   ██║       ██╔████╔██║██║   ██║██████╔╝
   ╚════██║██║     ██║   ██║   ██║       ██║╚██╔╝██║██║   ██║██╔══██╗
   ███████║███████╗╚██████╔╝   ██║       ██║ ╚═╝ ██║╚██████╔╝██████╔╝
   ╚══════╝╚══════╝ ╚═════╝    ╚═╝       ╚═╝     ╚═╝ ╚═════╝ ╚═════╝
                    ███████╗██╗   ██╗███╗   ██╗██████╗
                    ██╔════╝╚██╗ ██╔╝████╗  ██║██╔══██╗
                    ███████╗ ╚████╔╝ ██╔██╗ ██║██║  ██║
                    ╚════██║  ╚██╔╝  ██║╚██╗██║██║  ██║
                    ███████║   ██║   ██║ ╚████║██████╔╝
                    ╚══════╝   ╚═╝   ╚═╝  ╚═══╝╚═════╝
                    ══════  SYNDICATEBOT NET  ══════
"""

# ───────────────────────────────────────────────────── HELPERS ──────────
def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def terminal_width() -> int:
    try:
        return shutil.get_terminal_size().columns
    except Exception:
        return 80


def make_line(char: str = "═") -> str:
    return char * max(40, terminal_width())


def center_text(text: str) -> str:
    return text.center(terminal_width())


def log(msg: str, color: str = WHITE) -> None:
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"{DIM}[{ts}]{RESET} {color}{msg}{RESET}")


def animate(text: str, steps: int = 3) -> None:
    for i in range(steps):
        print(f"{YELLOW}{text}{'.' * (i + 1)}{RESET}", end="\r")
        time.sleep(0.25)
    print(" " * (len(text) + 6), end="\r")


# ───────────────────────────────────────────────────── STATS ────────────
class Stats:
    def __init__(self):
        self.started = datetime.now()
        self.cycles = 0
        self.spins = 0
        self.rewards = 0.0
        self.ads_hit = 0
        self.errors = 0
        self.relogins = 0

    def uptime(self) -> str:
        return str(datetime.now() - self.started).split(".")[0]


STATS = Stats()


# ───────────────────────────────────────────────────── SESSION ──────────
def new_session() -> requests.Session:
    s = requests.Session()
    s.headers.update({
        "User-Agent": "okhttp/4.12.0",
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
    })
    return s


def new_browser_session() -> requests.Session:
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


# ───────────────────────────────────────────────────── LOGIN ────────────
def login(session: requests.Session, email: str, password: str = "",
          retries: int = 3):
    """Login; tries email+password first, falls back to email-only."""
    payloads = [{"email": email, "password": password}, {"email": email}]
    for attempt in range(1, retries + 1):
        for payload in payloads:
            try:
                r = session.post(LOGIN_URL, data=json.dumps(payload), timeout=20)
                data = r.json()
                token = data.get("token")
                if token:
                    user = data.get("user", {}) or {}
                    return (
                        token,
                        user.get("_id"),
                        user.get("balance", 0),
                        user.get("credits", 0),
                    )
                log(f"Login attempt failed: {data.get('message', 'no token')}", YELLOW)
            except Exception as e:
                log(f"Login error ({attempt}/{retries}): {e}", RED)
                STATS.errors += 1
        time.sleep(2 * attempt)
    return None, None, 0, 0


# ───────────────────────────────────────────────────── UI ───────────────
def print_ui(email, balance=None, credits=None, extra: dict | None = None):
    clear_screen()
    print(CYAN + BANNER + RESET)
    print(CYAN + make_line("═"))
    print(f"{MAGENTA}{BOLD}Creator     : {RESET}AlperenThe")
    print(f"{MAGENTA}{BOLD}Mode        : {RESET}Auto-Login • 24/7 • Infinite Loop")
    print(CYAN + make_line("═"))
    print(f"{GREEN}Email       : {RESET}{email}")
    if balance is not None:
        print(f"{GREEN}Balance     : {RESET}{balance}")
    if credits is not None:
        print(f"{GREEN}Spin Credits: {RESET}{credits}")
    print(CYAN + make_line("─"))
    print(
        f"{YELLOW}Uptime      : {RESET}{STATS.uptime():<20}"
        f"{YELLOW}Cycles : {RESET}{STATS.cycles}"
    )
    print(
        f"{YELLOW}Spins       : {RESET}{STATS.spins:<20}"
        f"{YELLOW}Rewards: {RESET}{STATS.rewards:.4f}"
    )
    print(
        f"{YELLOW}Ads Hit     : {RESET}{STATS.ads_hit:<20}"
        f"{YELLOW}Errors : {RESET}{STATS.errors}"
    )
    if extra:
        for k, v in extra.items():
            print(f"{YELLOW}{k:<12}: {RESET}{v}")
    print(CYAN + make_line("═"))


# ───────────────────────────────────────────────────── SPIN ─────────────
def normalize_credit_count(value) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def run_spin_loop(session, email, token, balance, credits):
    credits = normalize_credit_count(credits)
    repeated = 0
    session.headers.update({"authorization": f"Bearer {token}"})

    while credits > 0:
        animate("🎰 Spinning")
        try:
            spin = session.get(SPIN_URL, timeout=20).json()
        except Exception as e:
            log(f"Spin error: {e}", RED)
            STATS.errors += 1
            break

        reward = spin.get("total", 0)
        user = spin.get("user", {}) or {}
        balance = user.get("balance", balance)
        new_credits = normalize_credit_count(user.get("credits", credits))

        if new_credits == credits:
            repeated += 1
        else:
            repeated = 0
            STATS.spins += 1
            try:
                STATS.rewards += float(reward)
            except (TypeError, ValueError):
                pass

        credits = new_credits

        print_ui(email, balance, credits, {
            "Reward": reward,
            "Message": spin.get("message", "—"),
        })

        if spin.get("success") is False or repeated >= 2:
            log("Spin stop — credits did not decrease.", YELLOW)
            break
        time.sleep(1)
    return balance, credits


# ───────────────────────────────────────────────────── ADS ──────────────
def run_ads_loop(user_id: str, attempts: int = 1) -> None:
    if not user_id:
        log("Ads skipped: user_id missing.", YELLOW)
        return

    log("🚀 Start Ads Farming...", CYAN)
    session = new_browser_session()

    for _ in range(attempts):
        try:
            response = session.get(ADS_URL, timeout=20)
            ctype = response.headers.get("Content-Type", "")
            if "application/json" in ctype:
                data = response.json()
                networks = data.get("ad_networks", [])
                if networks:
                    for reward_url in networks[0].get("video_reward_urls", []):
                        p = urlparse(reward_url)
                        q = parse_qs(p.query, keep_blank_values=True)
                        q["rwd_userid"] = [user_id]
                        updated = urlunparse(
                            p._replace(query=urlencode(q, doseq=True))
                        )
                        rr = session.get(updated, timeout=20)
                        STATS.ads_hit += 1
                        log(f"✔ Ads Hit {rr.status_code}", GREEN)
        except Exception as e:
            STATS.errors += 1
            log(f"Ads error: {e}", RED)
        time.sleep(3)


# ───────────────────────────────────────────────────── MAIN ─────────────
_STOP = False


def _on_sigint(signum, frame):
    global _STOP
    _STOP = True
    print(f"\n{YELLOW}Stopping — finishing current cycle…{RESET}")


def run_forever(email: str = DEFAULT_EMAIL, password: str = DEFAULT_PASSWORD) -> None:
    signal.signal(signal.SIGINT, _on_sigint)

    session = new_session()
    token = user_id = None
    balance, credits = 0, 0

    while not _STOP:
        STATS.cycles += 1
        try:
            if not token:
                animate("🔐 Logging in")
                token, user_id, balance, credits = login(session, email, password)
                if not token:
                    log("Login failed — retry in 30 s…", RED)
                    time.sleep(30)
                    continue
                STATS.relogins += 1
                log("Login OK ✅", GREEN)

            print_ui(email, balance, credits, {"State": "Spinning"})
            balance, credits = run_spin_loop(
                session, email, token, balance, credits
            )

            run_ads_loop(user_id)
            log("Cycle complete — restarting…", CYAN)

        except requests.exceptions.RequestException as e:
            STATS.errors += 1
            log(f"Network error: {e} — re-login.", RED)
            token = None
            time.sleep(15)
        except Exception as e:
            STATS.errors += 1
            log(f"Unexpected error: {e} — continuing.", RED)
            token = None
            time.sleep(10)

        # small cool-down between cycles
        time.sleep(random.uniform(2, 5))

    log("Shutdown cleanly. Bye 👋", MAGENTA)


# ───────────────────────────────────────────────────── ENTRY ────────────
if __name__ == "__main__":
    try:
        clear_screen()
        print(CYAN + BANNER + RESET)
        print(CYAN + make_line("═"))
        print(center_text(f"{BOLD}Auto-Login 24/7 Edition — AlperenThe{RESET}"))
        print(CYAN + make_line("═"))
        log(f"Account : {DEFAULT_EMAIL}", GREEN)
        log("Starting infinite loop in 3s… (Ctrl+C to stop)", YELLOW)
        time.sleep(3)
        run_forever(DEFAULT_EMAIL, DEFAULT_PASSWORD)
    except KeyboardInterrupt:
        print(f"\n{YELLOW}Interrupted by user.{RESET}")
    finally:
        print(f"{CYAN}Final stats → cycles={STATS.cycles} spins={STATS.spins} "
              f"rewards={STATS.rewards:.4f} ads={STATS.ads_hit} "
              f"errors={STATS.errors}{RESET}")
