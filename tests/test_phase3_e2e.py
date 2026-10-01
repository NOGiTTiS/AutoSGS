"""
Phase 3 End-to-End verification:
Simulates actual Excel / Google Sheets clipboard formats across 1-col, 3-col, and blank scenarios.
"""

import pytest
from pynput.keyboard import Key
from autosgs.core.clipboard_parser import parse_tsv
from autosgs.core.typer_engine import TyperEngine


class KeystrokeRecorder:
    def __init__(self):
        self.typed_texts = []
        self.tab_count = 0

    def type(self, text):
        self.typed_texts.append(text)

    def press(self, key):
        if key == Key.tab:
            self.tab_count += 1

    def release(self, key):
        pass


def test_excel_1_column_40_rows():
    """Simulates copying a single score column for 40 students."""
    tsv = "".join([f"{15 + (i % 6)}\r\n" for i in range(40)])
    matrix = parse_tsv(tsv)

    assert matrix.total_rows == 40
    assert matrix.total_columns == 1
    assert matrix.total_cells == 40
    assert matrix.empty_cells_count == 0

    recorder = KeystrokeRecorder()
    engine = TyperEngine(keyboard_controller=recorder)
    engine.start_typing(matrix=matrix, delay=0.001)
    engine._thread.join(timeout=2.0)

    assert len(recorder.typed_texts) == 40
    assert recorder.tab_count == 40


def test_excel_3_columns_40_rows():
    """Simulates copying 3 columns (Assignment 1, 2, Midterm) for 40 students."""
    tsv = "".join([f"{18}\t{19}\t{20}\r\n" for _ in range(40)])
    matrix = parse_tsv(tsv)

    assert matrix.total_rows == 40
    assert matrix.total_columns == 3
    assert matrix.total_cells == 120
    assert matrix.empty_cells_count == 0

    recorder = KeystrokeRecorder()
    engine = TyperEngine(keyboard_controller=recorder)
    engine.start_typing(matrix=matrix, delay=0.001)
    engine._thread.join(timeout=2.0)

    assert len(recorder.typed_texts) == 120
    assert recorder.tab_count == 120


def test_excel_3_columns_with_empty_cells():
    """Simulates copying a table where some students were absent (empty cells)."""
    lines = []
    expected_typed_count = 0
    total_cells = 30 * 3

    for i in range(30):
        # Student 5 and 15 have blanks
        c1 = "" if i == 5 else "17"
        c2 = "" if i == 15 else "18"
        c3 = "20"
        lines.append(f"{c1}\t{c2}\t{c3}")
        if c1: expected_typed_count += 1
        if c2: expected_typed_count += 1
        expected_typed_count += 1  # c3 always has a value

    tsv = "\r\n".join(lines)
    matrix = parse_tsv(tsv)

    assert matrix.total_rows == 30
    assert matrix.total_columns == 3
    assert matrix.total_cells == 90
    assert matrix.empty_cells_count == 2

    recorder = KeystrokeRecorder()
    engine = TyperEngine(keyboard_controller=recorder)
    engine.start_typing(matrix=matrix, delay=0.001)
    engine._thread.join(timeout=2.0)

    # Blank cells should NEVER call type(), but MUST press Tab
    assert len(recorder.typed_texts) == expected_typed_count
    assert recorder.tab_count == 90
