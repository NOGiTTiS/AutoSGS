"""
Unit tests for autosgs.core.typer_engine
"""

import time
import pytest
from pynput.keyboard import Key
from autosgs.core.clipboard_parser import ScoreMatrix
from autosgs.core.typer_engine import TyperEngine


class MockKeyboard:
    def __init__(self):
        self.events = []  # list of tuples: ('type', val), ('press', key), ('release', key)

    def type(self, text):
        self.events.append(("type", text))

    def press(self, key):
        self.events.append(("press", key))

    def release(self, key):
        self.events.append(("release", key))


def test_typer_engine_keystrokes_and_blank_handling():
    mock_kb = MockKeyboard()
    engine = TyperEngine(keyboard_controller=mock_kb)

    # 2 rows, 2 cols, one empty cell
    matrix = ScoreMatrix(
        total_rows=2,
        total_columns=2,
        total_cells=4,
        empty_cells_count=1,
        rows=[["15", "20"], ["", "18"]],
    )

    finished_cells = []
    progress_records = []

    def on_finished(count):
        finished_cells.append(count)

    def on_progress(row, total_rows, cell, total_cells, val):
        progress_records.append((row, cell, val))

    started = engine.start_typing(
        matrix=matrix,
        delay=0.01,
        countdown=0,
        on_progress=on_progress,
        on_finished=on_finished,
    )
    assert started is True

    # Wait for thread to finish
    engine._thread.join(timeout=2.0)
    assert engine.is_running is False
    assert finished_cells == [4]
    assert len(progress_records) == 4

    # Verify order of events:
    # 1. type "15", press Tab, release Tab
    # 2. type "20", press Tab, release Tab
    # 3. (blank cell) press Tab, release Tab (NO type)
    # 4. type "18", press Tab, release Tab
    expected_events = [
        ("type", "15"),
        ("press", Key.tab),
        ("release", Key.tab),
        ("type", "20"),
        ("press", Key.tab),
        ("release", Key.tab),
        ("press", Key.tab),
        ("release", Key.tab),
        ("type", "18"),
        ("press", Key.tab),
        ("release", Key.tab),
    ]
    assert mock_kb.events == expected_events


def test_typer_engine_emergency_stop():
    mock_kb = MockKeyboard()
    engine = TyperEngine(keyboard_controller=mock_kb)

    # Many cells with larger delay
    rows = [[str(i) for i in range(10)] for _ in range(10)]
    matrix = ScoreMatrix(
        total_rows=10,
        total_columns=10,
        total_cells=100,
        empty_cells_count=0,
        rows=rows,
    )

    stopped_reasons = []

    def on_stopped(reason):
        stopped_reasons.append(reason)

    started = engine.start_typing(
        matrix=matrix,
        delay=0.1,  # 100ms per cell
        countdown=0,
        on_stopped=on_stopped,
    )
    assert started is True

    # Let it run briefly then stop
    time.sleep(0.05)
    engine.stop()

    engine._thread.join(timeout=1.0)
    assert engine.is_running is False
    assert len(stopped_reasons) == 1
    assert "หยุดฉุกเฉิน" in stopped_reasons[0]
