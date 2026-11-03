"""
╔══════════════════════════════════════════════════════════════════╗
║     🎰 FRUITCLAIM PRO v4.0 - AAA EDITION 🎰                     ║
║     Ultra Premium UI | Multi-Account | Live Stats                ║
║     Creator: AlperenThe | 2026                                   ║
╚══════════════════════════════════════════════════════════════════╝
"""

# ═══════════════════════════════════════════════════════════════════
# 🎨 BÖLÜM 1: RENK KODLARI VE TEMA SİSTEMİ
# ═══════════════════════════════════════════════════════════════════

import json
import os
import shutil
import time
import sys
import random
import threading
from datetime import datetime
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# --- ANSI Renk Kodları ---
class Colors:
    """Tüm ANSI renk kodları ve stilleri"""
    RESET       = "\033[0m"
    BOLD        = "\033[1m"
    DIM         = "\033[2m"
    ITALIC      = "\033[3m"
    UNDERLINE   = "\033[4m"
    BLINK       = "\033[5m"
    REVERSE     = "\033[7m"
    HIDDEN      = "\033[8m"
    STRIKE      = "\033[9m"

    # Standart Renkler
    BLACK       = "\033[30m"
    RED         = "\033[31m"
    GREEN       = "\033[32m"
    YELLOW      = "\033[33m"
    BLUE        = "\033[34m"
    MAGENTA     = "\033[35m"
    CYAN        = "\033[36m"
    WHITE       = "\033[37m"

    # Parlak Renkler
    BRIGHT_BLACK    = "\033[90m"
    BRIGHT_RED      = "\033[91m"
    BRIGHT_GREEN    = "\033[92m"
    BRIGHT_YELLOW   = "\033[93m"
    BRIGHT_BLUE     = "\033[94m"
    BRIGHT_MAGENTA  = "\033[95m"
    BRIGHT_CYAN     = "\033[96m"
    BRIGHT_WHITE    = "\033[97m"

    # Arka Plan Renkleri
    BG_BLACK    = "\033[40m"
    BG_RED      = "\033[41m"
    BG_GREEN    = "\033[42m"
    BG_YELLOW   = "\033[43m"
    BG_BLUE     = "\033[44m"
    BG_MAGENTA  = "\033[45m"
    BG_CYAN     = "\033[46m"
    BG_WHITE    = "\033[47m"

    # Parlak Arka Plan
    BG_BRIGHT_RED     = "\033[101m"
    BG_BRIGHT_GREEN   = "\033[102m"
    BG_BRIGHT_YELLOW  = "\033[103m"
    BG_BRIGHT_BLUE    = "\033[104m"
    BG_BRIGHT_MAGENTA = "\033[105m"
    BG_BRIGHT_CYAN    = "\033[106m"

C = Colors()

# --- Tema Sistemi ---
class Theme:
    """Farklı tema seçenekleri"""
    THEMES = {
        "neon": {
            "primary": C.CYAN,
            "secondary": C.MAGENTA,
            "accent": C.YELLOW,
            "success": C.GREEN,
            "error": C.RED,
            "warning": C.YELLOW,
            "info": C.BLUE,
            "border": C.CYAN,
            "text": C.WHITE,
            "dim": C.DIM,
        },
        "fire": {
            "primary": C.RED,
            "secondary": C.YELLOW,
            "accent": C.BRIGHT_RED,
            "success": C.GREEN,
            "error": C.BRIGHT_RED,
            "warning": C.YELLOW,
            "info": C.BLUE,
            "border": C.RED,
            "text": C.WHITE,
            "dim": C.DIM,
        },
        "matrix": {
            "primary": C.GREEN,
            "secondary": C.BRIGHT_GREEN,
            "accent": C.YELLOW,
            "success": C.GREEN,
            "error": C.RED,
            "warning": C.YELLOW,
            "info": C.GREEN,
            "border": C.GREEN,
            "text": C.BRIGHT_GREEN,
            "dim": C.DIM,
        },
        "ocean": {
            "primary": C.BLUE,
            "secondary": C.CYAN,
            "accent": C.BRIGHT_CYAN,
            "success": C.GREEN,
            "error": C.RED,
            "warning": C.YELLOW,
            "info": C.BLUE,
            "border": C.BLUE,
            "text": C.WHITE,
            "dim": C.DIM,
        },
        "royal": {
            "primary": C.MAGENTA,
            "secondary": C.BRIGHT_MAGENTA,
            "accent": C.YELLOW,
            "success": C.GREEN,
            "error": C.RED,
            "warning": C.YELLOW,
            "info": C.BLUE,
            "border": C.MAGENTA,
            "text": C.WHITE,
            "dim": C.DIM,
        },
    }

    def __init__(self, name="neon"):
        self.name = name
        self.colors = self.THEMES.get(name, self.THEMES["neon"])

    def __getattr__(self, name):
        if name in self.colors:
            return self.colors[name]
        raise AttributeError(f"Theme has no '{name}'")

# Aktif tema
current_theme = Theme("neon")
T = current_theme

# ═══════════════════════════════════════════════════════════════════
# 📐 BÖLÜM 2: TERMİNAL VE EKRAN YÖNETİMİ
# ═══════════════════════════════════════════════════════════════════

class TerminalManager:
    """Terminal boyutu ve ekran yönetimi"""

    @staticmethod
    def width():
        """Terminal genişliğini al"""
        try:
            return shutil.get_terminal_size().columns
        except:
            return 80

    @staticmethod
    def height():
        """Terminal yüksekliğini al"""
        try:
            return shutil.get_terminal_size().lines
        except:
            return 24

    @staticmethod
    def clear():
        """Ekranı temizle"""
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
    def move_cursor(x, y):
        sys.stdout.write(f"\033[{y};{x}H")
        sys.stdout.flush()

    @staticmethod
    def save_cursor():
        sys.stdout.write("\033[s")
        sys.stdout.flush()

    @staticmethod
    def restore_cursor():
        sys.stdout.write("\033[u")
        sys.stdout.flush()

    @staticmethod
    def set_title(title):
        """Terminal başlığını ayarla"""
        sys.stdout.write(f"\033]0;{title}\007")
        sys.stdout.flush()

# ═══════════════════════════════════════════════════════════════════
# 🎨 BÖLÜM 3: ÇİZİM VE ŞEKİL FONKSİYONLARI
# ═══════════════════════════════════════════════════════════════════

class Drawer:
    """Çizim fonksiyonları"""

    @staticmethod
    def line(char="═", length=None, color=None):
        """Yatay çizgi"""
        w = length or TerminalManager.width()
        c = color or T.border
        return f"{c}{char * w}{C.RESET}"

    @staticmethod
    def double_line(length=None, color=None):
        return Drawer.line("═", length, color)

    @staticmethod
    def dashed_line(length=None, color=None):
        return Drawer.line("─", length, color)

    @staticmethod
    def dotted_line(length=None, color=None):
        return Drawer.line("·", length, color)

    @staticmethod
    def star_line(length=None, color=None):
        return Drawer.line("✦", length, color)

    @staticmethod
    def wave_line(length=None, color=None):
        w = length or TerminalManager.width()
        c = color or T.border
        wave = "≈" * (w // 2)
        return f"{c}{wave}{C.RESET}"

    @staticmethod
    def center(text, width=None):
        """Metni ortala"""
        w = width or TerminalManager.width()
        return text.center(w)

    @staticmethod
    def box(title, content, width=None, padding=1):
        """Kutu çiz"""
        w = width or TerminalManager.width()
        inner_w = w - 4
        lines = []
        lines.append(f"{T.border}╔{'═' * (inner_w)}╗{C.RESET}")
        if title:
            title_padded = f" {title} ".center(inner_w)
            lines.append(f"{T.border}║{C.RESET}{title_padded}{T.border}║{C.RESET}")
            lines.append(f"{T.border}╠{'═' * (inner_w)}╣{C.RESET}")
        for line in content.split('\n'):
            padded = line.ljust(inner_w)[:inner_w]
            lines.append(f"{T.border}║{C.RESET} {padded} {T.border}║{C.RESET}")
        lines.append(f"{T.border}╚{'═' * (inner_w)}╝{C.RESET}")
        return '\n'.join(lines)

    @staticmethod
    def fancy_box(title, content_lines, width=None):
        """Süslü kutu"""
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
        """Ayırıcı"""
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

    @staticmethod
    def corner_box(title, body_lines):
        """Köşeli kutu"""
        w = TerminalManager.width()
        inner = w - 4
        out = [f"{T.border}╔{'═' * inner}╗{C.RESET}"]
        if title:
            t = f" {title} ".center(inner)
            out.append(f"{T.border}║{C.RESET}{T.accent}{t}{C.RESET}{T.border}║{C.RESET}")
            out.append(f"{T.border}╠{'═' * inner}╣{C.RESET}")
        for line in body_lines:
            p = line.ljust(inner)[:inner]
            out.append(f"{T.border}║{C.RESET} {p} {T.border}║{C.RESET}")
        out.append(f"{T.border}╚{'═' * inner}╝{C.RESET}")
        return '\n'.join(out)

# ═══════════════════════════════════════════════════════════════════
# ✨ BÖLÜM 4: ANİMASYON SİSTEMİ
# ═══════════════════════════════════════════════════════════════════

class Animator:
    """Animasyon fonksiyonları"""

    SPINNERS = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    ARROWS = ["→", "↘", "↓", "↙", "←", "↖", "↑", "↗"]
    DOTS = [".  ", ".. ", "...", " ..", "  ."]
    PULSE = ["○", "◐", "●", "◑"]
    BOUNCERS = ["[    ]", "[=   ]", "[==  ]", "[===]", "[ == ]", "[  = ]", "[    ]"]
    LOADING_BARS = ["▰▱▱▱▱▱▱", "▰▰▱▱▱▱▱", "▰▰▰▱▱▱▱", "▰▰▰▰▱▱▱", "▰▰▰▰▰▱▱", "▰▰▰▰▰▰▱", "▰▰▰▰▰▰▰"]

    @staticmethod
    def spinner(text, duration=1.5, color=None):
        """Dönen spinner"""
        c = color or T.yellow
        end = time.time() + duration
        i = 0
        try:
            while time.time() < end:
                frame = Animator.SPINNERS[i % len(Animator.SPINNERS)]
                print(f"\r{c}{frame} {text}{C.RESET}", end="", flush=True)
                i += 1
                time.sleep(0.08)
            print(f"\r{T.success}✔ {text}{C.RESET}    ")
        except:
            pass

    @staticmethod
    def typing(text, speed=0.03, color=None):
        """Daktilo efekti"""
        c = color or T.text
        for char in text:
            print(f"{c}{char}{C.RESET}", end="", flush=True)
            time.sleep(speed)
        print()

    @staticmethod
    def progress_bar(percent, width=40, label=""):
        """İlerleme çubuğu"""
        filled = int(width * percent / 100)
        empty = width - filled
        bar = "█" * filled + "░" * empty
        if percent < 30:
            color = T.error
        elif percent < 70:
            color = T.warning
        else:
            color = T.success
        return f"{color}[{bar}]{C.RESET} {percent:3d}% {label}"

    @staticmethod
    def animated_progress(task, total_steps, color=None):
        """Animasyonlu ilerleme"""
        c = color or T.primary
        for i in range(total_steps + 1):
            pct = int(i * 100 / total_steps)
            bar = Animator.progress_bar(pct, 30)
            print(f"\r{c}{task}: {bar}{C.RESET}", end="", flush=True)
            time.sleep(0.1)
        print()

    @staticmethod
    def pulse(text, duration=2.0):
        """Nabız efekti"""
        end = time.time() + duration
        i = 0
        try:
            while time.time() < end:
                frame = Animator.PULSE[i % len(Animator.PULSE)]
                print(f"\r{T.accent}{frame} {text}{C.RESET}", end="", flush=True)
                i += 1
                time.sleep(0.2)
        except:
            pass

    @staticmethod
    def bounce(text, duration=1.5):
        """Zıplayan animasyon"""
        end = time.time() + duration
        i = 0
        try:
            while time.time() < end:
                frame = Animator.BOUNCERS[i % len(Animator.BOUNCERS)]
                print(f"\r{T.primary}{frame} {text}{C.RESET}", end="", flush=True)
                i += 1
                time.sleep(0.15)
        except:
            pass

    @staticmethod
    def loading_sequence(steps, delay=0.3):
        """Yükleme sekansı"""
        for step in steps:
            Animator.spinner(step, duration=delay)
            time.sleep(0.1)

    @staticmethod
    def matrix_rain(duration=2.0):
        """Matrix yağmuru efekti"""
        chars = "アイウエオカキクケコサシスセソ0123456789ABCDEF"
        w = TerminalManager.width()
        end = time.time() + duration
        try:
            while time.time() < end:
                line = ''.join(random.choice(chars) for _ in range(w))
                print(f"{T.success}{line}{C.RESET}")
                time.sleep(0.05)
        except:
            pass

    @staticmethod
    def rainbow_text(text):
        """Gökkuşağı metin"""
        colors = [C.RED, C.YELLOW, C.GREEN, C.CYAN, C.BLUE, C.MAGENTA]
        result = ""
        for i, char in enumerate(text):
            result += f"{colors[i % len(colors)]}{char}{C.RESET}"
        return result

    @staticmethod
    def glitch_text(text, iterations=3):
        """Glitch efekti"""
        glitch_chars = "!@#$%^&*()_+-=[]{}|;:',.<>?"
        for _ in range(iterations):
            glitched = ''.join(
                random.choice(glitch_chars) if random.random() < 0.3 else c
                for c in text
            )
            print(f"\r{T.error}{glitched}{C.RESET}", end="", flush=True)
            time.sleep(0.1)
        print(f"\r{T.success}{text}{C.RESET}", end="", flush=True)
        time.sleep(0.3)
        print()

# ═══════════════════════════════════════════════════════════════════
# 🎨 BÖLÜM 5: GÖRSEL BİLEŞENLER
# ═══════════════════════════════════════════════════════════════════

class VisualComponents:
    """Görsel UI bileşenleri"""

    @staticmethod
    def header(title, subtitle="", version=""):
        """Başlık"""
        w = TerminalManager.width()
        out = []
        out.append(Drawer.line("═", color=T.primary))
        out.append(Drawer.center(f"{T.accent}{C.BOLD}★ {title} ★{C.RESET}", w))
        if subtitle:
            out.append(Drawer.center(f"{T.text}{subtitle}{C.RESET}", w))
        if version:
            out.append(Drawer.center(f"{T.dim}v{version}{C.RESET}", w))
        out.append(Drawer.line("═", color=T.primary))
        return '\n'.join(out)

    @staticmethod
    def status_bar():
        """Durum çubuğu"""
        w = TerminalManager.width()
        now = datetime.now().strftime("%H:%M:%S")
        date = datetime.now().strftime("%d/%m/%Y")
        bar = f"{T.primary}┌{C.RESET}" + f"{T.primary}─{C.RESET}" * (w - 2) + f"{T.primary}┐{C.RESET}"
        content = f"{T.primary}│{C.RESET} {T.accent}🕐 {now}{C.RESET} | {T.accent}📅 {date}{C.RESET} | {T.accent}🎰 FruitClaim Pro v4.0{C.RESET} | {T.accent}👤 AlperenThe{C.RESET} "
        content = content.ljust(w - 2)[:w - 2]
        bottom = f"{T.primary}└{C.RESET}" + f"{T.primary}─{C.RESET}" * (w - 2) + f"{T.primary}┘{C.RESET}"
        return f"{bar}\n{T.primary}│{C.RESET}{content}{T.primary}│{C.RESET}\n{bottom}"

    @staticmethod
    def menu_item(number, text, icon="", selected=False):
        """Menü öğesi"""
        if selected:
            return f"{T.accent}{C.BOLD}  [{number}] {icon} {text}{C.RESET}"
        else:
            return f"{T.text}  [{number}] {icon} {text}{C.RESET}"

    @staticmethod
    def menu(title, items, footer=""):
        """Menü"""
        w = TerminalManager.width()
        out = []
        out.append(Drawer.line("═", color=T.primary))
        out.append(Drawer.center(f"{T.accent}{C.BOLD}« {title} »{C.RESET}", w))
        out.append(Drawer.line("─", color=T.border))
        for i, (num, text, icon) in enumerate(items):
            out.append(VisualComponents.menu_item(num, text, icon))
        if footer:
            out.append(Drawer.line("─", color=T.border))
            out.append(f"{T.dim}  {footer}{C.RESET}")
        out.append(Drawer.line("═", color=T.primary))
        return '\n'.join(out)

    @staticmethod
    def info_card(title, items, icon="ℹ️"):
        """Bilgi kartı"""
        lines = []
        lines.append(f"{T.accent}{icon} {title}{C.RESET}")
        lines.append(Drawer.dashed_line(color=T.border))
        for label, value in items:
            lines.append(f"{T.text}  {label:<20} : {T.accent}{value}{C.RESET}")
        return Drawer.fancy_box("", lines)

    @staticmethod
    def stat_card(label, value, icon="📊", color=None):
        """İstatistik kartı"""
        c = color or T.primary
        w = 25
        top = f"{c}┌{'─' * (w - 2)}┐{C.RESET}"
        mid = f"{c}│{C.RESET} {icon} {label:<15} {c}│{C.RESET}"
        val = f"{c}│{C.RESET} {T.accent}{C.BOLD}{str(value):<{w - 3}}{C.RESET}{c}│{C.RESET}"
        bot = f"{c}└{'─' * (w - 2)}┘{C.RESET}"
        return f"{top}\n{mid}\n{val}\n{bot}"

    @staticmethod
    def stats_grid(stats_dict):
        """İstatistik ızgarası"""
        cards = []
        for label, (value, icon, color) in stats_dict.items():
            cards.append(VisualComponents.stat_card(label, value, icon, color))
        # Yan yana diz
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
        """Hesap kartı"""
        w = 50
        if status == "active":
            border = T.success
            status_icon = "✅"
        elif status == "error":
            border = T.error
            status_icon = "❌"
        else:
            border = T.warning
            status_icon = "⏸️"

        out = []
        out.append(f"{border}╔{'═' * (w - 2)}╗{C.RESET}")
        out.append(f"{border}║{C.RESET} {T.accent}#{index}{C.RESET} {status_icon} {email:<40} {border}║{C.RESET}")
        out.append(f"{border}╠{'═' * (w - 2)}╣{C.RESET}")
        out.append(f"{border}║{C.RESET} 💰 Balance: {T.success}{balance:<10}{C.RESET} 🎰 Credits: {T.accent}{credits:<10} {border}║{C.RESET}")
        out.append(f"{border}╚{'═' * (w - 2)}╝{C.RESET}")
        return '\n'.join(out)

    @staticmethod
    def log_entry(level, message, timestamp=None):
        """Log girişi"""
        ts = timestamp or datetime.now().strftime("%H:%M:%S")
        if level == "INFO":
            color, icon = T.info, "ℹ️"
        elif level == "SUCCESS":
            color, icon = T.success, "✅"
        elif level == "WARNING":
            color, icon = T.warning, "⚠️"
        elif level == "ERROR":
            color, icon = T.error, "❌"
        elif level == "DEBUG":
            color, icon = T.dim, "🔍"
        else:
            color, icon = T.text, "•"
        return f"{T.dim}[{ts}]{C.RESET} {color}{icon} {message}{C.RESET}"

    @staticmethod
    def notification(title, message, level="info"):
        """Bildirim"""
        if level == "success":
            border, icon = T.success, "✅"
        elif level == "error":
            border, icon = T.error, "❌"
        elif level == "warning":
            border, icon = T.warning, "⚠️"
        else:
            border, icon = T.info, "ℹ️"
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
        """Giriş promptu"""
        return f"{T.accent}{icon} {label}: {C.RESET}"

    @staticmethod
    def splash_screen():
        """Açılış ekranı"""
        w = TerminalManager.width()
        out = []
        out.append("")
        out.append(Drawer.center(f"{T.primary}{C.BOLD}╔══════════════════════════════════════════════════════╗{C.RESET}", w))
        out.append(Drawer.center(f"{T.primary}{C.BOLD}║{C.RESET}{T.accent}  🎰 FRUITCLAIM PRO v4.0 - AAA EDITION 🎰  {C.RESET}{T.primary}{C.BOLD}║{C.RESET}", w))
        out.append(Drawer.center(f"{T.primary}{C.BOLD}╚══════════════════════════════════════════════════════╝{C.RESET}", w))
        out.append("")
        out.append(Drawer.center(f"{T.text}Ultra Premium Multi-Account Bot{C.RESET}", w))
        out.append(Drawer.center(f"{T.dim}Creator: AlperenThe | 2026{C.RESET}", w))
        out.append("")
        out.append(Drawer.center(f"{T.accent}Initializing system...{C.RESET}", w))
        return '\n'.join(out)

    @staticmethod
    def achievement_badge(title, description, icon="🏆"):
        """Başarı rozeti"""
        w = 50
        out = []
        out.append(f"{T.accent}╔{'═' * (w - 2)}╗{C.RESET}")
        out.append(f"{T.accent}║{C.RESET} {icon} {title.center(w - 6)} {T.accent}║{C.RESET}")
        out.append(f"{T.accent}╠{'═' * (w - 2)}╣{C.RESET}")
        desc_padded = description.center(w - 4)[:w - 4]
        out.append(f"{T.accent}║{C.RESET} {desc_padded} {T.accent}║{C.RESET}")
        out.append(f"{T.accent}╚{'═' * (w - 2)}╝{C.RESET}")
        return '\n'.join(out)

    @staticmethod
    def mini_bar_chart(values, labels, max_height=5):
        """Mini çubuk grafik"""
        max_val = max(values) if values else 1
        out = []
        for i, (val, label) in enumerate(zip(values, labels)):
            height = int(val / max_val * max_height) if max_val > 0 else 0
            bar = "█" * height
            color = [T.success, T.accent, T.warning, T.error][i % 4]
            out.append(f"{color}{bar:<{max_height}}{C.RESET} {label}: {val}")
        return '\n'.join(out)

    @staticmethod
    def loading_screen():
        """Yükleme ekranı"""
        w = TerminalManager.width()
        out = []
        out.append("")
        out.append(Drawer.center(f"{T.primary}╔══════════════════════════════════════╗{C.RESET}", w))
        out.append(Drawer.center(f"{T.primary}║{C.RESET}{T.accent}  SYSTEM LOADING...  {C.RESET}{T.primary}║{C.RESET}", w))
        out.append(Drawer.center(f"{T.primary}╚══════════════════════════════════════╝{C.RESET}", w))
        out.append("")
        return '\n'.join(out)

# ═══════════════════════════════════════════════════════════════════
# 🎭 BÖLÜM 6: ASCII SANAT KÜTÜPHANESİ
# ═══════════════════════════════════════════════════════════════════

class ASCIIArt:
    """ASCII sanat koleksiyonu"""

    FRUIT = r"""
    🍎🍊🍋🍇🍓🍒🍑🍍🥝🍌
    """

    SLOT_MACHINE = r"""
   ╔═══════════════════════════════╗
   ║  🎰  SLOT MACHINE  🎰        ║
   ║  ┌─────┬─────┬─────┐         ║
   ║  │  🍒 │  🍋 │  🍇 │         ║
   ║  └─────┴─────┴─────┘         ║
   ║         [ SPIN ]              ║
   ╚═══════════════════════════════╝
    """

    LOGO_BIG = r"""
 ███████╗██╗  ██╗ ██████╗ ███╗   ██╗███████╗██████╗ 
 ██╔════╝██║  ██║██╔═══██╗████╗  ██║██╔════╝██╔══██╗
 ███████╗███████║██║   ██║██╔██╗ ██║█████╗  ██████╔╝
 ╚════██║██╔══██║██║   ██║██║╚██╗██║██╔══╝  ██╔══██╗
 ███████║██║  ██║╚██████╔╝██║ ╚████║███████╗██║  ██║
 ╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝
    """

    LOGO_SMALL = r"""
  ┌─────────────────────────┐
  │  🎰 FRUITCLAIM PRO 🎰   │
  └─────────────────────────┘
    """

    TROPHY = r"""
       ___________
      '._==_==_=_.'
      .-\:      /-.
     | (|:.     |) |
      '-|:.     |-'
        \::.    /
         '::. .'
           ) (
         _.' '._
        `"""""""`
    """

    ROCKET = r"""
           /\\
          /  \\
         |    |
         |    |
         |    |
        /|    |\\
       / |    | \\
      /  |    |  \\
     /___|____|___\\
         |    |
         |    |
        /      \\
       /________\\
    """

    COIN = r"""
      .-""""""-.
    .'          '.
   /   O      O   \\
  :           `    :
  |                |
  :    .------.    :
   \\  '        '  /
    '.          .'
      '-......-'
    """

    CROWN = r"""
         .-~-.
        / _ _ \\
       | (_|_) |
       |  _ _  |
        \\_ _ /
         '---'
    """

    STAR = r"""
          *
         ***
        *****
       *******
      *********
       *******
        *****
         ***
          *
    """

    HEART = r"""
     **   **
    **** ****
   ***********
    *********
     *******
      *****
       ***
        *
    """

    DIAMOND = r"""
          *
         ***
        *****
       *******
      *********
       *******
        *****
         ***
          *
    """

    GEAR = r"""
       .-~~~-.
     .'       '.
    /    O   O   \\
   |      _      |
    \\    (_)    /
     '.       .'
       '-...-'
    """

    @staticmethod
    def get(name):
        """ASCII sanatı al"""
        return getattr(ASCIIArt, name.upper(), "")

# ═══════════════════════════════════════════════════════════════════
# 🎨 BÖLÜM 7: EFEKT VE TRANSİSYON SİSTEMİ
# ═══════════════════════════════════════════════════════════════════

class Effects:
    """Görsel efektler"""

    @staticmethod
    def fade_in(text, duration=0.5):
        """Solma efekti"""
        steps = 10
        for i in range(steps):
            alpha = i / steps
            # Basit simülasyon
            print(f"\r{text}", end="", flush=True)
            time.sleep(duration / steps)
        print()

    @staticmethod
    def slide_in(text, direction="left", width=None):
        """Kayma efekti"""
        w = width or TerminalManager.width()
        for i in range(w):
            if direction == "left":
                padded = text.rjust(w - i)
            else:
                padded = text.ljust(w - i)
            print(f"\r{padded}", end="", flush=True)
            time.sleep(0.02)
        print()

    @staticmethod
    def typewriter(text, speed=0.05, color=None):
        """Daktilo efekti"""
        c = color or T.text
        for char in text:
            print(f"{c}{char}{C.RESET}", end="", flush=True)
            time.sleep(speed)
        print()

    @staticmethod
    def scramble(text, iterations=5):
        """Karıştırma efekti"""
        chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%"
        for _ in range(iterations):
            scrambled = ''.join(random.choice(chars) for _ in text)
            print(f"\r{T.error}{scrambled}{C.RESET}", end="", flush=True)
            time.sleep(0.1)
        print(f"\r{T.success}{text}{C.RESET}", end="", flush=True)
        time.sleep(0.3)
        print()

    @staticmethod
    def flash(text, color=None, count=3):
        """Yanıp sönme"""
        c = color or T.accent
        for _ in range(count):
            print(f"\r{T.bg_bright_red}{c}{text}{C.RESET}", end="", flush=True)
            time.sleep(0.15)
            print(f"\r{' ' * len(text)}", end="", flush=True)
            time.sleep(0.15)
        print(f"\r{text}", end="", flush=True)
        time.sleep(0.3)
        print()

    @staticmethod
    def wave(text):
        """Dalga efekti"""
        for offset in range(len(text)):
            displayed = ""
            for i, char in enumerate(text):
                if (i + offset) % 3 == 0:
                    displayed += f"{T.accent}{char}{C.RESET}"
                else:
                    displayed += char
            print(f"\r{displayed}", end="", flush=True)
            time.sleep(0.1)
        print()

    @staticmethod
    def confetti(duration=1.0):
        """Konfeti efekti"""
        emojis = ["🎉", "🎊", "✨", "⭐", "💫", "🌟"]
        w = TerminalManager.width()
        end = time.time() + duration
        try:
            while time.time() < end:
                line = ''.join(random.choice(emojis) for _ in range(w // 2))
                print(f"\r{line}", end="", flush=True)
                time.sleep(0.1)
            print()
        except:
            pass

# ═══════════════════════════════════════════════════════════════════
# 📊 BÖLÜM 8: İSTATİSTİK VE RAPOR SİSTEMİ
# ═══════════════════════════════════════════════════════════════════

class StatsManager:
    """İstatistik yönetimi"""

    STATS_FILE = "bot_stats.json"
    ACCOUNTS_FILE = "accounts.json"

    @staticmethod
    def load_json(file):
        if os.path.exists(file):
            try:
                with open(file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {}

    @staticmethod
    def save_json(file, data):
        try:
            with open(file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"{T.error}Save error: {e}{C.RESET}")

    @staticmethod
    def update(email, spins, reward, ads):
        stats = StatsManager.load_json(StatsManager.STATS_FILE)
        if email not in stats:
            stats[email] = {"spins": 0, "reward": 0, "ads": 0, "sessions": 0}
        s = stats[email]
        s["spins"] += spins
        s["reward"] += reward
        s["ads"] += ads
        s["sessions"] += 1
        s["last_run"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        StatsManager.save_json(StatsManager.STATS_FILE, stats)

    @staticmethod
    def get_all():
        return StatsManager.load_json(StatsManager.STATS_FILE)

    @staticmethod
    def get_account(email):
        stats = StatsManager.get_all()
        return stats.get(email, {})

    @staticmethod
    def display_dashboard():
        """İstatistik panosu"""
        stats = StatsManager.get_all()
        w = TerminalManager.width()

        print(Drawer.line("═", color=T.primary))
        print(Drawer.center(f"{T.accent}{C.BOLD}📊 GLOBAL STATISTICS DASHBOARD 📊{C.RESET}", w))
        print(Drawer.line("═", color=T.primary))
        print()

        if not stats:
            print(Drawer.center(f"{T.warning}⚠️  No data yet. Run the bot first!{C.RESET}", w))
            return

        # Toplam istatistikler
        total_spins = sum(s.get("spins", 0) for s in stats.values())
        total_reward = sum(s.get("reward", 0) for s in stats.values())
        total_ads = sum(s.get("ads", 0) for s in stats.values())
        total_sessions = sum(s.get("sessions", 0) for s in stats.values())

        print(VisualComponents.stats_grid({
            "Total Spins": (total_spins, "🎰", T.accent),
            "Total Reward": (total_reward, "💎", T.success),
            "Total Ads": (total_ads, "📺", T.info),
            "Sessions": (total_sessions, "🔄", T.warning),
        }))
        print()

        # Her hesap için
        print(Drawer.divider("ACCOUNT DETAILS", "star"))
        print()

        for email, s in stats.items():
            print(VisualComponents.info_card(
                email,
                [
                    ("🎰 Spins", s.get("spins", 0)),
                    ("💎 Reward", s.get("reward", 0)),
                    ("📺 Ads", s.get("ads", 0)),
                    ("🔄 Sessions", s.get("sessions", 0)),
                    ("🕐 Last Run", s.get("last_run", "N/A")),
                ],
                "📧"
            ))
            print()

        # Mini grafik
        if len(stats) > 1:
            print(Drawer.divider("REWARD COMPARISON", "double"))
            print()
            emails = list(stats.keys())
            rewards = [stats[e].get("reward", 0) for e in emails]
            short_emails = [e[:15] for e in emails]
            print(VisualComponents.mini_bar_chart(rewards, short_emails))
            print()

        print(Drawer.line("═", color=T.primary))
        input(f"\n{T.accent}Press Enter to continue...{C.RESET}")

# ═══════════════════════════════════════════════════════════════════
# 👥 BÖLÜM 9: HESAP YÖNETİM SİSTEMİ
# ═══════════════════════════════════════════════════════════════════

class AccountManager:
    """Hesap yönetimi"""

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
        """Hesapları görüntüle"""
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
        """Hesap yönetimi menü döngüsü"""
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
# 🔐 BÖLÜM 10: API VE İŞ MANTIĞI
# ═══════════════════════════════════════════════════════════════════

# API URL'leri (boşluksuz)
API_LOGIN = "https://slotfruits.com/api/v1/users/signupFaucetPayLogin"
API_SPIN = "https://slotfruits.com/api/v1/users/earnRoll"
ADS_URL = (
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

def get_session():
    """Retry mekanizmalı session"""
    s = requests.Session()
    r = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
    a = HTTPAdapter(max_retries=r)
    s.mount("https://", a)
    s.mount("http://", a)
    return s

def api_login(email, password):
    """FaucetPay email + şifre girişi"""
    Animator.spinner("Authenticating", duration=1.0, color=T.accent)

    payload = {"email": email.strip(), "password": password.strip()}
    headers = {
        "User-Agent": "okhttp/4.12.0",
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json"
    }

    try:
        resp = get_session().post(API_LOGIN, json=payload, headers=headers, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        token = data.get("token")
        user = data.get("user", {})
        if not token:
            return None
        return {
            "token": token,
            "user_id": user.get("_id"),
            "balance": user.get("balance", 0),
            "credits": int(user.get("credits", 0)),
            "email": email
        }
    except Exception as e:
        print(f"{T.error}❌ Login Error: {str(e)}{C.RESET}")
        return None

def api_spin(info):
    """Spin döngüsü"""
    token = info["token"]
    email = info["email"]
    credits = info["credits"]
    balance = info["balance"]
    total_reward = 0
    spins = 0
    stuck = 0

    if credits <= 0:
        print(f"{T.warning}⚠️  No credits. Watch ads first!{C.RESET}")
        return balance, credits, 0, 0

    print(f"\n{T.accent}🎰 Starting Spin Loop ({credits} credits)...{C.RESET}\n")

    while credits > 0:
        try:
            hdrs = {
                "Authorization": f"Bearer {token}",
                "User-Agent": "okhttp/4.12.0",
                "Accept": "application/json, text/plain, */*"
            }
            r = get_session().get(API_SPIN, headers=hdrs, timeout=10)
            r.raise_for_status()
            data = r.json()

            reward = data.get("total", 0)
            u = data.get("user", {})
            new_cred = int(u.get("credits", 0))
            new_bal = u.get("balance", balance)

            if new_cred >= credits and data.get("success") is not True:
                stuck += 1
                if stuck > 2:
                    print(f"{T.warning}⚠️  API stopped rewards{C.RESET}")
                    break
            else:
                stuck = 0

            credits = new_cred
            balance = new_bal
            total_reward += reward
            spins += 1

            # Canlı gösterim
            TerminalManager.clear()
            print(VisualComponents.status_bar())
            print()
            print(Drawer.line("═", color=T.primary))
            print(Drawer.center(f"{T.accent}{C.BOLD}🎰 SPINNING | {email}{C.RESET}"))
            print(Drawer.line("═", color=T.primary))
            print()
            print(VisualComponents.stats_grid({
                "Balance": (balance, "💰", T.success),
                "Reward": (f"+{reward}", "🎁", T.accent),
                "Spins": (spins, "📊", T.info),
                "Total": (total_reward, "💎", T.warning),
                "Credits": (credits, "⏳", T.primary),
                "Time": (datetime.now().strftime("%H:%M:%S"), "🕐", T.dim),
            }))
            print()
            print(Animator.progress_bar(int(spins * 10), 40, "Progress"))
            print()

            if data.get("message"):
                print(f"{T.info}ℹ️  {data['message']}{C.RESET}")

            print(Drawer.line("═", color=T.primary))
            time.sleep(1.2)

        except requests.exceptions.ConnectionError:
            print(f"{T.error}⚠️  Connection lost. Retrying...{C.RESET}")
            time.sleep(5)
        except Exception as e:
            print(f"{T.error}⚠️  Spin Error: {str(e)}{C.RESET}")
            time.sleep(3)

    return balance, credits, spins, total_reward

def api_ads(uid):
    """Reklam izleme"""
    if not uid:
        print(f"{T.error}❌ No User ID{C.RESET}")
        return 0

    print(f"\n{T.accent}🚀 Starting Ads Farming...{C.RESET}")
    hdrs = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 12; SM-A217F Build/SP1A.210812.016; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/147.0.7727.111 Mobile Safari/537.36",
        "sec-ch-ua-platform": '"Android"',
        "sec-ch-ua-mobile": "?1",
        "x-requested-with": "com.piratebaixe.slotMobile",
        "sec-fetch-site": "same-origin",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer": "https://googleads.g.doubleclick.net/mads/static/sdk/native/sdk-core-v40.html",
        "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
        "priority": "u=1, i",
        "Cookie": "IDE=AHWqTUmPTIJAy-Z7wZUR-Si3c3uYRcuBwUfjmr_ffdlWQMrcruxMTVUyL8XPtA-y_Dk"
    }

    watched = 0
    try:
        r = get_session().get(ADS_URL, headers=hdrs, timeout=15)
        if "application/json" in r.headers.get("Content-Type", ""):
            nets = r.json().get("ad_networks", [])
            if nets:
                for vurl in nets[0].get("video_reward_urls", []):
                    p = urlparse(vurl)
                    q = parse_qs(p.query, keep_blank_values=True)
                    q["rwd_userid"] = [uid]
                    nu = urlunparse(p._replace(query=urlencode(q, doseq=True)))
                    rr = get_session().get(nu, headers=hdrs, timeout=10)
                    watched += 1
                    print(f"{T.success}✔ Ad #{watched} Watched ({rr.status_code}){C.RESET}")
                    time.sleep(2)
        else:
            print(f"{T.warning}⚠️  Ads returned non-JSON{C.RESET}")
    except requests.exceptions.ConnectionError:
        print(f"{T.error}❌ DNS/Connection Error{C.RESET}")
    except Exception as e:
        print(f"{T.error}❌ Ads Error: {str(e)}{C.RESET}")

    print(f"{T.success}✅ Ads done: {watched} watched{C.RESET}")
    return watched

def process_account(email, password):
    """Tek hesap işleme"""
    print(f"\n{T.accent}🔄 Processing: {email}{C.RESET}")
    info = api_login(email, password)
    if not info:
        print(f"{T.error}⏭️  Skipping {email}{C.RESET}")
        time.sleep(2)
        return

    TerminalManager.clear()
    print(VisualComponents.status_bar())
    print()
    print(VisualComponents.info_card(
        "ACCOUNT INFO",
        [
            ("📧 Email", info['email']),
            ("💰 Balance", info['balance']),
            ("🎰 Credits", info['credits']),
            ("🆔 User ID", info['user_id'][:12] + "..." if info['user_id'] else "N/A"),
        ],
        "👤"
    ))
    print()

    bal, cred, spins, rew = api_spin(info)
    ads = api_ads(info["user_id"])
    StatsManager.update(email, spins, rew, ads)

    print()
    print(VisualComponents.notification(
        "CYCLE COMPLETE",
        f"{spins} spins | {rew} reward | {ads} ads",
        "success"
    ))
    print(f"\n{T.warning}⏳ Cooldown 10s...{C.RESET}")
    time.sleep(10)

# ═══════════════════════════════════════════════════════════════════
# 🎯 BÖLÜM 11: ANA MENÜ VE BAŞLATMA
# ═══════════════════════════════════════════════════════════════════

def start_single():
    """Tek hesap başlat"""
    accs = AccountManager.list_all()
    if not accs:
        print(VisualComponents.notification("ERROR", "No accounts! Add one in Settings", "error"))
        time.sleep(2)
        return

    TerminalManager.clear()
    print(VisualComponents.header("SELECT ACCOUNT", "Choose an account to run", "4.0"))
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
        email = keys[int(ch) - 1]
        process_account(email, accs[email])
    except:
        print(f"{T.error}Invalid choice{C.RESET}")
        time.sleep(1)

def start_multi():
    """Çoklu hesap başlat"""
    accs = AccountManager.list_all()
    if not accs:
        print(VisualComponents.notification("ERROR", "No accounts!", "error"))
        time.sleep(2)
        return

    TerminalManager.clear()
    print(VisualComponents.header("MULTI-ACCOUNT MODE", f"Processing {len(accs)} accounts", "4.0"))
    print()
    print(VisualComponents.notification("INFO", "Starting all accounts sequentially...", "info"))
    print()

    for email, pwd in accs.items():
        process_account(email, pwd)

    print()
    Effects.confetti(duration=1.5)
    print(VisualComponents.notification("SUCCESS", "All accounts processed!", "success"))
    time.sleep(3)

def settings_menu():
    """Ayarlar menüsü"""
    while True:
        TerminalManager.clear()
        print(VisualComponents.header("SETTINGS", "Configuration & Accounts", "4.0"))
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
            print(VisualComponents.header("THEME SELECTOR", "Choose your style", "4.0"))
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
                print(VisualComponents.notification("SUCCESS", f"Theme changed to {themes[int(th_ch)-1]}", "success"))
                time.sleep(1)
            except:
                print(f"{T.error}Invalid{C.RESET}")
                time.sleep(1)
        elif ch == '3':
            StatsManager.display_dashboard()
        elif ch == '4':
            TerminalManager.clear()
            print(VisualComponents.header("SYSTEM INFO", "", "4.0"))
            print()
            info_lines = [
                f"🎰 Bot: FruitClaim Pro v4.0",
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
    """Ana fonksiyon"""
    TerminalManager.set_title("FruitClaim Pro v4.0 - AlperenThe")

    # Splash screen
    TerminalManager.clear()
    print(VisualComponents.splash_screen())
    time.sleep(1)

    # Loading animasyonu
    Animator.loading_sequence([
        "Loading core modules",
        "Initializing UI system",
        "Connecting to API",
        "Preparing dashboard",
        "System ready"
    ], delay=0.4)

    time.sleep(0.5)
    Effects.confetti(duration=0.8)

    # Ana döngü
    while True:
        TerminalManager.clear()
        print(VisualComponents.status_bar())
        print()
        print(VisualComponents.header("FRUITCLAIM PRO", "Ultra Premium Multi-Account Bot", "4.0"))
        print()

        # ASCII logo
        w = TerminalManager.width()
        for line in ASCIIArt.LOGO_BIG.split('\n'):
            print(Drawer.center(f"{T.accent}{line}{C.RESET}", w))
        print()

        items = [
            ("1", "START ONE ACCOUNT", "🎯"),
            ("2", "START MULTI ACCOUNT", "🚀"),
            ("3", "SETTINGS & ACCOUNTS", "⚙️"),
            ("4", "VIEW STATISTICS", "📊"),
            ("5", "EXIT SYSTEM", "🚪"),
        ]
        print(VisualComponents.menu("MAIN MENU", items, "Select an option to continue"))
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
            print(VisualComponents.header("GOODBYE", "Thanks for using FruitClaim Pro", "4.0"))
            print()
            print(Drawer.center(f"{T.accent}👋 See you soon!{C.RESET}"))
            print()
            Effects.confetti(duration=1.0)
            break
        else:
            print(VisualComponents.notification("ERROR", "Invalid option!", "error"))
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        TerminalManager.show_cursor()
        print(f"\n\n{T.warning}🛑 Stopped by user{C.RESET}")
    except Exception as e:
        TerminalManager.show_cursor()
        print(f"\n{T.error}💥 Fatal: {str(e)}{C.RESET}")
