"""
Integration tests for UI events and TyperEngine thread-safety.
"""

import time
import pytest
from autosgs.core.clipboard_parser import parse_tsv
from autosgs.core.typer_engine import TyperEngine


class MockEventCollector:
    """Mock collector simulating thread-safe UI callbacks."""
    def __init__(self):
        self.progress_events = []
        self.countdown_events = []
        self.finished_events = []
        self.stopped_events = []

    def on_countdown(self, sec):
        self.countdown_events.append(sec)

    def on_progress(self, row, total_rows, cell, total_cells, val):
        self.progress_events.append((row, total_rows, cell, total_cells, val))

    def on_finished(self, total):
        self.finished_events.append(total)

    def on_stopped(self, reason):
        self.stopped_events.append(reason)


def test_ui_thread_safe_event_flow():
    collector = MockEventCollector()
    engine = TyperEngine()

    sample_tsv = "15\t18\t20\r\n19\t\t17\r\n"
    matrix = parse_tsv(sample_tsv)

    assert matrix.total_rows == 2
    assert matrix.total_columns == 3
    assert matrix.total_cells == 6

    # Start typing with high speed for automated testing
    started = engine.start_typing(
        matrix=matrix,
        delay=0.005,
        countdown=0,
        on_progress=collector.on_progress,
        on_finished=collector.on_finished,
        on_stopped=collector.on_stopped,
    )
    assert started is True

    # Wait for completion
    engine._thread.join(timeout=2.0)
    assert engine.is_running is False

    # Check event counts and progression
    assert len(collector.finished_events) == 1
    assert collector.finished_events[0] == 6
    assert len(collector.progress_events) == 6

    # Verify first and last progress events
    first_event = collector.progress_events[0]
    assert first_event == (1, 2, 1, 6, "15")

    # Empty cell in row 2 col 2
    empty_cell_event = collector.progress_events[4]
    assert empty_cell_event == (2, 2, 5, 6, "")
