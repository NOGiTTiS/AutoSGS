"""
Sound Notifier module for AutoSGS.
Provides cross-platform audio feedback for countdowns, completion, and emergency stops.
"""

import sys
import threading
import subprocess
from typing import Optional


def _play_windows_beep(freq: int, duration_ms: int) -> None:
    try:
        import winsound
        winsound.Beep(freq, duration_ms)
    except Exception:
        pass


def _play_mac_sound(sound_name: str) -> None:
    try:
        sound_path = f"/System/Library/Sounds/{sound_name}.aiff"
        subprocess.Popen(["afplay", sound_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        # Fallback to terminal bell
        print("\a", end="", flush=True)


def play_countdown_beep(enabled: bool = True) -> None:
    """Plays a short, crisp beep during countdown tick (3.. 2.. 1..)."""
    if not enabled:
        return

    def _play():
        if sys.platform == "win32":
            _play_windows_beep(880, 70)
        elif sys.platform == "darwin":
            _play_mac_sound("Tink")
        else:
            print("\a", end="", flush=True)

    threading.Thread(target=_play, daemon=True).start()


def play_success_sound(enabled: bool = True) -> None:
    """Plays an upbeat chime when score typing finishes successfully."""
    if not enabled:
        return

    def _play():
        if sys.platform == "win32":
            # Two-tone rising chime
            _play_windows_beep(784, 120)  # G5
            _play_windows_beep(1046, 250) # C6
        elif sys.platform == "darwin":
            _play_mac_sound("Glass")
        else:
            print("\a", end="", flush=True)

    threading.Thread(target=_play, daemon=True).start()


def play_stop_sound(enabled: bool = True) -> None:
    """Plays a low alert tone when typing is aborted or emergency stopped."""
    if not enabled:
        return

    def _play():
        if sys.platform == "win32":
            _play_windows_beep(440, 200)  # A4 low tone
        elif sys.platform == "darwin":
            _play_mac_sound("Basso")
        else:
            print("\a", end="", flush=True)

    threading.Thread(target=_play, daemon=True).start()
