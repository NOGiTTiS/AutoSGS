"""
Configuration Manager for AutoSGS.
Loads and saves user preferences to ~/.autosgs/config.json
"""

import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Optional, Dict


SCALE_MAP: Dict[str, float] = {
    "Standard": 1.0,
    "Large": 1.15,
    "Extra Large": 1.30,
}

DISPLAY_TO_SCALE: Dict[str, str] = {
    "ปกติ (100%)": "Standard",
    "ใหญ่ (115%)": "Large",
    "ใหญ่พิเศษ (130%)": "Extra Large",
}

SCALE_TO_DISPLAY: Dict[str, str] = {v: k for k, v in DISPLAY_TO_SCALE.items()}


MODE_SPECS: Dict[str, dict] = {
    "scores": {
        "key": "scores",
        "label": "ผลการเรียน",
        "display_name": "📊 ผลการเรียน",
        "expected_cols": None,
        "extra_row_end_tabs": 0,
        "desc": "ผลการเรียนรายวิชาทั่วไป (พิมพ์ + Tab ทุกช่อง)",
        "show_save_reminder": False,
    },
    "characteristics": {
        "key": "characteristics",
        "label": "คุณลักษณะอันพึงประสงค์",
        "display_name": "⭐ คุณลักษณะฯ (8 ช่อง)",
        "expected_cols": 8,
        "extra_row_end_tabs": 4,
        "desc": "8 ช่อง (พิมพ์ + Tab) + Tab ท้ายแถว 4 ครั้ง",
        "show_save_reminder": True,
        "reminder_message": "💾 กรุณากดปุ่ม \"บันทึก\" ในระบบ SGS ด้วยนะครับ!",
    },
    "reading_analysis": {
        "key": "reading_analysis",
        "label": "การอ่าน คิดวิเคราะห์และเขียน",
        "display_name": "📖 การอ่านฯ (5 ช่อง)",
        "expected_cols": 5,
        "extra_row_end_tabs": 3,
        "desc": "5 ช่อง (พิมพ์ + Tab) + Tab ท้ายแถว 3 ครั้ง",
        "show_save_reminder": True,
        "reminder_message": "💾 กรุณากดปุ่ม \"บันทึก\" ในระบบ SGS ด้วยนะครับ!",
    },
}

DISPLAY_TO_MODE: Dict[str, str] = {v["display_name"]: k for k, v in MODE_SPECS.items()}
MODE_TO_DISPLAY: Dict[str, str] = {k: v["display_name"] for k, v in MODE_SPECS.items()}


def get_scaling_factor(scale_key: str) -> float:
    """Returns the float scaling factor for CustomTkinter widget scaling."""
    return SCALE_MAP.get(scale_key, 1.15)


@dataclass
class AppConfig:
    delay_seconds: float = 0.1
    delay_scores: float = 0.10
    delay_characteristics: float = 0.02
    delay_reading_analysis: float = 0.02
    countdown_seconds: int = 3
    start_hotkey: str = "F2"
    stop_hotkey: str = "Escape"
    always_on_top: bool = True
    sound_enabled: bool = True
    theme: str = "System"  # "System", "Dark", "Light"
    ui_scale: str = "Large"  # "Standard", "Large", "Extra Large"
    entry_mode: str = "scores"  # "scores", "characteristics", "reading_analysis"


def get_mode_delay(config: AppConfig, mode_key: str) -> float:
    """Returns the delay in seconds for the specified entry mode."""
    if mode_key == "characteristics":
        return getattr(config, "delay_characteristics", 0.02)
    elif mode_key == "reading_analysis":
        return getattr(config, "delay_reading_analysis", 0.02)
    else:
        return getattr(config, "delay_scores", config.delay_seconds)


def set_mode_delay(config: AppConfig, mode_key: str, delay: float) -> None:
    """Sets the delay in seconds for the specified entry mode."""
    val = round(delay, 2)
    if mode_key == "characteristics":
        config.delay_characteristics = val
    elif mode_key == "reading_analysis":
        config.delay_reading_analysis = val
    else:
        config.delay_scores = val
        config.delay_seconds = val


def get_config_dir() -> Path:
    """Returns the application config directory ~/.autosgs."""
    config_dir = Path.home() / ".autosgs"
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir


def get_config_path() -> Path:
    """Returns the config file path ~/.autosgs/config.json."""
    return get_config_dir() / "config.json"


def load_config(custom_path: Optional[Path] = None) -> AppConfig:
    """
    Loads config from JSON file. Returns default AppConfig if file doesn't exist or on error.
    """
    path = custom_path or get_config_path()
    if not path.exists():
        return AppConfig()

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            delay_sec = float(data.get("delay_seconds", 0.1))
            return AppConfig(
                delay_seconds=delay_sec,
                delay_scores=float(data.get("delay_scores", delay_sec)),
                delay_characteristics=float(data.get("delay_characteristics", 0.02)),
                delay_reading_analysis=float(data.get("delay_reading_analysis", 0.02)),
                countdown_seconds=int(data.get("countdown_seconds", 3)),
                start_hotkey=str(data.get("start_hotkey", "F2")),
                stop_hotkey=str(data.get("stop_hotkey", "Escape")),
                always_on_top=bool(data.get("always_on_top", True)),
                sound_enabled=bool(data.get("sound_enabled", True)),
                theme=str(data.get("theme", "System")),
                ui_scale=str(data.get("ui_scale", "Large")),
                entry_mode=str(data.get("entry_mode", "scores")) if data.get("entry_mode") in MODE_SPECS else "scores",
            )
    except Exception as e:
        print(f"[ConfigManager] Error reading config: {e}. Using defaults.")
        return AppConfig()


def save_config(config: AppConfig, custom_path: Optional[Path] = None) -> bool:
    """
    Saves AppConfig to JSON file. Returns True on success, False on error.
    """
    path = custom_path or get_config_path()
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(asdict(config), f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"[ConfigManager] Error saving config: {e}")
        return False
