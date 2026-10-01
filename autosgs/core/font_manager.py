"""
Font Manager for AutoSGS.
Loads and registers the 'Prompt' font dynamically at runtime on Windows and macOS.
Provides helper for obtaining consistent typography across all UI widgets.
"""

import sys
import os
from pathlib import Path
from typing import Optional
import customtkinter as ctk

FONT_FAMILY = "Prompt"
FALLBACK_FONTS = ["Prompt", "Leelawadee UI", "Segoe UI", "Tahoma", "sans-serif"]


def get_base_dir() -> Path:
    """Returns the base project directory or PyInstaller temporary bundle directory."""
    if getattr(sys, "frozen", False):
        return Path(sys._MEIPASS)
    return Path(__file__).resolve().parent.parent.parent


def get_asset_path(relative_path: str) -> Path:
    """Returns absolute path to an asset file."""
    return get_base_dir() / relative_path


def register_fonts():
    """
    Registers custom TTF fonts (e.g. Prompt) into the system in-memory font table on Windows.
    This enables CustomTkinter/Tkinter to immediately use 'Prompt' without requiring manual font installation.
    """
    if sys.platform == "win32":
        try:
            import ctypes
            fonts_dir = get_asset_path("assets/fonts")
            if fonts_dir.exists():
                for font_path in fonts_dir.glob("*.ttf"):
                    # 0x10 = FR_PRIVATE (process-private, unloaded on exit)
                    ctypes.windll.gdi32.AddFontResourceExW(str(font_path.resolve()), 0x10, 0)
        except Exception as e:
            print(f"[FontManager] Warning: Could not register font: {e}")


def get_ui_font(size: int = 13, weight: str = "normal") -> ctk.CTkFont:
    """
    Returns a CTkFont instance configured with 'Prompt' font family.
    """
    return ctk.CTkFont(family=FONT_FAMILY, size=size, weight=weight)
