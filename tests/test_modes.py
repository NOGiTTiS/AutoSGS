"""
Unit tests for AutoSGS Grading Modes (ผลการเรียน, คุณลักษณะอันพึงประสงค์, การอ่าน คิดวิเคราะห์และเขียน)
"""

import pytest
from pynput.keyboard import Key
from autosgs.core.config_manager import MODE_SPECS, AppConfig, load_config, save_config
from autosgs.core.clipboard_parser import ScoreMatrix
from autosgs.core.typer_engine import TyperEngine


class MockKeyboard:
    def __init__(self):
        self.events = []  # ('type', str) or ('press', Key) or ('release', Key)

    def type(self, text):
        self.events.append(("type", text))

    def press(self, key):
        self.events.append(("press", key))

    def release(self, key):
        self.events.append(("release", key))


def test_mode_specs_structure():
    """Verify MODE_SPECS contains the 3 required modes and correct attributes."""
    assert "scores" in MODE_SPECS
    assert "characteristics" in MODE_SPECS
    assert "reading_analysis" in MODE_SPECS

    # 1. Academic scores mode
    assert MODE_SPECS["scores"]["label"] == "ผลการเรียน"
    assert MODE_SPECS["scores"]["expected_cols"] is None
    assert MODE_SPECS["scores"]["extra_row_end_tabs"] == 0
    assert MODE_SPECS["scores"]["show_save_reminder"] is False

    # 2. Desirable characteristics mode
    assert MODE_SPECS["characteristics"]["label"] == "คุณลักษณะอันพึงประสงค์"
    assert MODE_SPECS["characteristics"]["expected_cols"] == 8
    assert MODE_SPECS["characteristics"]["extra_row_end_tabs"] == 4
    assert MODE_SPECS["characteristics"]["show_save_reminder"] is True
    assert "บันทึก" in MODE_SPECS["characteristics"]["reminder_message"]

    # 3. Reading, analysis and writing mode
    assert MODE_SPECS["reading_analysis"]["label"] == "การอ่าน คิดวิเคราะห์และเขียน"
    assert MODE_SPECS["reading_analysis"]["expected_cols"] == 5
    assert MODE_SPECS["reading_analysis"]["extra_row_end_tabs"] == 3
    assert MODE_SPECS["reading_analysis"]["show_save_reminder"] is True
    assert "บันทึก" in MODE_SPECS["reading_analysis"]["reminder_message"]


def test_mode_1_academic_scores_keystroke_sequence():
    """
    Mode 1: Academic Scores (ผลการเรียน)
    2 students x 3 columns = 6 cells.
    Each cell: score + 1 Tab.
    Total tabs: 6 (0 extra tabs).
    """
    mock_kb = MockKeyboard()
    engine = TyperEngine(keyboard_controller=mock_kb)

    matrix = ScoreMatrix(
        total_rows=2,
        total_columns=3,
        total_cells=6,
        empty_cells_count=0,
        rows=[["18", "19", "20"], ["15", "16", "17"]],
    )

    started = engine.start_typing(
        matrix=matrix,
        delay=0.001,
        countdown=0,
        extra_row_end_tabs=MODE_SPECS["scores"]["extra_row_end_tabs"],
    )
    assert started is True
    engine._thread.join(timeout=2.0)

    # Count tabs
    tab_presses = [e for e in mock_kb.events if e == ("press", Key.tab)]
    assert len(tab_presses) == 6

    # Verify order
    expected_types = ["18", "19", "20", "15", "16", "17"]
    actual_types = [e[1] for e in mock_kb.events if e[0] == "type"]
    assert actual_types == expected_types


def test_mode_2_characteristics_keystroke_sequence():
    """
    Mode 2: Characteristics (คุณลักษณะอันพึงประสงค์)
    8 columns + 4 extra tabs = 1 student.
    2 students x 8 columns = 16 cells.
    Each cell: score + 1 Tab (16 Tabs).
    Row end: 4 extra Tabs per student (2 * 4 = 8 extra Tabs).
    Total tabs: 24 Tabs.
    """
    mock_kb = MockKeyboard()
    engine = TyperEngine(keyboard_controller=mock_kb)

    row1 = ["3", "3", "3", "3", "3", "3", "3", "3"]
    row2 = ["3", "2", "3", "3", "2", "3", "3", "3"]
    matrix = ScoreMatrix(
        total_rows=2,
        total_columns=8,
        total_cells=16,
        empty_cells_count=0,
        rows=[row1, row2],
    )

    started = engine.start_typing(
        matrix=matrix,
        delay=0.001,
        countdown=0,
        extra_row_end_tabs=MODE_SPECS["characteristics"]["extra_row_end_tabs"],
    )
    assert started is True
    engine._thread.join(timeout=2.0)

    # Count tabs: 16 cell tabs + 8 extra tabs = 24
    tab_presses = [e for e in mock_kb.events if e == ("press", Key.tab)]
    assert len(tab_presses) == 24

    # Let's inspect the events of row 1:
    # 8 scores (each type + press tab + release tab = 24 events)
    # followed by 4 extra tabs (each press tab + release tab = 8 events)
    # Total row 1 events = 32
    row1_events = mock_kb.events[:32]
    # First 8 cell operations:
    for c in range(8):
        assert row1_events[c * 3] == ("type", "3")
        assert row1_events[c * 3 + 1] == ("press", Key.tab)
        assert row1_events[c * 3 + 2] == ("release", Key.tab)

    # 4 extra tabs at row 1 end:
    for t in range(4):
        assert row1_events[24 + t * 2] == ("press", Key.tab)
        assert row1_events[24 + t * 2 + 1] == ("release", Key.tab)


def test_mode_3_reading_analysis_keystroke_sequence():
    """
    Mode 3: Reading, Analytical Thinking & Writing (การอ่าน คิดวิเคราะห์และเขียน)
    5 columns + 3 extra tabs = 1 student.
    2 students x 5 columns = 10 cells.
    Each cell: score + 1 Tab (10 Tabs).
    Row end: 3 extra Tabs per student (2 * 3 = 6 extra Tabs).
    Total tabs: 16 Tabs.
    """
    mock_kb = MockKeyboard()
    engine = TyperEngine(keyboard_controller=mock_kb)

    row1 = ["3", "3", "3", "3", "3"]
    row2 = ["3", "2", "3", "3", "2"]
    matrix = ScoreMatrix(
        total_rows=2,
        total_columns=5,
        total_cells=10,
        empty_cells_count=0,
        rows=[row1, row2],
    )

    started = engine.start_typing(
        matrix=matrix,
        delay=0.001,
        countdown=0,
        extra_row_end_tabs=MODE_SPECS["reading_analysis"]["extra_row_end_tabs"],
    )
    assert started is True
    engine._thread.join(timeout=2.0)

    # Count tabs: 10 cell tabs + 6 extra tabs = 16
    tab_presses = [e for e in mock_kb.events if e == ("press", Key.tab)]
    assert len(tab_presses) == 16

    # Row 1 events: 5 cells * 3 = 15 events, plus 3 extra tabs * 2 = 6 events -> total 21
    row1_events = mock_kb.events[:21]
    # 5 cell keystrokes
    for c in range(5):
        assert row1_events[c * 3] == ("type", "3")
        assert row1_events[c * 3 + 1] == ("press", Key.tab)
        assert row1_events[c * 3 + 2] == ("release", Key.tab)

    # 3 Extra tabs at row 1 end:
    for t in range(3):
        assert row1_events[15 + t * 2] == ("press", Key.tab)
        assert row1_events[15 + t * 2 + 1] == ("release", Key.tab)


def test_mode_with_blank_cells():
    """Verify blank cells skip typing but still send tab and extra tabs."""
    mock_kb = MockKeyboard()
    engine = TyperEngine(keyboard_controller=mock_kb)

    # 1 row, 5 columns, with blank cell at index 2
    row = ["3", "3", "", "3", "3"]
    matrix = ScoreMatrix(
        total_rows=1,
        total_columns=5,
        total_cells=5,
        empty_cells_count=1,
        rows=[row],
    )

    started = engine.start_typing(
        matrix=matrix,
        delay=0.001,
        countdown=0,
        extra_row_end_tabs=3,
    )
    assert started is True
    engine._thread.join(timeout=2.0)

    # Total tabs: 5 cell tabs + 3 extra tabs = 8
    tab_presses = [e for e in mock_kb.events if e == ("press", Key.tab)]
    assert len(tab_presses) == 8

    # Typed scores: only 4 (one was blank)
    actual_types = [e[1] for e in mock_kb.events if e[0] == "type"]
    assert actual_types == ["3", "3", "3", "3"]


def test_mode_maximum_speed_execution():
    """Verify that mode 2 (characteristics) runs cleanly with maximum speed delay=0.02s."""
    mock_kb = MockKeyboard()
    engine = TyperEngine(keyboard_controller=mock_kb)

    row = ["3"] * 8
    matrix = ScoreMatrix(
        total_rows=1,
        total_columns=8,
        total_cells=8,
        empty_cells_count=0,
        rows=[row],
    )

    started = engine.start_typing(
        matrix=matrix,
        delay=0.02,
        countdown=0,
        extra_row_end_tabs=4,
    )
    assert started is True
    engine._thread.join(timeout=2.0)
    assert engine.is_running is False
    # 8 cell tabs + 4 extra tabs = 12
    tab_presses = [e for e in mock_kb.events if e == ("press", Key.tab)]
    assert len(tab_presses) == 12
