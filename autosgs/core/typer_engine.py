"""
Typer Engine module for AutoSGS.
Simulates keyboard typing and Tab navigation row-by-row on a background thread.
Supports immediate emergency stop, progress reporting, and customizable delay.
"""

import sys
import threading
import time
from typing import Callable, Optional
from pynput.keyboard import Controller, Key

from autosgs.core.clipboard_parser import ScoreMatrix


def is_macos_accessibility_enabled() -> bool:
    """
    Checks if Accessibility permissions are granted on macOS.
    Returns True on non-macOS platforms or if granted on macOS.
    """
    if sys.platform != "darwin":
        return True
    try:
        from ApplicationServices import AXIsProcessTrusted
        return bool(AXIsProcessTrusted())
    except Exception:
        return True


class TyperEngine:
    """
    Simulates horizontal-first keyboard input (Row-by-Row, Cell + Tab)
    with non-blocking thread execution and instant emergency stop.
    """

    def __init__(self, keyboard_controller: Optional[Controller] = None):
        self.keyboard = keyboard_controller if keyboard_controller is not None else Controller()
        self._stop_event = threading.Event()
        self._thread: Optional[threading.Thread] = None
        self._is_active = False

    @property
    def is_running(self) -> bool:
        """Returns True if the engine is currently counting down or typing."""
        return self._is_active and (self._thread is not None and self._thread.is_alive())

    def start_typing(
        self,
        matrix: ScoreMatrix,
        delay: float = 0.1,
        countdown: int = 0,
        extra_row_end_tabs: int = 0,
        on_countdown: Optional[Callable[[int], None]] = None,
        on_progress: Optional[Callable[[int, int, int, int, str], None]] = None,
        on_finished: Optional[Callable[[int], None]] = None,
        on_stopped: Optional[Callable[[str], None]] = None,
        on_error: Optional[Callable[[Exception], None]] = None,
    ) -> bool:
        """
        Starts typing on a background thread.
        extra_row_end_tabs: number of additional Tab keystrokes to send after finishing each row.
        Returns False if already running or matrix is empty.
        """
        if self.is_running:
            return False

        if matrix.is_empty:
            if on_stopped:
                on_stopped("ไม่พบข้อมูลที่จะพิมพ์")
            return False

        self._stop_event.clear()
        self._is_active = True

        self._thread = threading.Thread(
            target=self._worker,
            args=(matrix, delay, countdown, extra_row_end_tabs, on_countdown, on_progress, on_finished, on_stopped, on_error),
            name="AutoSGS-TyperThread",
            daemon=True,
        )
        self._thread.start()
        return True

    def stop(self, reason: str = "หยุดฉุกเฉิน") -> None:
        """Signals the background thread to stop immediately."""
        self._stop_event.set()

    def _worker(
        self,
        matrix: ScoreMatrix,
        delay: float,
        countdown: int,
        extra_row_end_tabs: int,
        on_countdown: Optional[Callable[[int], None]],
        on_progress: Optional[Callable[[int, int, int, int, str], None]],
        on_finished: Optional[Callable[[int], None]],
        on_stopped: Optional[Callable[[str], None]],
        on_error: Optional[Callable[[Exception], None]],
    ) -> None:
        try:
            # 1. Countdown Phase
            if countdown > 0:
                for sec in range(countdown, 0, -1):
                    if self._stop_event.is_set():
                        self._is_active = False
                        if on_stopped:
                            on_stopped("ยกเลิกระหว่างนับถอยหลัง")
                        return

                    if on_countdown:
                        on_countdown(sec)

                    # Sleep 1 second in 50ms intervals to be responsive to stop_event
                    for _ in range(20):
                        if self._stop_event.wait(timeout=0.05):
                            self._is_active = False
                            if on_stopped:
                                on_stopped("ยกเลิกระหว่างนับถอยหลัง")
                            return

            # Check stop before starting typing
            if self._stop_event.is_set():
                self._is_active = False
                if on_stopped:
                    on_stopped("ถูกหยุดก่อนเริ่มพิมพ์")
                return

            # 2. Typing Phase (Row-by-Row, Cell + Tab)
            cell_counter = 0
            total_cells = matrix.total_cells

            for r_idx, row in enumerate(matrix.rows):
                for c_idx, cell_value in enumerate(row):
                    if self._stop_event.is_set():
                        self._is_active = False
                        if on_stopped:
                            on_stopped("หยุดฉุกเฉินโดยผู้ใช้ (ESC)")
                        return

                    cell_counter += 1

                    if on_progress:
                        on_progress(r_idx + 1, matrix.total_rows, cell_counter, total_cells, cell_value)

                    # If cell has a value, type each character
                    if cell_value:
                        self.keyboard.type(cell_value)

                    # Send Tab keystroke
                    self.keyboard.press(Key.tab)
                    self.keyboard.release(Key.tab)

                    # Wait delay (using stop_event.wait for sub-millisecond stop latency)
                    if delay > 0:
                        if self._stop_event.wait(timeout=delay):
                            self._is_active = False
                            if on_stopped:
                                on_stopped("หยุดฉุกเฉินโดยผู้ใช้ (ESC)")
                            return

                # Send extra Tab keystrokes at row end (e.g. to skip summary columns to next student)
                if extra_row_end_tabs > 0:
                    for _ in range(extra_row_end_tabs):
                        if self._stop_event.is_set():
                            self._is_active = False
                            if on_stopped:
                                on_stopped("หยุดฉุกเฉินโดยผู้ใช้ (ESC)")
                            return

                        self.keyboard.press(Key.tab)
                        self.keyboard.release(Key.tab)

                        if delay > 0:
                            if self._stop_event.wait(timeout=delay):
                                self._is_active = False
                                if on_stopped:
                                    on_stopped("หยุดฉุกเฉินโดยผู้ใช้ (ESC)")
                                return

            # Completed successfully
            self._is_active = False
            if on_finished:
                on_finished(cell_counter)

        except Exception as e:
            self._is_active = False
            if on_error:
                on_error(e)
            elif on_stopped:
                on_stopped(f"เกิดข้อผิดพลาด: {e}")
