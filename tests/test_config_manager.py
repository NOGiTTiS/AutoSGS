"""
Unit tests for autosgs.core.config_manager
"""

import tempfile
from pathlib import Path
from autosgs.core.config_manager import (
    AppConfig,
    load_config,
    save_config,
    get_scaling_factor,
    get_mode_delay,
    set_mode_delay,
)


def test_default_config():
    config = AppConfig()
    assert config.delay_seconds == 0.1
    assert config.delay_scores == 0.10
    assert config.delay_characteristics == 0.02
    assert config.delay_reading_analysis == 0.02
    assert config.countdown_seconds == 3
    assert config.start_hotkey == "F2"
    assert config.always_on_top is True
    assert config.sound_enabled is True
    assert config.ui_scale == "Large"


def test_get_scaling_factor():
    assert get_scaling_factor("Standard") == 1.0
    assert get_scaling_factor("Large") == 1.15
    assert get_scaling_factor("Extra Large") == 1.30
    assert get_scaling_factor("Unknown") == 1.15


def test_per_mode_delay_helpers():
    cfg = AppConfig()
    # Default delays
    assert get_mode_delay(cfg, "scores") == 0.10
    assert get_mode_delay(cfg, "characteristics") == 0.02
    assert get_mode_delay(cfg, "reading_analysis") == 0.02

    # Modify characteristics delay only
    set_mode_delay(cfg, "characteristics", 0.05)
    assert get_mode_delay(cfg, "characteristics") == 0.05
    assert get_mode_delay(cfg, "scores") == 0.10
    assert get_mode_delay(cfg, "reading_analysis") == 0.02

    # Modify scores delay only
    set_mode_delay(cfg, "scores", 0.15)
    assert get_mode_delay(cfg, "scores") == 0.15
    assert get_mode_delay(cfg, "characteristics") == 0.05


def test_save_and_load_config():
    with tempfile.TemporaryDirectory() as tmp_dir:
        test_file = Path(tmp_dir) / "test_config.json"

        # Non-existing file returns default
        cfg = load_config(custom_path=test_file)
        assert cfg.delay_seconds == 0.1
        assert cfg.delay_characteristics == 0.02
        assert cfg.ui_scale == "Large"

        # Modify and save
        cfg.delay_scores = 0.18
        cfg.delay_characteristics = 0.03
        cfg.delay_reading_analysis = 0.04
        cfg.start_hotkey = "F8"
        cfg.always_on_top = False
        cfg.ui_scale = "Extra Large"
        saved = save_config(cfg, custom_path=test_file)
        assert saved is True

        # Reload
        reloaded = load_config(custom_path=test_file)
        assert reloaded.delay_scores == 0.18
        assert reloaded.delay_characteristics == 0.03
        assert reloaded.delay_reading_analysis == 0.04
        assert reloaded.start_hotkey == "F8"
        assert reloaded.always_on_top is False
        assert reloaded.ui_scale == "Extra Large"
