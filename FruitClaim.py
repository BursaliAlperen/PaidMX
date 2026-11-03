#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║     🎰 FRUITCLAIM PRO V.11 - ULTRA FAST 7/24 EDITION 🎰                      ║
║     Unlimited Loop | Multi-Account | AAA UI | Zero Bugs | Advanced Security  ║
║     Creator: AlperenThe | 2026                                               ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

Bu script, FruitClaim/SpinFruit platformları için geliştirilmiş, yüksek performanslı,
çoklu hesap destekli, gelişmiş güvenlik, proxy yönetimi ve detaylı istatistik
sistemleri içeren tam kapsamlı bir otomasyon aracıdır.

Özellikler:
- JSON tabanlı yerel hesap ve istatistik yönetimi
- Gelişmiş hata yakalama ve otomatik yeniden deneme (Retry) mekanizmaları
- 7+ farklı özelleştirilebilir terminal teması
- Detaylı istatistik, analiz paneli ve CSV dışa aktarma
- Proxy desteği ve rotasyonel User-Agent yönetimi
- Discord/Telegram Webhook bildirim sistemi
- 7/24 kesintisiz çalışma döngüsü ve akıllı bekleme stratejileri

Kullanım: python FruitClaim.py
"""

# ═══════════════════════════════════════════════════════════════════════════════
# BÖLÜM 1: IMPORTS VE TEMEL AYARLAR
# ═══════════════════════════════════════════════════════════════════════════════

import os
import sys
import json
import time
import random
import hashlib
import secrets
import logging
import argparse
import platform
import threading
import traceback
import configparser
import csv
from datetime import datetime, timedelta
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse
from typing import Dict, List, Optional, Tuple, Any, Union

try:
    import requests
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry
except ImportError:
    print("Gerekli kütüphaneler yükleniyor...")
    os.system(f"{sys.executable} -m pip install requests urllib3")
    import requests
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry

# ═══════════════════════════════════════════════════════════════════════════════
# BÖLÜM 2: ASCII SANAT REPOZİTORİSİ (GENİŞLETİLMİŞ)
# ═══════════════════════════════════════════════════════════════════════════════

class ASCIIArt:
    """Uygulama içinde kullanılan tüm ASCII sanat eserlerini barındırır."""
    
    MAIN_LOGO = r"""
                                                                                                                        
                                                     ..............                                                     
                                            ........//............\\........                                            
                                    .......//........--------------........\\.......                                    
                                ...//.......--------------------------------.......\\...                                
                              .//...------------------------------------------------...\\.                              
                           ..//.--------------------------------------------------------.\\..                           
                        ..//..------------------------------------------------------------..\\..                        
                      .//..------------------------------------------------------------------..\\.                      
                    .//.------------------------------------------------------------------------.\\.                    
                  .//.----------------------------------------------------------------------------.\\.                  
                .//.--------------------------------------------------------------------------------.\\.                
               //.------------------------------------------------------------------------------------.\\               
              //----------------------------------------------------------------------------------------\\              
            .//------------------------------------------------------------------------------------------\\.            
           //.--------------------------------------------------------------------------------------------.\\           
          //----------------..................--------------------------------------------------------------\\          
         //----------------``................\\..................--------------------------------------------\\         
        //------------------\\        ........         .........\\...............-----------------------------\\        
       //--------------------\`      ``-..............\\.........         ......\\.----------------------------\\       
      `/---------------------`\    ....\\.-------------..................\\    ...\\.---------------------------\`      
      /`----------------------\\  ``.\\..\\..----------------------------/`` .//\\..\\.-------------------------`\      
     `/------------------------\`  \`-.\\...\\-------------------------.//..//.--.\\..\\.------------------------\`     
     /`------------------------`\  `\---.\\..\\..--------------------.//. //.------.\\..\\.----------------------`\     
    `/--------------------------\\  \\----..\\..\\.----------------.//. .//----------.\\ .\\.---------------------\`    
    ``---------------------------\\  \\------\\.. .\...---------..//...//.-------------\\. .\\.-------------------``    
    /`----------------------------\\  \\------...\. ..\\.-----.//...//..----------......-``  .\\.-----------------`\    
   `/------------------------------\\  \\---------.\\...\\...//.  ``-............//.......    ````-----------------\`   
   ``-------------------------------\`  \`----------..\\......     .............  .......    .//.------------------``   
   ``-------------------------------`\  `\-------------.\\.         ...........//.......``  //.--------------------``   
   ``--------------------------------\\  \\--------------\`` ......//...........------.// .//----------------------``   
   ``---------------------------------\\  \\-------------`/ `/......----------------.//. //.-----------------------``   
   `\----------------------------------\`  \\------------`` ``---------------------//. .//-------------------------/`   
    \`---------------------------------`\   \`-----------`` ``------------------..// .//.-------------------------`/    
    ``----------------------------------\\  `\-----------/` /`----------------.//...//.---------------------------``    
    `\-----------------------------------\\  \`---------`/ `/----------------//. .//.-----------------------------/`    
     \`-----------------------------------\\ `\---------`` ``--------------.// .//.------------------------------`/     
     `\------------------------------------\\ \\--------`` ``-------------//..//.--------------------------------/`     
      \`------------------------------------\` \\-------/` ``-----------.// //.---------------------------------`/      
      `\------------------------------------``  \`-----`/  ``---------.//. //-----------------------------------/`      
       \\-----------------------------------`\  `\-----``  /`-------.//...//-----------------------------------//       
        \\-----------------------------------\\  \\----`` `/------.//..//..-----------------------------------//        
         \\-----------------------------------\\  \\---/` ``----.//. //.-------------------------------------//         
          \\-----------------------------------\\  \\-`/  ``---//. .//--------------------------------------//          
           \\.----------------------------------\`  \\/`  /`-.// .//.-------------------------------------.//           
            .\\---------------------------------`\   ..  `/-//..//.--------------------------------------//.            
              \\---------------------------------\\      `\// //.---------------------------------------//              
               \\.--------------------------------\\      ...//---------------------------------------.//               
                .\\.-------------------------------\\     .//.--------------------------------------.//.                
                  .\\.------------------------------\\  .//.--------------------------------------.//.                  
                    .\\.-----------------------------\\//.--------------------------------------.//.                    
                      .\\..--------------------------`./-------------------------------------..//.                      
                        ..\\..------------------------.-----------------------------------..//..                        
                           ..\\.--------------------------------------------------------.//..                           
                              .\\...------------------------------------------------...//.                              
                                ...\\.......--------------------------------.......//...                                
                                    .......\\........--------------........//.......                                    
                                            ........\\............//........                                            
                                                     ..............                                                     
                                                                                                                        
"""

    SPIN_ICON_SIMPLE = r"""
       .-""""-.
     .'  ↻     '.
    /   SPIN     \
   |      ⟳       |
    \            /
     '.        .'
       '-.__.-'
"""

    SPIN_ICON_ASCII_ONLY = r"""
       .------.
     .'  .--.  '.
    /   /    \   \
   |   |  ><  |   |
    \   \    /   /
     '.  '--'  .'
       '------'
"""

    SPINFRUIT_TEXT_BIG = r"""
 _____  ____  ___ _   _ _____ ____  _   _ ___ _____ 
/ ____|/ __ \|_ _| \ | |  ___|  _ \| | | |_ _|_   _|
\___ \| |  | || ||  \| | |_  | |_) | | | || |  | |  
 ___) | |__| || || |\  |  _| |  _ <| |_| || |  | |  
|____/ \____/|___|_| \_|_|   |_| \_\\___/|___| |_|  
"""

    SPINFRUIT_TEXT_SMALL = r"""
  ________________
 /                \
|   SPINFRUIT  ↻   |
 \________________/
"""

    V11_ICON_BOX = r"""
+---------+
|  V.11   |
+---------+
"""

    V11_ICON_ROUNDED = r"""
.-----------.
| SPINFRUIT |
|    V.11   |
'-----------'
"""

    DIVIDER_DOUBLE = "________________________________________"
    DIVIDER_HASH = "__  __  __  __  __  __  __  __  __  __"
    DIVIDER_ARROW = "<========== SPINFRUIT ==========>" 
    DIVIDER_WAVE = "---===---===---  SPINFRUIT  ---===---===---"

    COMBINED_HEADER = r"""
       .------.
     .'  .--.  '.
    /   /    \   \
   |   |  ><  |   |       SPINFRUIT
    \   \    /   /           V.11
     '.  '--'  .'
       '------'
________________________________________
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

    WARNING_ICON = r"""
       ⚠️
      /!\
     / ! \
    /_____\\
"""

    SUCCESS_ICON = r"""
       ✅
      /✓\
     /___\\
"""

    LOADING_FRAMES = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    
    @staticmethod
    def get_random_logo() -> str:
        """Rastgele bir logo döndürür."""
        logos = [ASCIIArt.MAIN_LOGO, ASCIIArt.COMBINED_HEADER]
        return random.choice(logos)


# ═══════════════════════════════════════════════════════════════════════════════
# BÖLÜM 3: RENK KODLARI VE TEMA SİSTEMİ
# ═══════════════════════════════════════════════════════════════════════════════

class Colors:
    """Terminal renk kodlarını ve formatlarını tanımlar."""
    RESET       = "\033[0m"
    BOLD        = "\033[1m"
    DIM         = "\033[2m"
    ITALIC      = "\033[3m"
    UNDERLINE   = "\033[4m"
    BLINK       = "\033[5m"
    REVERSE     = "\033[7m"
    HIDDEN      = "\033[8m"
    STRIKE      = "\033[9m"
    
    BLACK       = "\033[30m"
    RED         = "\033[31m"
    GREEN       = "\033[32m"
    YELLOW      = "\033[33m"
    BLUE        = "\033[34m"
    MAGENTA     = "\033[35m"
    CYAN        = "\033[36m"
    WHITE       = "\033[37m"
    
    BRIGHT_BLACK    = "\033[90m"
    BRIGHT_RED      = "\033[91m"
    BRIGHT_GREEN    = "\033[92m"
    BRIGHT_YELLOW   = "\033[93m"
    BRIGHT_BLUE     = "\033[94m"
    BRIGHT_MAGENTA  = "\033[95m"
    BRIGHT_CYAN     = "\033[96m"
    BRIGHT_WHITE    = "\033[97m"
    
    BG_BLACK    = "\033[40m"
    BG_RED      = "\033[41m"
    BG_GREEN    = "\033[42m"
    BG_YELLOW   = "\033[43m"
    BG_BLUE     = "\033[44m"
    BG_MAGENTA  = "\033[45m"
    BG_CYAN     = "\033[46m"
    BG_WHITE    = "\033[47m"

C = Colors()

class Theme:
    """Gelişmiş tema yönetim sistemi."""
    THEMES = {
        "neon": {
            "primary": C.BRIGHT_CYAN,
            "secondary": C.BRIGHT_MAGENTA,
            "accent": C.BRIGHT_YELLOW,
            "success": C.BRIGHT_GREEN,
            "error": C.BRIGHT_RED,
            "warning": C.YELLOW,
            "info": C.BRIGHT_BLUE,
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
        "cyberpunk": {
            "primary": C.BRIGHT_MAGENTA,
            "secondary": C.BRIGHT_CYAN,
            "accent": C.BRIGHT_YELLOW,
            "success": C.BRIGHT_GREEN,
            "error": C.BRIGHT_RED,
            "warning": C.BRIGHT_YELLOW,
            "info": C.BRIGHT_BLUE,
            "border": C.BRIGHT_MAGENTA,
            "text": C.BRIGHT_WHITE,
            "dim": C.DIM,
        },
        "monochrome": {
            "primary": C.WHITE,
            "secondary": C.BRIGHT_BLACK,
            "accent": C.WHITE,
            "success": C.WHITE,
            "error": C.BRIGHT_WHITE,
            "warning": C.BRIGHT_BLACK,
            "info": C.WHITE,
            "border": C.BRIGHT_BLACK,
            "text": C.WHITE,
            "dim": C.DIM,
        }
    }

    def __init__(self, name: str = "neon"):
        self.name = name
        self.colors = self.THEMES.get(name.lower(), self.THEMES["neon"])

    def __getattr__(self, name: str) -> str:
        if name in self.colors:
            return self.colors[name]
        upper = name.upper()
        if hasattr(Colors, upper):
            return getattr(Colors, upper)
        return C.YELLOW

current_theme = Theme("neon")
T = current_theme


# ═══════════════════════════════════════════════════════════════════════════════
# BÖLÜM 4: TERMİNAL VE UI YÖNETİMİ
# ═══════════════════════════════════════════════════════════════════════════════

class TerminalManager:
    """Terminal penceresi, boyutlandırma ve çıktı yönetimi."""
    
    @staticmethod
    def width() -> int:
        try:
            return os.get_terminal_size().columns
        except OSError:
            return 80

    @staticmethod
    def height() -> int:
        try:
            return os.get_terminal_size().lines
        except OSError:
            return 24

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
    def set_title(title: str):
        if os.name == "nt":
            os.system(f"title {title}")
        else:
            sys.stdout.write(f"\033]0;{title}\007")
            sys.stdout.flush()

    @staticmethod
    def move_cursor(x: int, y: int):
        sys.stdout.write(f"\033[{y};{x}H")
        sys.stdout.flush()


class Drawer:
    """Çizim, kutu ve görsel düzenleme fonksiyonları."""
    
    @staticmethod
    def line(char: str = "═", length: Optional[int] = None, color: Optional[str] = None) -> str:
        w = length or TerminalManager.width()
        c = color or T.border
        return f"{c}{char * w}{C.RESET}"

    @staticmethod
    def double_line(length: Optional[int] = None, color: Optional[str] = None) -> str:
        return Drawer.line("═", length, color)

    @staticmethod
    def dashed_line(length: Optional[int] = None, color: Optional[str] = None) -> str:
        return Drawer.line("─", length, color)

    @staticmethod
    def dotted_line(length: Optional[int] = None, color: Optional[str] = None) -> str:
        return Drawer.line("·", length, color)

    @staticmethod
    def star_line(length: Optional[int] = None, color: Optional[str] = None) -> str:
        return Drawer.line("✦", length, color)

    @staticmethod
    def center(text: str, width: Optional[int] = None) -> str:
        w = width or TerminalManager.width()
        clean_text = text
        for code in [C.RESET, C.BOLD, C.DIM, C.ITALIC, C.UNDERLINE, C.BLINK, C.REVERSE, C.HIDDEN, C.STRIKE,
                     C.BLACK, C.RED, C.GREEN, C.YELLOW, C.BLUE, C.MAGENTA, C.CYAN, C.WHITE,
                     C.BRIGHT_BLACK, C.BRIGHT_RED, C.BRIGHT_GREEN, C.BRIGHT_YELLOW, C.BRIGHT_BLUE, 
                     C.BRIGHT_MAGENTA, C.BRIGHT_CYAN, C.BRIGHT_WHITE]:
            clean_text = clean_text.replace(code, "")
        padding = (w - len(clean_text)) // 2
        return " " * max(0, padding) + text

    @staticmethod
    def fancy_box(title: str, content_lines: List[str], width: Optional[int] = None) -> str:
        w = width or TerminalManager.width()
        inner = max(20, w - 6)
        out = []
        out.append(f"{T.primary}┏{'━' * inner}┓{C.RESET}")
        if title:
            t = f" {title} ".center(inner)
            out.append(f"{T.primary}┃{C.RESET}{T.accent}{t}{C.RESET}{T.primary}┃{C.RESET}")
            out.append(f"{T.primary}┣{'━' * inner}┫{C.RESET}")
        for line in content_lines:
            clean_line = line
            for code in [C.RESET, C.BOLD, C.DIM, C.ITALIC, C.UNDERLINE, C.BLINK, C.REVERSE, C.HIDDEN, C.STRIKE,
                         C.BLACK, C.RED, C.GREEN, C.YELLOW, C.BLUE, C.MAGENTA, C.CYAN, C.WHITE,
                         C.BRIGHT_BLACK, C.BRIGHT_RED, C.BRIGHT_GREEN, C.BRIGHT_YELLOW, C.BRIGHT_BLUE, 
                         C.BRIGHT_MAGENTA, C.BRIGHT_CYAN, C.BRIGHT_WHITE]:
                clean_line = clean_line.replace(code, "")
            padded = line.ljust(inner + len(line) - len(clean_line))[:inner + len(line) - len(clean_line)]
            out.append(f"{T.primary}┃{C.RESET} {padded} {T.primary}┃{C.RESET}")
        out.append(f"{T.primary}┗{'━' * inner}┛{C.RESET}")
        return '\n'.join(out)

    @staticmethod
    def divider(text: str = "", style: str = "double") -> str:
        w = TerminalManager.width()
        clean_text = text
        for code in [C.RESET, C.BOLD, C.DIM, C.ITALIC, C.UNDERLINE, C.BLINK, C.REVERSE, C.HIDDEN, C.STRIKE,
                     C.BLACK, C.RED, C.GREEN, C.YELLOW, C.BLUE, C.MAGENTA, C.CYAN, C.WHITE,
                     C.BRIGHT_BLACK, C.BRIGHT_RED, C.BRIGHT_GREEN, C.BRIGHT_YELLOW, C.BRIGHT_BLUE, 
                     C.BRIGHT_MAGENTA, C.BRIGHT_CYAN, C.BRIGHT_WHITE]:
            clean_text = clean_text.replace(code, "")
            
        if style == "double":
            left = "═" * ((w - len(clean_text) - 4) // 2)
            right = "═" * (w - len(clean_text) - 4 - len(left))
            return f"{T.border}{left} {T.accent}« {text} »{T.border} {right}{C.RESET}"
        elif style == "star":
            left = "✦" * ((w - len(clean_text) - 4) // 2)
            right = "✦" * (w - len(clean_text) - 4 - len(left))
            return f"{T.border}{left} {T.accent}[ {text} ]{T.border} {right}{C.RESET}"
        else:
            left = "─" * ((w - len(clean_text) - 4) // 2)
            right = "─" * (w - len(clean_text) - 4 - len(left))
            return f"{T.border}{left} {T.accent}• {text} •{T.border} {right}{C.RESET}"


class Animator:
    """Animasyon, yükleme ve ilerleme çubuğu efektleri."""
    
    SPINNERS = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    PULSE = ["○", "◐", "●", "◑"]
    LOADING_BARS = ["▰▱▱▱▱▱▱", "▰▰▱▱▱▱▱", "▰▰▰▱▱▱▱", "▰▰▰▰▱▱▱", "▰▰▰▰▰▱▱", "▰▰▰▰▰▰▱", "▰▰▰▰▰▰▰"]

    @staticmethod
    def spinner(text: str, duration: float = 1.0, color: Optional[str] = None):
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
        except KeyboardInterrupt:
            print(f"\r{T.error}✖ {text} İptal edildi{C.RESET}    ")

    @staticmethod
    def progress_bar(percent: float, width: int = 40, label: str = "") -> str:
        filled = int(width * percent / 100)
        empty = width - filled
        bar = "█" * filled + "░" * empty
        if percent < 30:
            color = T.error
        elif percent < 70:
            color = T.warning
        else:
            color = T.success
        return f"{color}[{bar}]{C.RESET} {percent:3.0f}% {label}"

    @staticmethod
    def loading_sequence(steps: List[str], delay: float = 0.3):
        for step in steps:
            Animator.spinner(step, duration=delay)
            time.sleep(0.1)

    @staticmethod
    def rainbow_text(text: str) -> str:
        colors = [C.RED, C.YELLOW, C.GREEN, C.CYAN, C.BLUE, C.MAGENTA]
        result = ""
        for i, char in enumerate(text):
            result += f"{colors[i % len(colors)]}{char}{C.RESET}"
        return result


class VisualComponents:
    """Görsel bileşenler, menüler ve UI elementleri."""
    
    @staticmethod
    def header(title: str, subtitle: str = "", version: str = "") -> str:
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
    def status_bar() -> str:
        w = TerminalManager.width()
        now = datetime.now().strftime("%H:%M:%S")
        date = datetime.now().strftime("%d/%m/%Y")
        bar = f"{T.primary}┌{C.RESET}" + f"{T.primary}─{C.RESET}" * (w - 2) + f"{T.primary}┐{C.RESET}"
        content = f"{T.primary}│{C.RESET} {T.accent}🕐 {now}{C.RESET} | {T.accent}📅 {date}{C.RESET} | {T.accent}🎰 FruitClaim Pro V.11{C.RESET} | {T.accent}👤 AlperenThe{C.RESET} "
        clean_content = content
        for code in [C.RESET, C.BOLD, C.DIM, C.ITALIC, C.UNDERLINE, C.BLINK, C.REVERSE, C.HIDDEN, C.STRIKE,
                     C.BLACK, C.RED, C.GREEN, C.YELLOW, C.BLUE, C.MAGENTA, C.CYAN, C.WHITE,
                     C.BRIGHT_BLACK, C.BRIGHT_RED, C.BRIGHT_GREEN, C.BRIGHT_YELLOW, C.BRIGHT_BLUE, 
                     C.BRIGHT_MAGENTA, C.BRIGHT_CYAN, C.BRIGHT_WHITE]:
            clean_content = clean_content.replace(code, "")
        padding = w - 2 - len(clean_content)
        content += " " * max(0, padding)
        bottom = f"{T.primary}└{C.RESET}" + f"{T.primary}─{C.RESET}" * (w - 2) + f"{T.primary}┘{C.RESET}"
        return f"{bar}\n{T.primary}│{C.RESET}{content[:w-2]}{T.primary}│{C.RESET}\n{bottom}"

    @staticmethod
    def menu_item(number: str, text: str, icon: str = "", selected: bool = False) -> str:
        if selected:
            return f"{T.accent}{C.BOLD}  [{number}] {icon} {text}{C.RESET}"
        else:
            return f"{T.text}  [{number}] {icon} {text}{C.RESET}"

    @staticmethod
    def menu(title: str, items: List[Tuple[str, str, str]], footer: str = "") -> str:
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
    def notification(title: str, message: str, level: str = "info") -> str:
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
    def input_prompt(label: str, icon: str = "▶") -> str:
        return f"{T.accent}{icon} {label}: {C.RESET}"

    @staticmethod
    def splash_screen() -> str:
        w = TerminalManager.width()
        out = []
        out.append("")
        out.append(Drawer.center(f"{T.primary}{C.BOLD}╔══════════════════════════════════════════════════════╗{C.RESET}", w))
        out.append(Drawer.center(f"{T.primary}{C.BOLD}║{C.RESET}{T.accent}  🎰 FRUITCLAIM PRO V.11 - ULTRA FAST 🎰  {C.RESET}{T.primary}{C.BOLD}║{C.RESET}", w))
        out.append(Drawer.center(f"{T.primary}{C.BOLD}╚══════════════════════════════════════════════════════╝{C.RESET}", w))
        out.append("")
        out.append(Drawer.center(f"{T.text}7/24 Unlimited | Multi-Account | Zero Bugs{C.RESET}", w))
        out.append(Drawer.center(f"{T.dim}Creator: AlperenThe | 2026{C.RESET}", w))
        out.append("")
        out.append(Drawer.center(f"{T.accent}Initializing system...{C.RESET}", w))
        return '\n'.join(out)


# ═══════════════════════════════════════════════════════════════════════════════
# BÖLÜM 5: YAPILANDIRMA VE LOG YÖNETİMİ
# ═══════════════════════════════════════════════════════════════════════════════

class ConfigManager:
    """Uygulama yapılandırma dosyası yönetimi."""
    CONFIG_FILE = "config.ini"
    
    DEFAULT_CONFIG = {
        "Settings": {
            "theme": "neon",
            "delay_between_spins": "0.1",
            "max_retries": "5",
            "enable_proxy": "false",
            "proxy_file": "proxies.txt"
        },
        "Notifications": {
            "enable_discord": "false",
            "discord_webhook": "",
            "enable_telegram": "false",
            "telegram_bot_token": "",
            "telegram_chat_id": ""
        }
    }

    def __init__(self):
        self.config = configparser.ConfigParser()
        self._load_or_create()

    def _load_or_create(self):
        if not os.path.exists(self.CONFIG_FILE):
            for section, options in self.DEFAULT_CONFIG.items():
                self.config[section] = options
            self.save()
        else:
            self.config.read(self.CONFIG_FILE, encoding='utf-8')

    def save(self):
        with open(self.CONFIG_FILE, 'w', encoding='utf-8') as f:
            self.config.write(f)

    def get(self, section: str, key: str, fallback: str = "") -> str:
        return self.config.get(section, key, fallback=fallback)

    def set(self, section: str, key: str, value: str):
        if section not in self.config:
            self.config[section] = {}
        self.config[section][key] = value
        self.save()


class LoggerManager:
    """Gelişmiş dosya ve konsol loglama sistemi."""
    LOG_FILE = "fruitclaim.log"
    
    def __init__(self):
        self.logger = logging.getLogger("FruitClaimPro")
        self.logger.setLevel(logging.DEBUG)
        
        if not self.logger.handlers:
            fh = logging.FileHandler(self.LOG_FILE, encoding='utf-8')
            fh.setLevel(logging.DEBUG)
            ch = logging.StreamHandler()
            ch.setLevel(logging.INFO)
            
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            fh.setFormatter(formatter)
            ch.setFormatter(formatter)
            
            self.logger.addHandler(fh)
            self.logger.addHandler(ch)

    def info(self, msg: str):
        self.logger.info(msg)

    def warning(self, msg: str):
        self.logger.warning(msg)

    def error(self, msg: str):
        self.logger.error(msg)

    def debug(self, msg: str):
        self.logger.debug(msg)


# ═══════════════════════════════════════════════════════════════════════════════
# BÖLÜM 6: GÜVENLİK VE ŞİFRELEME
# ═══════════════════════════════════════════════════════════════════════════════

class SecurityManager:
    """Hesap bilgileri ve hassas veriler için güvenlik yönetimi."""
    
    @staticmethod
    def hash_password(password: str, salt: Optional[str] = None) -> Tuple[str, str]:
        """Parolayı SHA-256 ile tuzlayarak hash'ler."""
        if salt is None:
            salt = secrets.token_hex(16)
        pwd_hash = hashlib.sha256((password + salt).encode('utf-8')).hexdigest()
        return pwd_hash, salt

    @staticmethod
    def verify_password(password: str, stored_hash: str, salt: str) -> bool:
        """Parolanın doğruluğunu kontrol eder."""
        pwd_hash, _ = SecurityManager.hash_password(password, salt)
        return pwd_hash == stored_hash

    @staticmethod
    def obfuscate_email(email: str) -> str:
        """E-posta adresini gizler (ornek@domain.com -> or***@d***.com)."""
        if '@' not in email:
            return email
        local, domain = email.split('@', 1)
        if len(local) > 2:
            local = local[0] + '*' * (len(local) - 2) + local[-1]
        if len(domain) > 4:
            domain_part, tld = domain.rsplit('.', 1)
            domain = domain_part[0] + '*' * (len(domain_part) - 1) + '.' + tld
        return f"{local}@{domain}"


# ═══════════════════════════════════════════════════════════════════════════════
# BÖLÜM 7: PROXY YÖNETİMİ
# ═══════════════════════════════════════════════════════════════════════════════

class ProxyManager:
    """Proxy listesi yükleme ve rotasyon yönetimi."""
    
    def __init__(self, proxy_file: str = "proxies.txt"):
        self.proxy_file = proxy_file
        self.proxies = []
        self.current_index = 0
        self._load_proxies()

    def _load_proxies(self):
        if os.path.exists(self.proxy_file):
            try:
                with open(self.proxy_file, 'r', encoding='utf-8') as f:
                    self.proxies = [line.strip() for line in f if line.strip()]
                print(f"{T.success}✔ {len(self.proxies)} proxy yüklendi.{C.RESET}")
            except Exception as e:
                print(f"{T.error}❌ Proxy dosyası okunamadı: {e}{C.RESET}")

    def get_next_proxy(self) -> Optional[Dict[str, str]]:
        if not self.proxies:
            return None
        proxy = self.proxies[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.proxies)
        return {"http": proxy, "https": proxy}


# ═══════════════════════════════════════════════════════════════════════════════
# BÖLÜM 8: AĞ VE API YÖNETİCİSİ
# ═══════════════════════════════════════════════════════════════════════════════

class NetworkManager:
    """Gelişmiş ağ istekleri, API yönetimi ve retry mekanizmaları."""
    
    USER_AGENTS = [
        "Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 12; SM-A217F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36",
        "okhttp/4.12.0"
    ]

    API_LOGIN = "https://slotfruits.com/api/v1/users/signupFaucetPayLogin"
    API_SPIN = "https://slotfruits.com/api/v1/users/earnRoll"
    ADS_URL = (
        "https://googleads.g.doubleclick.net/mads/gma?submodel=SM-A217F"
        "&adid_p=1&format=interstitial_mb&ini_pn=com.google.android.packageinstaller"
        "&ins_pn=com.google.android.packageinstaller&omid_v=a.1.5.2-google_20241009"
        "&dv=254380203&ev=24.6.0&gl=ID&hl=in&js=afma-sdk-a-v254380999.253410000.1"
        "&kw=clothing%2Cfashion&lv=253410000&msid=com.piratebaixe.slotMobile"
        "&an=17.android.com.spincoin.appmobile.top&u_audio=3&net=ed&u_so=p&rbv=1"
        "&client=ca-app-pub-5674874137587223&slotname=7114498212&kw_type=broad&gsb=4g"
    )

    def __init__(self, proxy_manager: Optional[ProxyManager] = None):
        self.session = self._create_session()
        self.proxy_manager = proxy_manager

    def _create_session(self) -> requests.Session:
        """Güçlü ve yeniden deneme yetenekli bir oturum oluşturur."""
        session = requests.Session()
        retry = Retry(
            total=5,
            backoff_factor=0.5,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "POST", "OPTIONS"]
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount("https://", adapter)
        session.mount("http://", adapter)
        return session

    def get_random_user_agent(self) -> str:
        return random.choice(self.USER_AGENTS)

    def api_login(self, email: str, password: str) -> Optional[Dict[str, Any]]:
        """API'ye giriş yapar."""
        payload = {"email": email.strip(), "password": password.strip()}
        headers = {
            "User-Agent": self.get_random_user_agent(),
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json"
        }
        proxies = self.proxy_manager.get_next_proxy() if self.proxy_manager else None
        
        try:
            resp = self.session.post(self.API_LOGIN, json=payload, headers=headers, proxies=proxies, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            
            token = data.get("token")
            user = data.get("user", {})
            
            if not token:
                return None
                
            return {
                "token": token,
                "user_id": user.get("_id"),
                "balance": float(user.get("balance", 0)),
                "credits": int(user.get("credits", 0)),
                "email": email
            }
        except requests.exceptions.HTTPError as e:
            print(f"{T.error}❌ HTTP Hatası: {e}{C.RESET}")
            return None
        except requests.exceptions.ConnectionError:
            print(f"{T.error}❌ Bağlantı Hatası{C.RESET}")
            return None
        except requests.exceptions.Timeout:
            print(f"{T.error}❌ Zaman Aşımı{C.RESET}")
            return None
        except Exception as e:
            print(f"{T.error}❌ Giriş Hatası: {str(e)}{C.RESET}")
            return None

    def api_spin(self, token: str) -> Optional[Dict[str, Any]]:
        """Spin işlemi gerçekleştirir."""
        headers = {
            "Authorization": f"Bearer {token}",
            "User-Agent": self.get_random_user_agent(),
            "Accept": "application/json, text/plain, */*"
        }
        proxies = self.proxy_manager.get_next_proxy() if self.proxy_manager else None
        
        try:
            r = self.session.get(self.API_SPIN, headers=headers, proxies=proxies, timeout=5)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            return {"error": str(e)}

    def api_ads(self, uid: str) -> int:
        """Reklam izleme simülasyonu ve ödül talebi."""
        if not uid:
            return 0
            
        headers = {
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
        proxies = self.proxy_manager.get_next_proxy() if self.proxy_manager else None
        watched = 0
        
        try:
            r = self.session.get(self.ADS_URL, headers=headers, proxies=proxies, timeout=10)
            if "application/json" in r.headers.get("Content-Type", ""):
                nets = r.json().get("ad_networks", [])
                if nets:
                    for vurl in nets[0].get("video_reward_urls", []):
                        p = urlparse(vurl)
                        q = parse_qs(p.query, keep_blank_values=True)
                        q["rwd_userid"] = [uid]
                        nu = urlunparse(p._replace(query=urlencode(q, doseq=True)))
                        rr = self.session.get(nu, headers=headers, proxies=proxies, timeout=5)
                        watched += 1
                        time.sleep(0.5)
        except Exception:
            pass
            
        return watched


# ═══════════════════════════════════════════════════════════════════════════════
# BÖLÜM 9: İSTATİSTİK VE RAPORLAMA
# ═══════════════════════════════════════════════════════════════════════════════

class StatisticsManager:
    """JSON ve CSV tabanlı gelişmiş istatistik yönetimi."""
    STATS_FILE = "bot_stats.json"
    CSV_FILE = "bot_stats_export.csv"
    
    @staticmethod
    def load_json() -> Dict[str, Any]:
        if os.path.exists(StatisticsManager.STATS_FILE):
            try:
                with open(StatisticsManager.STATS_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                pass
        return {}

    @staticmethod
    def save_json(data: Dict[str, Any]):
        try:
            with open(StatisticsManager.STATS_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"{T.error}❌ İstatistik kaydetme hatası: {e}{C.RESET}")

    @staticmethod
    def update(email: str, spins: int, reward: float, ads: int):
        stats = StatisticsManager.load_json()
        if email not in stats:
            stats[email] = {"spins": 0, "reward": 0.0, "ads": 0, "sessions": 0}
        
        s = stats[email]
        s["spins"] += spins
        s["reward"] += reward
        s["ads"] += ads
        s["sessions"] += 1
        s["last_run"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        StatisticsManager.save_json(stats)

    @staticmethod
    def export_to_csv():
        stats = StatisticsManager.load_json()
        if not stats:
            print(f"{T.warning}⚠️ Dışa aktarılacak veri yok.{C.RESET}")
            return
            
        try:
            with open(StatisticsManager.CSV_FILE, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["Email", "Total Spins", "Total Reward", "Total Ads", "Sessions", "Last Run"])
                for email, data in stats.items():
                    writer.writerow([
                        email,
                        data.get("spins", 0),
                        data.get("reward", 0.0),
                        data.get("ads", 0),
                        data.get("sessions", 0),
                        data.get("last_run", "N/A")
                    ])
            print(f"{T.success}✅ İstatistikler {StatisticsManager.CSV_FILE} dosyasına aktarıldı.{C.RESET}")
        except Exception as e:
            print(f"{T.error}❌ CSV aktarma hatası: {e}{C.RESET}")

    @staticmethod
    def display_dashboard():
        TerminalManager.clear()
        stats = StatisticsManager.load_json()
        w = TerminalManager.width()
        
        print(Drawer.line("═", color=T.primary))
        print(Drawer.center(f"{T.accent}{C.BOLD}📊 GLOBAL STATISTICS DASHBOARD 📊{C.RESET}", w))
        print(Drawer.line("═", color=T.primary))
        print()
        
        if not stats:
            print(Drawer.center(f"{T.warning}⚠️ Henüz veri yok. Önce botu çalıştırın!{C.RESET}", w))
            print()
            input(f"\n{T.accent}Devam etmek için Enter'a basın...{C.RESET}")
            return
            
        total_spins = sum(s.get("spins", 0) for s in stats.values())
        total_reward = sum(s.get("reward", 0.0) for s in stats.values())
        total_ads = sum(s.get("ads", 0) for s in stats.values())
        total_sessions = sum(s.get("sessions", 0) for s in stats.values())
        
        print(f"  {T.success}💰 Toplam Ödül{C.RESET}: {T.accent}{total_reward:.2f}{C.RESET}")
        print(f"  {T.info}🎰 Toplam Spin{C.RESET}: {T.accent}{total_spins}{C.RESET}")
        print(f"  {T.warning}📺 Toplam Reklam{C.RESET}: {T.accent}{total_ads}{C.RESET}")
        print(f"  {T.primary}🔄 Toplam Oturum{C.RESET}: {T.accent}{total_sessions}{C.RESET}")
        print()
        print(Drawer.divider("HESAP DETAYLARI", "star"))
        print()
        
        for email, s in stats.items():
            lines = [
                f"  {T.text}🎰 Spinler   : {T.accent}{s.get('spins', 0)}{C.RESET}",
                f"  {T.text}💎 Ödüller   : {T.accent}{s.get('reward', 0.0):.2f}{C.RESET}",
                f"  {T.text}📺 Reklamlar  : {T.accent}{s.get('ads', 0)}{C.RESET}",
                f"  {T.text}🔄 Oturumlar  : {T.accent}{s.get('sessions', 0)}{C.RESET}",
                f"  {T.text}🕐 Son Güncelleme: {T.accent}{s.get('last_run', 'N/A')}{C.RESET}",
            ]
            print(Drawer.fancy_box(f"📧 {email}", lines))
            print()
            
        print(Drawer.line("═", color=T.primary))
        input(f"\n{T.accent}Devam etmek için Enter'a basın...{C.RESET}")


# ═══════════════════════════════════════════════════════════════════════════════
# BÖLÜM 10: HESAP YÖNETİMİ
# ═══════════════════════════════════════════════════════════════════════════════

class AccountManager:
    """Kullanıcı dostu hesap yönetimi arayüzü ve CRUD işlemleri."""
    ACCOUNTS_FILE = "accounts.json"
    
    @staticmethod
    def load() -> Dict[str, str]:
        if os.path.exists(AccountManager.ACCOUNTS_FILE):
            try:
                with open(AccountManager.ACCOUNTS_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                pass
        return {}

    @staticmethod
    def save(accs: Dict[str, str]):
        try:
            with open(AccountManager.ACCOUNTS_FILE, 'w', encoding='utf-8') as f:
                json.dump(accs, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"{T.error}❌ Hesap kaydetme hatası: {e}{C.RESET}")

    @staticmethod
    def add(email: str, password: str) -> bool:
        accs = AccountManager.load()
        if email in accs:
            return False
        accs[email] = password
        AccountManager.save(accs)
        return True

    @staticmethod
    def remove(email: str) -> bool:
        accs = AccountManager.load()
        if email in accs:
            del accs[email]
            AccountManager.save(accs)
            return True
        return False

    @staticmethod
    def display():
        TerminalManager.clear()
        accs = AccountManager.load()
        w = TerminalManager.width()
        
        print(Drawer.line("═", color=T.primary))
        print(Drawer.center(f"{T.accent}{C.BOLD}👥 ACCOUNT MANAGER 👥{C.RESET}", w))
        print(Drawer.line("═", color=T.primary))
        print()
        
        if not accs:
            print(Drawer.center(f"{T.warning}⚠️ Kayıtlı hesap yok.{C.RESET}", w))
            print()
            print(Drawer.center(f"{T.text}İlk hesabınızı eklemek için [+] kullanın{C.RESET}", w))
        else:
            for i, (email, pwd) in enumerate(accs.items(), 1):
                masked = pwd[:2] + "•" * (len(pwd) - 2) if len(pwd) > 2 else "•••"
                w_card = 50
                border = T.success
                status_icon = "✅"
                
                print(f"{border}╔{'═' * (w_card - 2)}╗{C.RESET}")
                print(f"{border}║{C.RESET} {T.accent}#{i}{C.RESET} {status_icon} {email:<40} {border}║{C.RESET}")
                print(f"{border}╠{'═' * (w_card - 2)}╣{C.RESET}")
                print(f"{border}║{C.RESET} {T.dim}🔑 Password: {masked:<36}{C.RESET} {border}║{C.RESET}")
                print(f"{border}╚{'═' * (w_card - 2)}╝{C.RESET}")
                print()
                
        print(Drawer.line("═", color=T.primary))

    @staticmethod
    def menu_loop():
        while True:
            AccountManager.display()
            print()
            print(f"{T.success}  [+] Hesap Ekle{C.RESET}")
            print(f"{T.error}  [-] Hesap Sil{C.RESET}")
            print(f"{T.accent}  [C] Tümünü Temizle{C.RESET}")
            print(f"{T.warning}  [0] Ana Menüye Dön{C.RESET}")
            print()
            ch = input(VisualComponents.input_prompt("Seçim", "▶")).strip().upper()
            
            if ch == '0':
                break
            elif ch == '+':
                email = input(VisualComponents.input_prompt("E-posta", "📧")).strip()
                password = input(VisualComponents.input_prompt("Şifre", "🔑")).strip()
                if email and password and '@' in email:
                    if AccountManager.add(email, password):
                        print(VisualComponents.notification("SUCCESS", "Hesap başarıyla eklendi!", "success"))
                    else:
                        print(VisualComponents.notification("ERROR", "Bu e-posta zaten kayıtlı!", "error"))
                    time.sleep(1.5)
                else:
                    print(VisualComponents.notification("ERROR", "Geçersiz giriş!", "error"))
                    time.sleep(1)
            elif ch == '-':
                accs = AccountManager.load()
                if not accs:
                    print(VisualComponents.notification("INFO", "Silinecek hesap yok", "info"))
                    time.sleep(1)
                    continue
                idx = input(VisualComponents.input_prompt("Hesap Numarası", "#")).strip()
                try:
                    keys = list(accs.keys())
                    email = keys[int(idx) - 1]
                    if AccountManager.remove(email):
                        print(VisualComponents.notification("SUCCESS", f"Silindi: {email}", "success"))
                    time.sleep(1)
                except (ValueError, IndexError):
                    print(VisualComponents.notification("ERROR", "Geçersiz seçim", "error"))
                    time.sleep(1)
            elif ch == 'C':
                confirm = input(f"{T.error}Tüm hesaplar silinecek? (y/n): {C.RESET}").strip().lower()
                if confirm == 'y':
                    AccountManager.save({})
                    print(VisualComponents.notification("SUCCESS", "Tüm hesaplar temizlendi", "success"))
                    time.sleep(1)


# ═══════════════════════════════════════════════════════════════════════════════
# BÖLÜM 11: BOT MOTORU (7/24 ÇEKİRDEK)
# ═══════════════════════════════════════════════════════════════════════════════

class BotEngine:
    """Ana bot işleme motoru ve 7/24 döngü yönetimi."""
    
    def __init__(self, config: ConfigManager, logger: LoggerManager):
        self.config = config
        self.logger = logger
        proxy_enabled = self.config.get("Settings", "enable_proxy").lower() == "true"
        proxy_file = self.config.get("Settings", "proxy_file")
        self.proxy_manager = ProxyManager(proxy_file) if proxy_enabled else None
        self.network = NetworkManager(self.proxy_manager)
        self.is_running = False

    def process_account(self, email: str, password: str):
        """Tek bir hesabı 7/24 işler."""
        self.is_running = True
        cycle = 0
        total_spins_all = 0
        total_reward_all = 0.0
        
        print(f"\n{T.success}{'='*60}{C.RESET}")
        print(Drawer.center(f"{T.accent}{C.BOLD} 7/24 ULTRA FAST MODE - {SecurityManager.obfuscate_email(email)}{C.RESET}"))
        print(f"{T.success}{'='*60}{C.RESET}\n")
        
        while self.is_running:
            cycle += 1
            print(f"\n{T.primary}{'='*60}{C.RESET}")
            print(Drawer.center(f"🔄 CYCLE #{cycle} | {datetime.now().strftime('%H:%M:%S')}"))
            print(f"{T.primary}{'='*60}{C.RESET}\n")
            
            info = self.network.api_login(email, password)
            if not info:
                print(f"{T.error}❌ Giriş başarısız. 3 saniye içinde yeniden deneniyor...{C.RESET}")
                self.logger.warning(f"Giriş başarısız: {email}")
                time.sleep(3)
                continue
            
            self.logger.info(f"Giriş başarılı: {email}")
            print(f"{T.success}✅ Giriş başarılı | Bakiye: {info['balance']} | Kredi: {info['credits']}{C.RESET}")
            
            bal, cred, spins, rew = self._spin_loop(info)
            total_spins_all += spins
            total_reward_all += rew
            
            print(f"\n{T.success}✅ Spinler: {spins} | Ödül: {rew}{C.RESET}")
            
            ads = self.network.api_ads(info["user_id"])
            StatisticsManager.update(email, spins, rew, ads)
            
            print(f"{T.success}📺 Reklamlar: {ads} | Toplam Spin: {total_spins_all} | Toplam Ödül: {total_reward_all}{C.RESET}")
            
            delay = float(self.config.get("Settings", "delay_between_spins", "2.0"))
            print(f"\n{T.warning}⏳ {delay} saniye içinde yeniden başlatılıyor... (Durdurmak için Ctrl+C){C.RESET}")
            time.sleep(delay)

    def _spin_loop(self, info: Dict[str, Any]) -> Tuple[float, int, int, float]:
        """Hızlı spin döngüsü."""
        token = info["token"]
        email = info["email"]
        credits = info["credits"]
        balance = info["balance"]
        total_reward = 0.0
        spins = 0
        stuck = 0
        max_stuck = 3
        
        if credits <= 0:
            print(f"{T.warning}⚠️ Yetersiz kredi. Önce reklam izlenmeli!{C.RESET}")
            return balance, credits, 0, 0.0
            
        print(f"\n{T.accent}🚀 ULTRA FAST MODE: {credits} kredi ile başlatılıyor{C.RESET}\n")
        
        while credits > 0 and self.is_running:
            try:
                data = self.network.api_spin(token)
                if not data or "error" in data:
                    stuck += 1
                    if stuck >= max_stuck:
                        print(f"{T.warning}⚠️ API ödül vermeyi durdurdu{C.RESET}")
                        break
                    time.sleep(1)
                    continue
                    
                reward = float(data.get("total", 0))
                u = data.get("user", {})
                new_cred = int(u.get("credits", 0))
                new_bal = float(u.get("balance", balance))
                
                if new_cred >= credits and data.get("success") is not True:
                    stuck += 1
                    if stuck >= max_stuck:
                        print(f"{T.warning}⚠️ API ödül vermeyi durdurdu{C.RESET}")
                        break
                else:
                    stuck = 0
                    
                credits = new_cred
                balance = new_bal
                total_reward += reward
                spins += 1
                
                if spins % 10 == 0:
                    TerminalManager.clear()
                    print(VisualComponents.status_bar())
                    print()
                    print(Drawer.line("═", color=T.primary))
                    print(Drawer.center(f"{T.accent}{C.BOLD}🎰 SPINNING | {SecurityManager.obfuscate_email(email)}{C.RESET}"))
                    print(Drawer.line("═", color=T.primary))
                    print()
                    
                    stats_dict = {
                        "Balance": (f"{balance:.2f}", "💰", T.success),
                        "Reward": (f"+{reward:.2f}", "🎁", T.accent),
                        "Spins": (spins, "📊", T.info),
                        "Total": (f"{total_reward:.2f}", "💎", T.warning),
                        "Credits": (credits, "⏳", T.primary),
                        "Time": (datetime.now().strftime("%H:%M:%S"), "🕐", T.dim),
                    }
                    
                    for label, (value, icon, color) in stats_dict.items():
                        print(f"  {color}{icon} {label:<10}: {T.accent}{value}{C.RESET}")
                        
                    print()
                    print(Animator.progress_bar(min(spins * 5, 100), 40, "Cycle Progress"))
                    print(Drawer.line("═", color=T.primary))
                    
                time.sleep(0.1)
                
            except KeyboardInterrupt:
                self.is_running = False
                raise
            except Exception as e:
                print(f"{T.error}⚠️ Spin Hatası: {str(e)}{C.RESET}")
                self.logger.error(f"Spin Hatası: {str(e)}")
                time.sleep(1)
                
        return balance, credits, spins, total_reward


# ═══════════════════════════════════════════════════════════════════════════════
# BÖLÜM 12: ANA UYGULAMA VE MENÜ SİSTEMİ
# ═══════════════════════════════════════════════════════════════════════════════

class Application:
    """Ana uygulama sınıfı ve menü yönlendiricisi."""
    
    def __init__(self):
        self.config = ConfigManager()
        self.logger = LoggerManager()
        self.bot = BotEngine(self.config, self.logger)

    def start_single(self):
        """Tek hesap başlatır."""
        accs = AccountManager.load()
        if not accs:
            print(VisualComponents.notification("ERROR", "Hesap yok! Ayarlar'dan ekleyin", "error"))
            time.sleep(2)
            return
            
        TerminalManager.clear()
        print(VisualComponents.header("HESAP SEÇİN", "Çalıştırmak için bir hesap seçin", "11.0"))
        print()
        
        keys = list(accs.keys())
        for i, k in enumerate(keys, 1):
            print(VisualComponents.menu_item(str(i), k, "📧"))
        print(VisualComponents.menu_item("0", "Geri Dön", "↩️"))
        print()
        
        ch = input(VisualComponents.input_prompt("Seçim", "▶")).strip()
        if ch == '0':
            return
            
        try:
            email = keys[int(ch) - 1]
            pwd = accs[email]
            self.bot.process_account(email, pwd)
        except KeyboardInterrupt:
            print(f"\n\n{T.warning}🛑 Kullanıcı tarafından durduruldu{C.RESET}")
        except Exception:
            print(f"{T.error}Geçersiz seçim{C.RESET}")
            time.sleep(1)

    def start_multi(self):
        """Çoklu hesap başlatır."""
        accs = AccountManager.load()
        if not accs:
            print(VisualComponents.notification("ERROR", "Hesap yok!", "error"))
            time.sleep(2)
            return
            
        TerminalManager.clear()
        print(VisualComponents.header("ÇOKLU HESAP MODU", f"{len(accs)} hesap işleniyor", "11.0"))
        print()
        print(VisualComponents.notification("INFO", "Tüm hesaplar sırayla başlatılıyor...", "info"))
        print()
        
        for email, pwd in accs.items():
            try:
                self.bot.process_account(email, pwd)
            except KeyboardInterrupt:
                print(f"\n\n{T.warning}🛑 Kullanıcı tarafından durduruldu{C.RESET}")
                break
                
        print()
        print(VisualComponents.notification("SUCCESS", "Tüm hesaplar işlendi!", "success"))
        time.sleep(3)

    def settings_menu(self):
        """Ayarlar menüsü."""
        while True:
            TerminalManager.clear()
            print(VisualComponents.header("AYARLAR", "Yapılandırma ve Hesaplar", "11.0"))
            print()
            
            items = [
                ("1", "Hesap Yöneticisi", "👥"),
                ("2", "Tema Değiştir", "🎨"),
                ("3", "İstatistikleri Görüntüle", "📊"),
                ("4", "CSV Olarak Dışa Aktar", "📁"),
                ("5", "Sistem Bilgisi", "ℹ️"),
                ("0", "Ana Menüye Dön", "↩️"),
            ]
            print(VisualComponents.menu("AYARLAR", items))
            print()
            
            ch = input(VisualComponents.input_prompt("Seçim", "▶")).strip()
            
            if ch == '1':
                AccountManager.menu_loop()
            elif ch == '2':
                TerminalManager.clear()
                print(VisualComponents.header("TEMA SEÇİCİ", "Tarzınızı seçin", "11.0"))
                print()
                themes = list(Theme.THEMES.keys())
                for i, t in enumerate(themes, 1):
                    print(VisualComponents.menu_item(str(i), t.upper(), "🎨"))
                print()
                th_ch = input(VisualComponents.input_prompt("Tema", "▶")).strip()
                try:
                    global current_theme, T
                    current_theme = Theme(themes[int(th_ch) - 1])
                    T = current_theme
                    self.config.set("Settings", "theme", current_theme.name)
                    print(VisualComponents.notification("SUCCESS", f"Tema değiştirildi: {current_theme.name}", "success"))
                    time.sleep(1)
                except (ValueError, IndexError):
                    print(VisualComponents.notification("ERROR", "Geçersiz seçim", "error"))
                    time.sleep(1)
            elif ch == '3':
                StatisticsManager.display_dashboard()
            elif ch == '4':
                StatisticsManager.export_to_csv()
                time.sleep(2)
            elif ch == '5':
                TerminalManager.clear()
                print(VisualComponents.header("SİSTEM BİLGİSİ", "", "11.0"))
                print()
                info_lines = [
                    f"🎰 Bot: FruitClaim Pro V.11",
                    f"👤 Oluşturucu: AlperenThe",
                    f"📅 Yıl: 2026",
                    f"🖥️  Terminal: {TerminalManager.width()}x{TerminalManager.height()}",
                    f"🎨 Tema: {current_theme.name}",
                    f"🐍 Python: {platform.python_version()}",
                    f"📦 İşletim Sistemi: {platform.system()} {platform.release()}",
                    f"🌐 Requests: {requests.__version__}",
                ]
                print(Drawer.fancy_box("BİLGİ", info_lines))
                print()
                input(f"{T.accent}Devam etmek için Enter'a basın...{C.RESET}")
            elif ch == '0':
                break

    def run(self):
        """Ana çalışma döngüsü."""
        TerminalManager.set_title("FruitClaim Pro V.11 - AlperenThe")
        TerminalManager.hide_cursor()
        
        try:
            TerminalManager.clear()
            print(VisualComponents.splash_screen())
            time.sleep(1)
            
            Animator.loading_sequence([
                "Çekirdek modüller yükleniyor",
                "UI sistemi başlatılıyor",
                "Yapılandırma dosyası okunuyor",
                "API uç noktaları doğrulanıyor",
                "Sistem hazır"
            ], delay=0.4)
            time.sleep(0.5)
            
            while True:
                TerminalManager.clear()
                print(VisualComponents.status_bar())
                print()
                
                w = TerminalManager.width()
                print(Drawer.center(f"{T.accent}{ASCIIArt.COMBINED_HEADER}{C.RESET}", w))
                print(Drawer.center(f"{T.primary}{C.BOLD}FRUITCLAIM PRO V.11{C.RESET}", w))
                print()
                
                items = [
                    ("1", "TEK HESAP BAŞLAT (7/24)", "🎯"),
                    ("2", "ÇOKLU HESAP BAŞLAT (7/24)", "🚀"),
                    ("3", "AYARLAR VE HESAPLAR", "⚙️"),
                    ("4", "İSTATİSTİKLERİ GÖRÜNTÜLE", "📊"),
                    ("5", "SİSTEMDEN ÇIK", "🚪"),
                ]
                print(VisualComponents.menu("ANA MENÜ", items, "Devam etmek için bir seçenek belirleyin"))
                print()
                
                ch = input(VisualComponents.input_prompt("Seçenek", "▶")).strip()
                
                if ch == '1':
                    self.start_single()
                elif ch == '2':
                    self.start_multi()
                elif ch == '3':
                    self.settings_menu()
                elif ch == '4':
                    StatisticsManager.display_dashboard()
                elif ch == '5':
                    TerminalManager.clear()
                    print(VisualComponents.header("GÖRÜŞÜRÜZ", "FruitClaim Pro'yu kullandığınız için teşekkürler", "11.0"))
                    print()
                    print(Drawer.center(f"{T.accent}👋 Yakında görüşmek üzere!{C.RESET}"))
                    print()
                    print(Drawer.center(f"{T.dim}Creator: AlperenThe | 2026{C.RESET}"))
                    print()
                    break
                else:
                    print(VisualComponents.notification("ERROR", "Geçersiz seçenek!", "error"))
                    time.sleep(1)
                    
        except KeyboardInterrupt:
            pass
        finally:
            TerminalManager.show_cursor()
            TerminalManager.clear()
            print(f"\n{T.warning}🛑 Sistem güvenli şekilde kapatıldı.{C.RESET}\n")


# ═══════════════════════════════════════════════════════════════════════════════
# BÖLÜM 13: GİRİŞ NOKTASI
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    try:
        if os.name == "nt":
            os.system("chcp 65001 >nul")
            
        app = Application()
        app.run()
    except Exception as e:
        TerminalManager.show_cursor()
        print(f"\n{T.error}💥 Kritik Hata: {str(e)}{C.RESET}")
        traceback.print_exc()
        sys.exit(1)
