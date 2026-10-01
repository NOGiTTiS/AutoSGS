"""
Hotkey Manager module for AutoSGS.
Listens for global hotkeys (start key and emergency stop ESC) across applications.
"""

from typing import Callable, Optional
import threading
from pynput import keyboard


SPECIAL_KEYS = {
    "f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9", "f10", "f11", "f12",
    "ctrl", "alt", "shift", "cmd", "esc", "escape", "space", "enter", "tab",
    "backspace", "delete", "home", "end", "page_up", "page_down"
}


def normalize_hotkey(hotkey: str) -> str:
    """
    Normalizes a hotkey string for pynput GlobalHotKeys.
    Follows pynput syntax:
    - Special keys in angle brackets: <f2>, <esc>, <ctrl>, <alt>
    - Regular characters: v, s, etc.
    Examples:
        'F2' -> '<f2>'
        'f8' -> '<f8>'
        'ESC' -> '<esc>'
        'ctrl+alt+v' -> '<ctrl>+<alt>+v'
    """
    h = hotkey.strip().lower()
    if not h:
        return "<f2>"
    if h in ["esc", "escape"]:
        return "<esc>"
    if h.startswith("<") and h.endswith(">"):
        return h

    if "+" in h:
        parts = [p.strip() for p in h.split("+")]
        formatted = []
        for p in parts:
            p_clean = p.strip("<> ")
            if p_clean in SPECIAL_KEYS:
                name = "esc" if p_clean in ["esc", "escape"] else p_clean
                formatted.append(f"<{name}>")
            else:
                formatted.append(p_clean)
        return "+".join(formatted)

    clean = h.strip("<> ")
    if clean in SPECIAL_KEYS:
        name = "esc" if clean in ["esc", "escape"] else clean
        return f"<{name}>"

    return clean


class HotkeyManager:
    """
    Manages global keyboard hotkeys for starting typing and emergency stopping.
    """

    def __init__(
        self,
        on_start: Optional[Callable[[], None]] = None,
        on_stop: Optional[Callable[[], None]] = None,
        start_hotkey: str = "F2",
    ):
        self.on_start = on_start
        self.on_stop = on_stop
        self.start_hotkey_str = start_hotkey
        self._listener: Optional[keyboard.GlobalHotKeys] = None
        self._lock = threading.Lock()
        self._is_running = False

    @property
    def is_running(self) -> bool:
        return self._is_running

    def _build_hotkey_dict(self) -> dict:
        hotkeys = {}
        normalized_start = normalize_hotkey(self.start_hotkey_str)

        if self.on_start:
            hotkeys[normalized_start] = self._handle_start

        if self.on_stop:
            # ESC is always the emergency stop key
            hotkeys["<esc>"] = self._handle_stop

        return hotkeys

    def _handle_start(self) -> None:
        if self.on_start:
            try:
                self.on_start()
            except Exception as e:
                print(f"[HotkeyManager] Error in on_start: {e}")

    def _handle_stop(self) -> None:
        if self.on_stop:
            try:
                self.on_stop()
            except Exception as e:
                print(f"[HotkeyManager] Error in on_stop: {e}")

    def start(self) -> bool:
        """Starts the global hotkey listener in background thread."""
        with self._lock:
            if self._is_running:
                return True
            try:
                hotkey_map = self._build_hotkey_dict()
                if not hotkey_map:
                    return False
                self._listener = keyboard.GlobalHotKeys(hotkey_map)
                self._listener.start()
                self._is_running = True
                return True
            except Exception as e:
                print(f"[HotkeyManager] Failed to start listener: {e}")
                self._is_running = False
                return False

    def stop(self) -> None:
        """Stops the global hotkey listener."""
        with self._lock:
            if self._listener is not None:
                try:
                    self._listener.stop()
                except Exception:
                    pass
                self._listener = None
            self._is_running = False

    def update_start_hotkey(self, new_hotkey: str) -> bool:
        """Updates the start hotkey and restarts the listener if active."""
        with self._lock:
            self.start_hotkey_str = new_hotkey
            if self._is_running:
                if self._listener is not None:
                    self._listener.stop()
                    self._listener = None
                hotkey_map = self._build_hotkey_dict()
                if not hotkey_map:
                    self._is_running = False
                    return True
                try:
                    self._listener = keyboard.GlobalHotKeys(hotkey_map)
                    self._listener.start()
                    return True
                except Exception as e:
                    print(f"[HotkeyManager] Failed to restart listener: {e}")
                    self._is_running = False
                    return False
            return True
