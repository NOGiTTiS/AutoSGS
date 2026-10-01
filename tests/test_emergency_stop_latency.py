"""
Automated Latency and Edge-case tests for AutoSGS Emergency Stop & Complex TSV Parsing.
Verifies AC 4.1: Emergency Stop latency must be <= 50ms.
"""

import time
import pytest
from pynput.keyboard import Key
from autosgs.core.clipboard_parser import parse_tsv, ScoreMatrix
from autosgs.core.typer_engine import TyperEngine


class MockKeyboard:
    def __init__(self):
        self.count = 0

    def type(self, text):
        self.count += 1

    def press(self, key):
        pass

    def release(self, key):
        pass


def test_emergency_stop_sub_50ms_latency():
    """
    Verifies that calling engine.stop() while typing loop is waiting on delay
    aborts the thread in less than 50 milliseconds.
    """
    mock_kb = MockKeyboard()
    engine = TyperEngine(keyboard_controller=mock_kb)

    # 100 rows x 5 columns with a slow delay (1.0 second per cell)
    rows = [[str(col) for col in range(5)] for _ in range(100)]
    matrix = ScoreMatrix(
        total_rows=100,
        total_columns=5,
        total_cells=500,
        empty_cells_count=0,
        rows=rows,
    )

    started = engine.start_typing(matrix=matrix, delay=1.0, countdown=0)
    assert started is True

    # Allow thread to start and enter delay wait
    time.sleep(0.05)
    assert engine.is_running is True

    # Measure stop latency
    t_start = time.perf_counter()
    engine.stop("User pressed ESC")
    engine._thread.join(timeout=1.0)
    t_elapsed_ms = (time.perf_counter() - t_start) * 1000

    assert engine.is_running is False
    # Strict requirement: Emergency stop latency <= 50ms
    assert t_elapsed_ms < 50.0, f"Emergency stop took too long: {t_elapsed_ms:.2f}ms"


def test_complex_and_40_row_tsv_parsing():
    """
    Tests parsing a realistic 40 students x 3 columns dataset with blanks and Thai strings.
    """
    lines = []
    for i in range(40):
        # Introduce blanks at specific indices
        c1 = "" if i % 7 == 0 else f"{15 + (i % 5)}"
        c2 = "" if i % 5 == 0 else f"{18.5}"
        c3 = "ข" if i == 10 else f"{19}"
        lines.append(f"{c1}\t{c2}\t{c3}")

    raw_tsv = "\r\n".join(lines) + "\r\n\r\n"
    matrix = parse_tsv(raw_tsv)

    assert matrix.total_rows == 40
    assert matrix.total_columns == 3
    assert matrix.total_cells == 120
    assert matrix.empty_cells_count > 0

    # Verify student 10 has "ข"
    assert matrix.rows[10][2] == "ข"

    # Verify blank handling in row 0
    assert matrix.rows[0][0] == ""
    assert matrix.rows[0][1] == ""
