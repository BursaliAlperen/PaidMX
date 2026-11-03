#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════╗
║     🎰 FRUITCLAIM PRO v7.0 - ULTRA FAST 7/24 EDITION 🎰         ║
║     Unlimited Loop | Multi-Account | AAA UI | Zero Bugs          ║
║     Creator: AlperenThe | 2026                                   ║
╚══════════════════════════════════════════════════════════════════╝
"""
# ═══════════════════════════════════════════════════════════════════
# BÖLÜM 1: IMPORTS
# ═══════════════════════════════════════════════════════════════════
import json
import os
import shutil
import time
import sys
import random
import math
import tempfile
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# ═══════════════════════════════════════════════════════════════════
# BÖLÜM 2: RENK KODLARI
# ═══════════════════════════════════════════════════════════════════
class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    BRIGHT_BLACK = "\033[90m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"

C = Colors()

# ═══════════════════════════════════════════════════════════════════
# BÖLÜM 3: TEMA SİSTEMİ
# ═══════════════════════════════════════════════════════════════════
class Theme:
    THEMES = {
        "neon": {
            "primary": C.CYAN, "secondary": C.MAGENTA, "accent": C.YELLOW,
            "success": C.GREEN, "error": C.RED, "warning": C.YELLOW,
            "info": C.BLUE, "border": C.CYAN, "text": C.WHITE, "dim": C.DIM,
        },
        "fire": {
            "primary": C.RED, "secondary": C.YELLOW, "accent": C.BRIGHT_RED,
            "success": C.GREEN, "error": C.BRIGHT_RED, "warning": C.YELLOW,
            "info": C.BLUE, "border": C.RED, "text": C.WHITE, "dim": C.DIM,
        },
        "matrix": {
            "primary": C.GREEN, "secondary": C.BRIGHT_GREEN, "accent": C.YELLOW,
            "success": C.GREEN, "error": C.RED, "warning": C.YELLOW,
            "info": C.GREEN, "border": C.GREEN, "text": C.BRIGHT_GREEN, "dim": C.DIM,
        },
        "ocean": {
            "primary": C.BLUE, "secondary": C.CYAN, "accent": C.BRIGHT_CYAN,
            "success": C.GREEN, "error": C.RED, "warning": C.YELLOW,
            "info": C.BLUE, "border": C.BLUE, "text": C.WHITE, "dim": C.DIM,
        },
        "royal": {
            "primary": C.MAGENTA, "secondary": C.BRIGHT_MAGENTA, "accent": C.YELLOW,
            "success": C.GREEN, "error": C.RED, "warning": C.YELLOW,
            "info": C.BLUE, "border": C.MAGENTA, "text": C.WHITE, "dim": C.DIM,
        },
    }

    def __init__(self, name="neon"):
        self.name = name
        self.colors = self.THEMES.get(name, self.THEMES["neon"])

    def __getattr__(self, name):
        if name in self.colors:
            return self.colors[name]
        upper = name.upper()
        if hasattr(Colors, upper):
            return getattr(Colors, upper)
        return C.YELLOW

current_theme = Theme("neon")
T = current_theme

# ═══════════════════════════════════════════════════════════════════
# BÖLÜM 4: TERMİNAL YÖNETİMİ
# ═══════════════════════════════════════════════════════════════════
class TerminalManager:
    @staticmethod
    def width():
        try: return shutil.get_terminal_size().columns
        except: return 80

    @staticmethod
    def height():
        try: return shutil.get_terminal_size().lines
        except: return 24

    @staticmethod
    def clear():
        os.system("cls" if os.name == "nt" else "clear")

    @staticmethod
    def hide_cursor():
        sys.stdout.write("\033[?25l")
        sys.stdout.flush()

    @staticmethod
    def show_cursor():
        sys.stdout.write("\033[?25h")
        sys.stdout.flush()

    @staticmethod
    def set_title(title):
        try:
            sys.stdout.write(f"\033]0;{title}\007")
            sys.stdout.flush()
        except: pass

# ═══════════════════════════════════════════════════════════════════
# BÖLÜM 5: ÇİZİM FONKSİYONLARI
# ═══════════════════════════════════════════════════════════════════
class Drawer:
    @staticmethod
    def line(char="═", length=None, color=None):
        w = length or TerminalManager.width()
        c = color or T.border
        return f"{c}{char * w}{C.RESET}"

    @staticmethod
    def center(text, width=None):
        w = width or TerminalManager.width()
        return text.center(w)

    @staticmethod
    def fancy_box(title, content_lines, width=None):
        w = width or TerminalManager.width()
        inner = w - 6
        out = []
        out.append(f"{T.primary}┏{'━' * inner}┓{C.RESET}")
        if title:
            t = f" {title} ".center(inner)
            out.append(f"{T.primary}┃{C.RESET}{T.accent}{t}{C.RESET}{T.primary}┃{C.RESET}")
            out.append(f"{T.primary}┣{'━' * inner}┫{C.RESET}")
        for line in content_lines:
            padded = line.ljust(inner)[:inner]
            out.append(f"{T.primary}┃{C.RESET} {padded} {T.primary}┃{C.RESET}")
        out.append(f"{T.primary}┗{'━' * inner}┛{C.RESET}")
        return '\n'.join(out)

    @staticmethod
    def divider(text="", style="double"):
        w = TerminalManager.width()
        if style == "double":
            left = "═" * ((w - len(text) - 4) // 2)
            right = "═" * (w - len(text) - 4 - len(left))
            return f"{T.border}{left} {T.accent}« {text} »{T.border} {right}{C.RESET}"
        elif style == "star":
            left = "✦" * ((w - len(text) - 4) // 2)
            right = "✦" * (w - len(text) - 4 - len(left))
            return f"{T.border}{left} {T.accent}[ {text} ]{T.border} {right}{C.RESET}"
        else:
            left = "─" * ((w - len(text) - 4) // 2)
            right = "─" * (w - len(text) - 4 - len(left))
            return f"{T.border}{left} {T.accent}• {text} •{T.border} {right}{C.RESET}"

# ═══════════════════════════════════════════════════════════════════
# BÖLÜM 6: ANİMASYON SİSTEMİ
# ═══════════════════════════════════════════════════════════════════
class Animator:
    SPINNERS = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]

    @staticmethod
    def spinner(text, duration=1.0, color=None):
        c = color or T.warning
        end = time.time() + duration
        i = 0
        try:
            while time.time() < end:
                frame = Animator.SPINNERS[i % len(Animator.SPINNERS)]
                print(f"\r{c}{frame} {text}{C.RESET}", end="", flush=True)
                i += 1
                time.sleep(0.08)
            print(f"\r{T.success}✔ {text}{C.RESET}    ")
        except: pass

    @staticmethod
    def progress_bar(percent, width=40, label=""):
        filled = int(width * percent / 100)
        empty = width - filled
        bar = "█" * filled + "░" * empty
        if percent < 30: color = T.error
        elif percent < 70: color = T.warning
        else: color = T.success
        return f"{color}[{bar}]{C.RESET} {percent:3d}% {label}"

    @staticmethod
    def loading_sequence(steps, delay=0.3):
        for step in steps:
            Animator.spinner(step, duration=delay)
            time.sleep(0.1)

# ═══════════════════════════════════════════════════════════════════
# BÖLÜM 7: ASCII SANAT
# ═══════════════════════════════════════════════════════════════════
class ASCIIArt:
    LOGO_BIG = """
███████╗██╗  ██╗ ██████╗ ███╗   ██╗███████╗██████╗ 
██╔════╝██║  ██║██╔═══██╗████╗  ██║██╔════╝██╔══██╗
███████╗███████║██║   ██║██╔██╗ ██║█████╗  ██████╔╝
╚════██║██╔══██║██║   ██║██║╚██╗██║██╔══╝  ██╔══██╗
███████║██║  ██║╚██████╔╝██║ ╚████║███████╗██║  ██║
╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝
"""

# ═══════════════════════════════════════════════════════════════════
# BÖLÜM 8: GÖRSEL BİLEŞENLER
# ═══════════════════════════════════════════════════════════════════
class VisualComponents:
    @staticmethod
    def header(title, subtitle="", version=""):
        w = TerminalManager.width()
        out = []
        out.append(Drawer.line("═", color=T.primary))
        out.append(Drawer.center(f"{T.accent}{C.BOLD}★ {title} ★{C.RESET}", w))
        if subtitle: out.append(Drawer.center(f"{T.text}{subtitle}{C.RESET}", w))
        if version: out.append(Drawer.center(f"{T.dim}v{version}{C.RESET}", w))
        out.append(Drawer.line("═", color=T.primary))
        return '\n'.join(out)

    @staticmethod
    def status_bar():
        w = TerminalManager.width()
        now = datetime.now().strftime("%H:%M:%S")
        date = datetime.now().strftime("%d/%m/%Y")
        bar = f"{T.primary}┌{C.RESET}" + f"{T.primary}─{C.RESET}" * (w - 2) + f"{T.primary}┐{C.RESET}"
        content = f"{T.primary}│{C.RESET} {T.accent}🕐 {now}{C.RESET} | {T.accent}📅 {date}{C.RESET} | {T.accent}🎰 FruitClaim Pro v7.0{C.RESET} | {T.accent}👤 AlperenThe{C.RESET} "
        content = content.ljust(w - 2)[:w - 2]
        bottom = f"{T.primary}└{C.RESET}" + f"{T.primary}─{C.RESET}" * (w - 2) + f"{T.primary}┘{C.RESET}"
        return f"{bar}\n{T.primary}│{C.RESET}{content}{T.primary}│{C.RESET}\n{bottom}"

    @staticmethod
    def menu_item(number, text, icon="", selected=False):
        if selected: return f"{T.accent}{C.BOLD}  [{number}] {icon} {text}{C.RESET}"
        else: return f"{T.text}  [{number}] {icon} {text}{C.RESET}"

    @staticmethod
    def menu(title, items, footer=""):
        w = TerminalManager.width()
        out = []
        out.append(Drawer.line("═", color=T.primary))
        out.append(Drawer.center(f"{T.accent}{C.BOLD}« {title} »{C.RESET}", w))
        out.append(Drawer.line("─", color=T.border))
        for num, text, icon in items:
            out.append(VisualComponents.menu_item(num, text, icon))
        if footer:
            out.append(Drawer.line("─", color=T.border))
            out.append(f"{T.dim}  {footer}{C.RESET}")
        out.append(Drawer.line("═", color=T.primary))
        return '\n'.join(out)

    @staticmethod
    def stat_card(label, value, icon="📊", color=None):
        c = color or T.primary
        w = 25
        top = f"{c}┌{'─' * (w - 2)}┐{C.RESET}"
        mid = f"{c}│{C.RESET} {icon} {label:<15} {c}│{C.RESET}"
        val = f"{c}│{C.RESET} {T.accent}{C.BOLD}{str(value):<{w - 3}}{C.RESET}{c}│{C.RESET}"
        bot = f"{c}└{'─' * (w - 2)}┘{C.RESET}"
        return f"{top}\n{mid}\n{val}\n{bot}"

    @staticmethod
    def stats_grid(stats_dict):
        cards = []
        for label, (value, icon, color) in stats_dict.items():
            cards.append(VisualComponents.stat_card(label, value, icon, color))
        card_lines = [c.split('\n') for c in cards]
        max_lines = max(len(cl) for cl in card_lines)
        out = []
        for i in range(max_lines):
            row = []
            for cl in card_lines:
                row.append(cl[i] if i < len(cl) else " " * 25)
            out.append("  ".join(row))
        return '\n'.join(out)

    @staticmethod
    def account_card(index, email, balance, credits, status="active"):
        w = 50
        border = T.success if status == "active" else (T.error if status == "error" else T.warning)
        status_icon = "✅" if status == "active" else ("❌" if status == "error" else "⏸️")
        out = []
        out.append(f"{border}╔{'═' * (w - 2)}╗{C.RESET}")
        out.append(f"{border}║{C.RESET} {T.accent}#{index}{C.RESET} {status_icon} {email:<40} {border}║{C.RESET}")
        out.append(f"{border}╠{'═' * (w - 2)}╣{C.RESET}")
        out.append(f"{border}║{C.RESET} 💰 Balance: {T.success}{str(balance):<10}{C.RESET} 🎰 Credits: {T.accent}{str(credits):<10} {border}║{C.RESET}")
        out.append(f"{border}╚{'═' * (w - 2)}╝{C.RESET}")
        return '\n'.join(out)

    @staticmethod
    def notification(title, message, level="info"):
        if level == "success": border, icon = T.success, "✅"
        elif level == "error": border, icon = T.error, "❌"
        elif level == "warning": border, icon = T.warning, "⚠️"
        else: border, icon = T.info, "ℹ️"
        w = 60
        out = []
        out.append(f"{border}╔{'═' * (w - 2)}╗{C.RESET}")
        out.append(f"{border}║{C.RESET} {T.accent}{C.BOLD}{title.center(w - 4)}{C.RESET} {border}║{C.RESET}")
        out.append(f"{border}╠{'═' * (w - 2)}╣{C.RESET}")
        msg_padded = message.center(w - 4)[:w - 4]
        out.append(f"{border}║{C.RESET} {msg_padded} {border}║{C.RESET}")
        out.append(f"{border}╚{'═' * (w - 2)}╝{C.RESET}")
        return '\n'.join(out)

    @staticmethod
    def input_prompt(label, icon="▶"):
        return f"{T.accent}{icon} {label}: {C.RESET}"

    @staticmethod
    def splash_screen():
        w = TerminalManager.width()
        out = []
        out.append("")
        out.append(Drawer.center(f"{T.primary}{C.BOLD}╔══════════════════════════════════════════════════════╗{C.RESET}", w))
        out.append(Drawer.center(f"{T.primary}{C.BOLD}║{C.RESET}{T.accent}  🎰 FRUITCLAIM PRO v7.0 - ULTRA FAST 🎰  {C.RESET}{T.primary}{C.BOLD}║{C.RESET}", w))
        out.append(Drawer.center(f"{T.primary}{C.BOLD}╚══════════════════════════════════════════════════════╝{C.RESET}", w))
        out.append("")
        out.append(Drawer.center(f"{T.text}7/24 Unlimited | Multi-Account | Zero Bugs{C.RESET}", w))
        out.append(Drawer.center(f"{T.dim}Creator: AlperenThe | 2026{C.RESET}", w))
        out.append("")
        out.append(Drawer.center(f"{T.accent}Initializing system...{C.RESET}", w))
        return '\n'.join(out)

# ═══════════════════════════════════════════════════════════════════
# BÖLÜM 9: EFEKTLER
# ═══════════════════════════════════════════════════════════════════
class Effects:
    @staticmethod
    def confetti(duration=1.0):
        emojis = ["🎉", "🎊", "✨", "⭐", "💫", "🌟"]
        w = TerminalManager.width()
        end = time.time() + duration
        try:
            while time.time() < end:
                line = ''.join(random.choice(emojis) for _ in range(w // 2))
                print(f"\r{line}", end="", flush=True)
                time.sleep(0.1)
            print()
        except: pass

# ═══════════════════════════════════════════════════════════════════
# BÖLÜM 10: İSTATİSTİK YÖNETİMİ
# ═══════════════════════════════════════════════════════════════════
class StatsManager:
    STATS_FILE = "bot_stats.json"
    ACCOUNTS_FILE = "accounts.json"

    FIELD_ALIASES = {
        "spins": ("spins", "total_spins", "spin_count", "totalSpins", "spinCount", "rolls"),
        "reward": ("reward", "total_reward", "rewards", "totalReward", "earned", "total_earned"),
        "ads": ("ads", "total_ads", "ad_views", "ads_watched", "totalAds", "adViews"),
        "sessions": ("sessions", "session_count", "total_sessions", "totalSessions"),
    }

    @staticmethod
    def _finite_number(value, default=0.0):
        try:
            number = float(value)
            return number if math.isfinite(number) else default
        except (TypeError, ValueError, OverflowError):
            return default

    @staticmethod
    def normalize_record(record):
        normalized = dict(record) if isinstance(record, dict) else {}
        for canonical, aliases in StatsManager.FIELD_ALIASES.items():
            values = []
            for key in aliases:
                if key in normalized and normalized[key] is not None:
                    value = StatsManager._finite_number(normalized[key], default=None)
                    if value is not None:
                        values.append(value)
            value = max(values) if values else 0.0
            normalized[canonical] = int(value) if canonical != "reward" else value
        if "last_run" not in normalized:
            for alias in ("lastRun", "last_updated", "updated_at"):
                if normalized.get(alias):
                    normalized["last_run"] = normalized[alias]
                    break
        normalized.setdefault("last_run", "")
        return normalized

    @staticmethod
    def load_json(file):
        if os.path.exists(file):
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                return data if isinstance(data, dict) else {}
            except (OSError, json.JSONDecodeError, UnicodeDecodeError):
                return {}
        return {}

    @staticmethod
    def save_json(file, data):
        temp_name = None
        try:
            directory = os.path.dirname(os.path.abspath(file))
            os.makedirs(directory, exist_ok=True)
            with tempfile.NamedTemporaryFile(
                mode='w', encoding='utf-8', dir=directory, delete=False,
                prefix='.fruitclaim-', suffix='.tmp'
            ) as f:
                temp_name = f.name
                json.dump(data, f, indent=2, ensure_ascii=False)
                f.flush()
                os.fsync(f.fileno())
                os.replace(temp_name, file)
            return True
        except (OSError, TypeError, ValueError) as e:
            if temp_name and os.path.exists(temp_name):
                try:
                    os.unlink(temp_name)
                except OSError:
                    pass
            print(f"{T.error}Save error: {e}{C.RESET}")
            return False

    @staticmethod
    def update(email, spins, reward, ads):
        stats = StatsManager.load_json(StatsManager.STATS_FILE)
        current = StatsManager.normalize_record(stats.get(email, {}))
        current["spins"] = int(current["spins"] + StatsManager._finite_number(spins))
        current["reward"] = current["reward"] + StatsManager._finite_number(reward)
        current["ads"] = int(current["ads"] + StatsManager._finite_number(ads))
        current["sessions"] = int(current["sessions"] + 1)
        current["last_run"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        stats[email] = current
        return StatsManager.save_json(StatsManager.STATS_FILE, stats)

    @staticmethod
    def get_all():
        raw = StatsManager.load_json(StatsManager.STATS_FILE)
        return {
            email: StatsManager.normalize_record(record)
            for email, record in raw.items()
            if isinstance(record, dict)
        }

    @staticmethod
    def display_dashboard():
        stats = StatsManager.get_all()
        w = TerminalManager.width()
        print(Drawer.line("═", color=T.primary))
        print(Drawer.center(f"{T.accent}{C.BOLD}📊 GLOBAL STATISTICS DASHBOARD 📊{C.RESET}", w))
        print(Drawer.line("═", color=T.primary))
        print()
        if not stats:
            print(Drawer.center(f"{T.warning}⚠️  No data yet. Run the bot first!{C.RESET}", w))
            return
        total_spins = sum(s["spins"] for s in stats.values())
        total_reward = sum(s["reward"] for s in stats.values())
        total_ads = sum(s["ads"] for s in stats.values())
        total_sessions = sum(s["sessions"] for s in stats.values())
        print(VisualComponents.stats_grid({
            "Total Spins": (total_spins, "🎰", T.accent),
            "Total Reward": (total_reward, "💎", T.success),
            "Total Ads": (total_ads, "📺", T.info),
            "Sessions": (total_sessions, "🔄", T.warning),
        }))
        print()
        print(Drawer.divider("ACCOUNT DETAILS", "star"))
        print()
        for index, (email, record) in enumerate(stats.items(), 1):
            print(VisualComponents.account_card(
                index, email, record["reward"], record["spins"], "active"
            ))
        print()
        print(Drawer.line("═", color=T.primary))
        input(f"\n{T.accent}Press Enter to continue...{C.RESET}")

# ═══════════════════════════════════════════════════════════════════
# BÖLÜM 11: HESAP YÖNETİMİ
# ═══════════════════════════════════════════════════════════════════
class AccountManager:
    @staticmethod
    def load():
        return StatsManager.load_json(StatsManager.ACCOUNTS_FILE)

    @staticmethod
    def save(accs):
        StatsManager.save_json(StatsManager.ACCOUNTS_FILE, accs)

    @staticmethod
    def add(email, password):
        accs = AccountManager.load()
        accs[email] = password
        AccountManager.save(accs)

    @staticmethod
    def remove(email):
        accs = AccountManager.load()
        if email in accs:
            del accs[email]
            AccountManager.save(accs)
            return True
        return False

    @staticmethod
    def list_all():
        return AccountManager.load()

    @staticmethod
    def display():
        accs = AccountManager.list_all()
        w = TerminalManager.width()
        print(Drawer.line("═", color=T.primary))
        print(Drawer.center(f"{T.accent}{C.BOLD}👥 ACCOUNT MANAGER 👥{C.RESET}", w))
        print(Drawer.line("═", color=T.primary))
        print()
        if not accs:
            print(Drawer.center(f"{T.warning}⚠️  No accounts saved.{C.RESET}", w))
            print()
            print(Drawer.center(f"{T.text}Use [+] to add your first account{C.RESET}", w))
        else:
            for i, (email, pwd) in enumerate(accs.items(), 1):
                masked = pwd[:2] + "•" * (len(pwd) - 2) if len(pwd) > 2 else "•••"
                print(VisualComponents.account_card(i, email, "—", "—", "active"))
                print(f"{T.dim}  🔑 Password: {masked}{C.RESET}")
                print()
        print(Drawer.line("═", color=T.primary))

    @staticmethod
    def menu_loop():
        while True:
            AccountManager.display()
            print()
            print(f"{T.success}  [+] Add Account{C.RESET}")
            print(f"{T.error}  [-] Remove Account{C.RESET}")
            print(f"{T.accent}  [C] Clear All{C.RESET}")
            print(f"{T.warning}  [0] Back to Main Menu{C.RESET}")
            print()
            ch = input(VisualComponents.input_prompt("Choice", "▶")).strip().upper()
            if ch == '0':
                break
            elif ch == '+':
                email = input(VisualComponents.input_prompt("Email", "📧")).strip()
                password = input(VisualComponents.input_prompt("Password", "🔑")).strip()
                if email and password:
                    AccountManager.add(email, password)
                    print(VisualComponents.notification("SUCCESS", "Account added!", "success"))
                    time.sleep(1)
                else:
                    print(VisualComponents.notification("ERROR", "Invalid input!", "error"))
                    time.sleep(1)
            elif ch == '-':
                accs = AccountManager.list_all()
                if not accs:
                    print(VisualComponents.notification("INFO", "No accounts to remove", "info"))
                    time.sleep(1)
                    continue
                idx = input(VisualComponents.input_prompt("Account Number", "#")).strip()
                keys = list(accs.keys())
                try:
                    email = keys[int(idx) - 1]
                    if AccountManager.remove(email):
                        print(VisualComponents.notification("SUCCESS", f"Removed {email}", "success"))
                        time.sleep(1)
                except:
                    print(VisualComponents.notification("ERROR", "Invalid selection", "error"))
                    time.sleep(1)
            elif ch == 'C':
                confirm = input(f"{T.error}Clear all accounts? (y/n): {C.RESET}").strip().lower()
                if confirm == 'y':
                    AccountManager.save({})
                    print(VisualComponents.notification("SUCCESS", "All accounts cleared", "success"))
                    time.sleep(1)

# ═══════════════════════════════════════════════════════════════════
# BÖLÜM 12: API URL'LERİ
# ═══════════════════════════════════════════════════════════════════
API_LOGIN = "https://slotfruits.com/api/v1/users/signupFaucetPayLogin"
API_SPIN = "https://slotfruits.com/api/v1/users/earnRoll"
ADS_URL_BASE = (
    "https://googleads.g.doubleclick.net/mads/gma?submodel=SM-A217F"
    "&adid_p=1&format=interstitial_mb"
    "&ini_pn=com.google.android.packageinstaller"
    "&ins_pn=com.google.android.packageinstaller"
    "&omid_v=a.1.5.2-google_20241009"
    "&dv=254380203&ev=24.6.0&gl=ID&hl=in"
    "&js=afma-sdk-a-v254380999.253410000.1"
    "&kw=clothing%2Cfashion&lv=253410000"
    "&ms=CqgFmsA_ATEaQQHY5dWIJ1nnZI0TXJOCrRjxy3oie3ZsfYBDue5jJF2CTFQQuf7W9C9KnP8xbLx0FI_PC-5wIrw0itcrK2KvDP4iEt0E6Yp1pn72NO8vWhbzh19JnXz5v7gGWsohjScUvkVohNO_jbecHUPYSmq4yT-WuJZ2EFv8_r-2HeMQg4ZPiq_jwKyeOrQjsiRXsU8vcZpKSMI0Z7Pn6iha94ABhZW_FbLysDgYt2ox4f_FIffLSbr_vjYntwKQpTg44MpacMRJ2_Ch0aplBuEzXYGkOTHBpg58oZtEw_3nZ8wsO9jE5lLVvx_cmKmOEpfemdesE_wTXvV0Hv5MWrZQ2I4ulXfQrY_gKRBI5ivJJLh3XYIzgBBRhoZastP7yEVFBT7Y8iunIsK3VrABvtw9RWUDkE2lETA0ezNEzwFoAhoGTGHuS2JaZ68x68KZGPFPR1CX4CXbMf1DDtzECiUr12lOsiuPUQ2WWtrjma3PKtkBk-0B5HoTVviRRPOHqgth3x80sbtwMn4G95El7JP079-e_jUT0oa75oJQC-Ph3zmllppvqq3dJN_RCGbyELdXc042fsR1fi3Syd6w1SJROO_t2sP3o2Bdzn2_jv1aokWO8NAzbtrWUs64BUiv1-XMv3k6CReZ91Ac9T28vbfulD8b_t8WSPrIHmXCGEC4h50U74SHhRxUcOmlR7sWpB2y8WfC7NlfoGCG5r6vXzVpG1oFOvTYscbEq1GPl1SjpnwS00RVM5_wfwa6GKc53oRubkV-CBhU_KMXUN115FELhAaNab2qn8reOKeN6xdg_OkZjGgHml1GIlVQity3vBcbzP2yE898LCwcwXVc9oLcH_WHL1eb7K19Z6f5kpquk35qGtTP3xrSzDcw6t-GAxGg1lTCxlMgBA"
    "&mv=84923430.com.android.vending&lft=1&vnm=1.1.6&plbs=0&plcs=0"
    "&u_sd=1.75&request_id=1267448703&target_api=35&carrier=51011"
    "&request_agent=rn-invertase-15.8.0&seq_num=2"
    "&eid=318500618,318486317,318491267,318503826,318509511,318509849,318515546,318518927,318527162,318482080,318483611,318484497,318484801,318525018,318526145,318526848"
    "&guci=0.0.0.0.0.0.0.0&sdk_apis=7%2C8"
    "&omid_p=Google%2Fafma-sdk-a-v260480999.253410000.1&cap=m"
    "&u_w=412&u_h=828&msid=com.piratebaixe.slotMobile"
    "&an=17.android.com.spincoin.appmobile.top&u_audio=3&net=ed&u_so=p&rbv=1"
    "&loeid=44766145%2C318502926&preqs_in_session=1&preqs=1&time_in_session=70&pcc=0"
    "&sst=1766181420000&output=html&region=mobile_app&u_tz=420"
    "&client=ca-app-pub-5674874137587223&slotname=7114498212&kw_type=broad&gsb=4g&lite=0"
    "&app_wp_code=ca-app-pub-5674874137587223&app_code=5186053460&num_ads=1"
    "&vpt=8&vfmt=18&vst=0&sdkv=o.254380999.253410000.1&sdmax=0&dmax=1&sdki=3c4d"
    "&stbg=1&bisch=true&blev=0.16&canm=true&_mv=84923430.com.android.vending"
    "&heap_free=35837248&heap_max=268435456&heap_total=67108864&wv_count=0&rdps=5500"
    "&caps=inlineVideo_interactiveVideo_mraid1_mraid2_mraid3_sdkVideo_exo3_th_autoplay_mediation_scroll_av_transparentBackground_sdkAdmobApiForAds_di_aso_sfv_dinm_dim_nav_navc_dinmo_ipd_of_gls_gcache_saiMacro_sai_demuxedGcache_xSeconds"
    "&is_lat=false"
    "&blob=ABPQqLFPLHz2k6c8n6CqX1sW26j7BjCjFG5-MaUl0CxgLB41Sc1B8kpJWaikL2C_Gp9pl25Xd46LPjDMkuzcNeNk1dvygLdxMwK-Y6rlwJbBvC5njmNuysN-8h288vPObPEuoucf6F2FyhorQbQv9YbRKuFGXNMnm3mLs9x1FneK3ofa6gCK_UTEhPBLeTogM4C8tHMwO2a7T816OsKSD0JYRvo61pYUj8Rx-RsJMnAhHhTzRs3ktQdg-BbwRWiEaPEswxrDeM_GpknK8GoDLzwQ_wuTxQDlAIhl0WIPz9VciYotTXJ86Pe3o5uMwqNeQhZ_qFNQWL_Rncwnb9idfxUEGM5ucxxK_zjofg8F"
    "&jsv=sdk_20190107_RC02-production-sdk_20251202_RC00"
)

# ═══════════════════════════════════════════════════════════════════
# BÖLÜM 13: API FONKSİYONLARI
# ═══════════════════════════════════════════════════════════════════
def get_session():
    session = requests.Session()
    no_retry = Retry(total=0, connect=0, read=0, redirect=0, status=0)
    adapter = HTTPAdapter(max_retries=no_retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session

class RateLimitError(Exception):
    MAX_RATE_LIMIT_WAIT = 24 * 60 * 60
    DEFAULT_RATE_LIMIT_WAIT = 300

def retry_after_seconds(response):
    value = (getattr(response, "headers", {}) or {}).get("Retry-After")
    if not value:
        return RateLimitError.DEFAULT_RATE_LIMIT_WAIT
    try:
        return max(1, int(value.strip()))
    except (AttributeError, TypeError, ValueError):
        pass
    try:
        target = parsedate_to_datetime(value)
        if target.tzinfo is None:
            target = target.replace(tzinfo=timezone.utc)
        now = datetime.now(timezone.utc)
        return max(1, math.ceil((target - now).total_seconds()))
    except (TypeError, ValueError, OverflowError):
        return RateLimitError.DEFAULT_RATE_LIMIT_WAIT

def wait_with_countdown(seconds):
    remaining = max(0, int(seconds))
    while remaining:
        mins, secs = divmod(remaining, 60)
        print(
            f"\r{T.warning}⏳ 429 beklemesi: {mins:02d}:{secs:02d} kaldı "
            f"(Ctrl+C ile durdur){C.RESET}", end="", flush=True
        )
        time.sleep(1)
        remaining -= 1
    print(f"\r{T.success}✔ Bekleme tamamlandı; tek bir tekrar denemesi yapılacak.{C.RESET}                    ")

def wait_once_for_429(response, operation):
    seconds = retry_after_seconds(response)
    if seconds > RateLimitError.MAX_RATE_LIMIT_WAIT:
        message = (
            f"Sunucu {seconds} saniyeden uzun bekleme istedi; güvenli üst sınır "
            f"{RateLimitError.MAX_RATE_LIMIT_WAIT} saniye. {operation} durduruldu."
        )
        print(f"{T.error}⏹️ {message}{C.RESET}")
        raise RateLimitError(message)
    print(
        f"{T.warning}⏳ Sunucu istekleri sınırladı (429). "
        f"{seconds} saniye bekleniyor.{C.RESET}"
    )
    wait_with_countdown(seconds)

def api_login(email, password):
    payload = {"email": email.strip(), "password": password.strip()}
    headers = {
        "User-Agent": "okhttp/4.12.0",
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json"
    }
    session = get_session()
    try:
        for attempt in range(2):
            Animator.spinner("Authenticating", duration=0.8, color=T.accent)
            try:
                resp = session.post(API_LOGIN, json=payload, headers=headers, timeout=10)
                if resp.status_code == 429:
                    if attempt == 0:
                        wait_once_for_429(resp, "Giriş")
                        continue
                    message = "Bekleme sonrası da 429 geldi. Giriş durduruldu."
                    print(f"{T.error}❌ {message}{C.RESET}")
                    raise RateLimitError(message)
                resp.raise_for_status()
                data = resp.json()
                if not isinstance(data, dict):
                    print(f"{T.error}❌ Login yanıtı JSON değil.{C.RESET}")
                    return None
                token = data.get("token")
                user = data.get("user") or {}
                if not isinstance(user, dict):
                    user = {}
                if not token:
                    print(f"{T.error}❌ Token yok.{C.RESET}")
                    return None
                return {
                    "token": token,
                    "user_id": user.get("_id"),
                    "balance": StatsManager._finite_number(user.get("balance", 0)),
                    "credits": max(0, int(StatsManager._finite_number(user.get("credits", 0)))),
                    "email": email
                }
            except RateLimitError:
                raise
            except requests.exceptions.RequestException as e:
                print(f"{T.error}❌ Login Error: {e}{C.RESET}")
                return None
            except (ValueError, TypeError) as e:
                print(f"{T.error}❌ Login yanıtı okunamadı: {e}{C.RESET}")
                return None
            except Exception as e:
                print(f"{T.error}❌ Login Error: {e}{C.RESET}")
                return None
        return None
    finally:
        session.close()

def api_spin_fast(info):
    token = info.get("token", "")
    email = info.get("email", "")
    credits = max(0, int(StatsManager._finite_number(info.get("credits", 0))))
    balance = StatsManager._finite_number(info.get("balance", 0))
    total_reward = 0.0
    spins = 0
    if credits <= 0:
        print(f"{T.warning}⚠️  Kredi yok. Spin yapılmayacak.{C.RESET}")
        return balance, 0, 0, 0.0
    print(f"\n{T.accent}🚀 Spin başlıyor: {credits} kredi{C.RESET}\n")
    headers = {
        "Authorization": f"Bearer {token}",
        "User-Agent": "okhttp/4.12.0",
        "Accept": "application/json, text/plain, */*"
    }
    session = get_session()
    rate_limit_retried = False
    consecutive_failures = 0
    max_failures = 3
    try:
        while credits > 0:
            try:
                response = session.get(API_SPIN, headers=headers, timeout=10)
                if response.status_code == 429:
                    if rate_limit_retried:
                        message = "Spin 429 aldı; döngü durduruldu."
                        print(f"{T.error}⏹️ {message}{C.RESET}")
                        raise RateLimitError(message)
                    rate_limit_retried = True
                    wait_once_for_429(response, "Spin")
                    continue
                response.raise_for_status()
                data = response.json()
                if not isinstance(data, dict):
                    raise ValueError("API yanıtı JSON değil")
                if data.get("error") or data.get("message") == "error":
                    print(f"{T.error}⚠️  API hatası: {data.get('message', 'Bilinmeyen')}{C.RESET}")
                    break
                user = data.get("user") or {}
                if not isinstance(user, dict):
                    user = {}
                new_credits = max(0, int(StatsManager._finite_number(user.get("credits", credits))))
                new_balance = StatsManager._finite_number(user.get("balance", balance), balance)
                success = data.get("success") is True
                if not success and new_credits >= credits:
                    consecutive_failures += 1
                    print(f"{T.warning}⚠️  Spin onaylanmadı; tekrar {consecutive_failures}/{max_failures}.{C.RESET}")
                    if consecutive_failures >= max_failures:
                        print(f"{T.warning}⚠️  API başarılı spin bildirmedi; döngü durduruldu.{C.RESET}")
                        break
                    time.sleep(1)
                    continue
                consecutive_failures = 0
                reward = StatsManager._finite_number(data.get("total", 0))
                credits = new_credits
                balance = new_balance
                total_reward += reward
                spins += 1
                TerminalManager.clear()
                print(VisualComponents.status_bar())
                print()
                print(Drawer.line("═", color=T.primary))
                print(Drawer.center(f"{T.accent}{C.BOLD}🎰 SPINNING | {email}{C.RESET}"))
                print(Drawer.line("═", color=T.primary))
                print()
                print(VisualComponents.stats_grid({
                    "Balance": (f"{balance:.4f}", "💰", T.success),
                    "Last Reward": (f"+{reward:.4f}", "🎁", T.accent),
                    "Spins": (spins, "📊", T.info),
                    "Total Reward": (f"{total_reward:.4f}", "💎", T.warning),
                    "Credits Left": (credits, "⏳", T.primary),
                    "Time": (datetime.now().strftime("%H:%M:%S"), "🕐", T.dim),
                }))
                print()
                print(Animator.progress_bar(min(spins * 5, 100), 40, "Cycle Progress"))
                print()
                if data.get("message"):
                    print(f"{T.info}ℹ️  {data['message']}{C.RESET}")
                print(Drawer.line("═", color=T.primary))
                if credits > 0:
                    time.sleep(0.1)
            except RateLimitError:
                raise
            except requests.exceptions.RequestException as e:
                consecutive_failures += 1
                print(f"{T.error}⚠️  Ağ hatası ({consecutive_failures}/{max_failures}): {e}{C.RESET}")
                if consecutive_failures >= max_failures:
                    print(f"{T.error}⏹️  Tekrarlanan ağ hataları; döngü durduruldu.{C.RESET}")
                    break
                time.sleep(min(2 * consecutive_failures, 5))
            except (ValueError, TypeError, OverflowError) as e:
                consecutive_failures += 1
                print(f"{T.error}⚠️  Yanıt geçersiz ({consecutive_failures}/{max_failures}): {e}{C.RESET}")
                if consecutive_failures >= max_failures:
                    print(f"{T.error}⏹️  Tekrarlanan geçersiz yanıtlar; döngü durduruldu.{C.RESET}")
                    break
                time.sleep(1)
    finally:
        session.close()
    return balance, credits, spins, total_reward

def api_ads_fast(uid, max_ads=3):
    """OTOMATİK REKLAM İZLEME - Orijinal dosyadaki gibi"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 12; SM-A217F Build/SP1A.210812.016; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/147.0.7727.111 Mobile Safari/537.36",
        "sec-ch-ua-platform": '"Android"',
        "sec-ch-ua": '"Android WebView";v="147", "Not.A/Brand";v="8", "Chromium";v="147"',
        "sec-ch-ua-mobile": "?1",
        "x-requested-with": "com.piratebaixe.slotMobile",
        "sec-fetch-site": "same-origin",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer": "https://googleads.g.doubleclick.net/mads/static/sdk/native/sdk-core-v40.html",
        "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
        "priority": "u=1, i",
        "Cookie": "IDE=AHWqTUmPTIJAy-Z7wZUR-Si3c3uYRcuBwUfjmr_ffdlWQMrcruxMTVUyL8XPtA-y_Dk",
    }
    print(f"\n{T.cyan}{'='*60}{C.RESET}")
    print(f"{T.yellow}🚀 Otomatik Reklam İzleme Başlıyor...{C.RESET}")
    print(f"{T.cyan}{'='*60}{C.RESET}\n")
    ads_watched = 0
    session = get_session()
    for i in range(max_ads):
        try:
            Animator.spinner(f"Reklam {i+1}/{max_ads} yükleniyor", duration=1.0, color=T.accent)
            response = session.get(ADS_URL_BASE, headers=headers, timeout=10)
            if "application/json" in response.headers.get("Content-Type", ""):
                data = response.json()
                ad_networks = data.get("ad_networks", [])
                if ad_networks:
                    video_reward_urls = ad_networks[0].get("video_reward_urls", [])
                    for video_url in video_reward_urls:
                        parsed_url = urlparse(video_url)
                        query_parameters = parse_qs(parsed_url.query, keep_blank_values=True)
                        query_parameters["rwd_userid"] = [uid]
                        updated_url = urlunparse(
                            parsed_url._replace(query=urlencode(query_parameters, doseq=True))
                        )
                        reward_response = session.get(updated_url, headers=headers, timeout=10)
                        ads_watched += 1
                        print(f"{T.green}✔ Reklam {ads_watched} izlendi (Status: {reward_response.status_code}){C.RESET}")
                        time.sleep(2)
        except Exception as e:
            print(f"{T.red}❌ Reklam hatası: {str(e)}{C.RESET}")
        time.sleep(3)
    session.close()
    print(f"\n{T.green}✅ Reklam izleme tamamlandı: {ads_watched} reklam{C.RESET}\n")
    return ads_watched

def process_account_247(email, password):
    """Kredi 0 olunca OTOMATİK reklam izler ve devam eder"""
    print(f"\n{T.success}{'='*60}{C.RESET}")
    print(Drawer.center(f"{T.accent}{C.BOLD} FruitClaim - {email}{C.RESET}"))
    print(f"{T.success}{'='*60}{C.RESET}\n")
    cycle = 0
    total_spins_all = 0
    total_reward_all = 0.0
    total_ads_all = 0
    while True:
        cycle += 1
        if cycle % 5 == 1:
            TerminalManager.clear()
            print(f"\n{T.primary}{'='*60}{C.RESET}")
            print(Drawer.center(f"🔄 CYCLE #{cycle} | {datetime.now().strftime('%H:%M:%S')}"))
            print(f"{T.primary}{'='*60}{C.RESET}\n")
        try:
            info = api_login(email, password)
        except RateLimitError:
            print(f"{T.error}⏹️ Rate limit; hesap durduruldu.{C.RESET}")
            break
        if not info:
            print(f"{T.error}❌ Giriş başarısız; hesap durduruldu.{C.RESET}")
            break
        print(f"{T.success}✅ Giriş başarılı | Bakiye: {info['balance']} | Kredi: {info['credits']}{C.RESET}")
        credits = max(0, int(StatsManager._finite_number(info.get("credits", 0))))
        user_id = info.get("user_id")
        # KREDİ 0 İSE OTOMATİK REKLAM İZLE
        if credits <= 0:
            print(f"\n{T.warning}⚠️  Kredi 0! Otomatik reklam izleniyor...{C.RESET}\n")
            if user_id:
                ads_watched = api_ads_fast(user_id, max_ads=3)
                total_ads_all += ads_watched
                print(f"{T.info}📺 {ads_watched} reklam izlendi. Tekrar giriş yapılıyor...{C.RESET}\n")
                time.sleep(2)
                # Tekrar giriş yap ve kredi kontrol et
                try:
                    refreshed_info = api_login(email, password)
                except RateLimitError:
                    print(f"{T.error}⏹️ Kredi doğrulaması rate limit.{C.RESET}")
                    break
                if not refreshed_info:
                    print(f"{T.error}❌ Kredi doğrulanamadı.{C.RESET}")
                    break
                refreshed_credits = max(0, int(StatsManager._finite_number(refreshed_info.get("credits", 0))))
                if refreshed_credits <= 0:
                    print(f"{T.warning}⏹️ Reklam sonrası kredi hâlâ 0. Döngüye devam ediliyor...{C.RESET}\n")
                    time.sleep(5)
                    continue  # Başa dön, tekrar dene
                info = refreshed_info
                credits = refreshed_credits
                print(f"{T.success}✅ Kredi geldi: {credits}. Spinlere devam ediliyor.{C.RESET}\n")
            else:
                print(f"{T.error}❌ User ID yok, reklam izlenemiyor.{C.RESET}\n")
                time.sleep(5)
                continue
        # SPİN YAP
        spins = 0
        reward = 0.0
        remaining_credits = credits
        rate_limited = False
        try:
            _, remaining_credits, spins, reward = api_spin_fast(info)
            total_spins_all += spins
            total_reward_all += reward
            print(f"\n{T.success}✅ Spin: {spins} | Ödül: {reward}{C.RESET}")
        except RateLimitError:
            rate_limited = True
            print(f"{T.error}⏹️ Rate limit; hesap durduruldu.{C.RESET}")
        except Exception as spin_err:
            print(f"{T.error}❌ Spin hatası: {spin_err}{C.RESET}")
        # İstatistik kaydet
        ads = 0
        try:
            StatsManager.update(email, spins, reward, ads)
            print(f"{T.success}📊 Toplam spin: {total_spins_all} | Toplam ödül: {total_reward_all} | Toplam reklam: {total_ads_all}{C.RESET}")
        except Exception as stats_err:
            print(f"{T.error}❌ İstatistik hatası: {stats_err}{C.RESET}")
        if rate_limited:
            break
        # Yeni çevrime geç
        print(f"\n{T.warning}⏳ Yeni çevrimden önce 10 saniye bekleniyor...{C.RESET}")
        wait_with_countdown(10)

# ═══════════════════════════════════════════════════════════════════
# BÖLÜM 14: MENÜ SİSTEMİ
# ═══════════════════════════════════════════════════════════════════
def start_single():
    accs = AccountManager.list_all()
    if not accs:
        print(VisualComponents.notification("ERROR", "No accounts! Add one in Settings", "error"))
        time.sleep(2)
        return
    TerminalManager.clear()
    print(VisualComponents.header("SELECT ACCOUNT", "Choose an account to run", "7.0"))
    print()
    keys = list(accs.keys())
    for i, k in enumerate(keys, 1):
        print(VisualComponents.menu_item(i, k, "📧"))
    print(VisualComponents.menu_item(0, "Back", "↩️"))
    print()
    ch = input(VisualComponents.input_prompt("Choice", "▶")).strip()
    if ch == '0':
        return
    try:
        idx = int(ch)
        if 1 <= idx <= len(keys):
            email = keys[idx - 1]
            process_account_247(email, accs[email])
        else:
            print(f"{T.error}Invalid choice.{C.RESET}")
            time.sleep(1)
    except ValueError:
        print(f"{T.error}Invalid input.{C.RESET}")
        time.sleep(1)
    except KeyboardInterrupt:
        print(f"\n{T.warning}🛑 Stopped{C.RESET}")
    except Exception as e:
        print(f"{T.error}Error: {str(e)}{C.RESET}")
        time.sleep(1)

def start_multi():
    accs = AccountManager.list_all()
    if not accs:
        print(VisualComponents.notification("ERROR", "No accounts!", "error"))
        time.sleep(2)
        return
    TerminalManager.clear()
    print(VisualComponents.header("MULTI-ACCOUNT MODE", f"Processing {len(accs)} accounts", "7.0"))
    print()
    print(VisualComponents.notification("INFO", "Starting all accounts...", "info"))
    print()
    for email, pwd in accs.items():
        try:
            process_account_247(email, pwd)
        except KeyboardInterrupt:
            print(f"\n{T.warning}🛑 Stopped{C.RESET}")
            break
    print()
    Effects.confetti(duration=1.5)
    print(VisualComponents.notification("SUCCESS", "All accounts processed!", "success"))
    time.sleep(3)

def settings_menu():
    while True:
        TerminalManager.clear()
        print(VisualComponents.header("SETTINGS", "Configuration & Accounts", "7.0"))
        print()
        items = [
            ("1", "Account Manager", "👥"),
            ("2", "Change Theme", "🎨"),
            ("3", "View Statistics", "📊"),
            ("4", "System Info", "ℹ️"),
            ("0", "Back to Main Menu", "↩️"),
        ]
        print(VisualComponents.menu("SETTINGS", items))
        print()
        ch = input(VisualComponents.input_prompt("Choice", "▶")).strip()
        if ch == '1':
            AccountManager.menu_loop()
        elif ch == '2':
            TerminalManager.clear()
            print(VisualComponents.header("THEME SELECTOR", "Choose your style", "7.0"))
            print()
            themes = list(Theme.THEMES.keys())
            for i, t in enumerate(themes, 1):
                print(VisualComponents.menu_item(i, t.upper(), "🎨"))
            print()
            th_ch = input(VisualComponents.input_prompt("Theme", "▶")).strip()
            try:
                global current_theme, T
                current_theme = Theme(themes[int(th_ch) - 1])
                T = current_theme
                print(VisualComponents.notification("SUCCESS", f"Theme: {themes[int(th_ch)-1]}", "success"))
                time.sleep(1)
            except:
                print(f"{T.error}Invalid{C.RESET}")
                time.sleep(1)
        elif ch == '3':
            StatsManager.display_dashboard()
        elif ch == '4':
            TerminalManager.clear()
            print(VisualComponents.header("SYSTEM INFO", "", "7.0"))
            print()
            info_lines = [
                f"🎰 Bot: FruitClaim Pro v7.0",
                f"👤 Creator: AlperenThe",
                f"📅 Year: 2026",
                f"🖥️  Terminal: {TerminalManager.width()}x{TerminalManager.height()}",
                f"🎨 Theme: {current_theme.name}",
                f"🐍 Python: {sys.version.split()[0]}",
                f"📦 Requests: {requests.__version__}",
            ]
            print(VisualComponents.fancy_box("INFORMATION", info_lines))
            print()
            input(f"{T.accent}Press Enter...{C.RESET}")
        elif ch == '0':
            break

def main():
    TerminalManager.set_title("FruitClaim Pro v7.0 - AlperenThe")
    TerminalManager.clear()
    print(VisualComponents.splash_screen())
    time.sleep(1)
    Animator.loading_sequence([
        "Loading core modules",
        "Initializing UI system",
        "Connecting to API",
        "Preparing dashboard",
        "System ready"
    ], delay=0.3)
    time.sleep(0.5)
    Effects.confetti(duration=0.8)
    while True:
        TerminalManager.clear()
        print(VisualComponents.status_bar())
        print()
        print(VisualComponents.header("FRUITCLAIM PRO", "7/24 Ultra Fast Multi-Account Bot", "7.0"))
        print()
        w = TerminalManager.width()
        for line in ASCIIArt.LOGO_BIG.split('\n'):
            print(Drawer.center(f"{T.accent}{line}{C.RESET}", w))
        print()
        items = [
            ("1", "START ONE ACCOUNT (7/24)", "🎯"),
            ("2", "START MULTI ACCOUNT (7/24)", "🚀"),
            ("3", "SETTINGS & ACCOUNTS", "⚙️"),
            ("4", "VIEW STATISTICS", "📊"),
            ("5", "EXIT SYSTEM", "🚪"),
        ]
        print(VisualComponents.menu("MAIN MENU", items, "Select an option"))
        print()
        ch = input(VisualComponents.input_prompt("Select Option", "▶")).strip()
        if ch == '1':
            start_single()
        elif ch == '2':
            start_multi()
        elif ch == '3':
            settings_menu()
        elif ch == '4':
            StatsManager.display_dashboard()
        elif ch == '5':
            TerminalManager.clear()
            print(VisualComponents.header("GOODBYE", "Thanks for using FruitClaim Pro", "7.0"))
            print()
            print(Drawer.center(f"{T.accent}👋 See you soon!{C.RESET}"))
            print()
            Effects.confetti(duration=1.0)
            break
        else:
            print(VisualComponents.notification("ERROR", "Invalid option!", "error"))
            time.sleep(1)

# ═══════════════════════════════════════════════════════════════════
# BÖLÜM 15: GİRİŞ NOKTASI
# ═══════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        TerminalManager.show_cursor()
        print(f"\n{T.warning}🛑 Stopped{C.RESET}")
    except Exception as e:
        TerminalManager.show_cursor()
        print(f"\n{T.error}💥 Fatal: {str(e)}{C.RESET}")
