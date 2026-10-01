"""
Unit tests for autosgs.core.sound_notifier
"""

import time
import pytest
from autosgs.core.sound_notifier import (
    play_countdown_beep,
    play_success_sound,
    play_stop_sound,
)


def test_sound_notifier_enabled_and_disabled():
    # Calling with enabled=False should execute silently without error
    play_countdown_beep(enabled=False)
    play_success_sound(enabled=False)
    play_stop_sound(enabled=False)

    # Calling with enabled=True should dispatch to non-blocking threads without raising exceptions
    play_countdown_beep(enabled=True)
    play_success_sound(enabled=True)
    play_stop_sound(enabled=True)

    # Give threads a tiny moment to run
    time.sleep(0.1)
