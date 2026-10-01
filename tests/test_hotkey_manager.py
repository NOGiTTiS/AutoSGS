"""
Unit tests for autosgs.core.hotkey_manager
"""

import pytest
from autosgs.core.hotkey_manager import normalize_hotkey, HotkeyManager


def test_normalize_hotkey():
    assert normalize_hotkey("F2") == "<f2>"
    assert normalize_hotkey("f8") == "<f8>"
    assert normalize_hotkey("ESC") == "<esc>"
    assert normalize_hotkey("escape") == "<esc>"
    assert normalize_hotkey("<f2>") == "<f2>"
    assert normalize_hotkey("ctrl+alt+v") == "<ctrl>+<alt>+v"
    assert normalize_hotkey("") == "<f2>"


def test_hotkey_manager_map_creation():
    on_start_called = False
    on_stop_called = False

    def on_start():
        nonlocal on_start_called
        on_start_called = True

    def on_stop():
        nonlocal on_stop_called
        on_stop_called = True

    manager = HotkeyManager(on_start=on_start, on_stop=on_stop, start_hotkey="F8")
    mapping = manager._build_hotkey_dict()

    assert "<f8>" in mapping
    assert "<esc>" in mapping

    # Simulate triggering handlers directly
    mapping["<f8>"]()
    assert on_start_called is True

    mapping["<esc>"]()
    assert on_stop_called is True


def test_hotkey_manager_update():
    manager = HotkeyManager(on_start=lambda: None, start_hotkey="F2")
    mapping = manager._build_hotkey_dict()
    assert "<f2>" in mapping

    manager.update_start_hotkey("F9")
    mapping2 = manager._build_hotkey_dict()
    assert "<f9>" in mapping2
    assert "<f2>" not in mapping2
