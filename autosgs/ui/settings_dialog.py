"""
Settings Dialog for AutoSGS.
Allows configuring Hotkeys, Sound Alerts, Countdown duration, Theme, and Font/UI Scale.
Uses the modern 'Prompt' font and features high-contrast dark buttons pinned at bottom.
"""

from typing import Callable, Optional
import customtkinter as ctk

from autosgs.core.config_manager import (
    AppConfig,
    save_config,
    DISPLAY_TO_SCALE,
    SCALE_TO_DISPLAY,
)
from autosgs.core.font_manager import get_ui_font


class SettingsDialog(ctk.CTkToplevel):
    def __init__(
        self,
        parent,
        config: AppConfig,
        on_save_callback: Optional[Callable[[AppConfig], None]] = None,
    ):
        super().__init__(parent)

        self.config = config
        self.on_save_callback = on_save_callback

        self.title("การตั้งค่า - AutoSGS")
        self.geometry("450x590")
        self.minsize(400, 480)
        self.resizable(True, True)

        # Make modal
        self.transient(parent)
        self.grab_set()

        self._build_ui()
        self._load_values()

    def _build_ui(self):
        # 1. Header (Pinned at top)
        header = ctk.CTkLabel(
            self,
            text="⚙️ ตั้งค่าระบบ AutoSGS",
            font=get_ui_font(size=20, weight="bold"),
        )
        header.pack(side="top", pady=(16, 8))

        # 2. Bottom Action Buttons (Pinned at bottom FIRST - high contrast darker colors)
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(side="bottom", padx=24, pady=(10, 16), fill="x")

        btn_cancel = ctk.CTkButton(
            btn_frame,
            text="ยกเลิก",
            fg_color="#424949",
            hover_color="#2c3e50",
            text_color="white",
            width=110,
            height=38,
            font=get_ui_font(size=14),
            command=self.destroy,
        )
        btn_cancel.pack(side="left", padx=(0, 10))

        btn_save = ctk.CTkButton(
            btn_frame,
            text="💾 บันทึกการตั้งค่า",
            fg_color="#196f3d",
            hover_color="#145a32",
            text_color="white",
            width=180,
            height=38,
            font=get_ui_font(size=14, weight="bold"),
            command=self._on_save,
        )
        btn_save.pack(side="right")

        # 3. Form Content (Scrollable frame so all fields are accessible on any scaling)
        scroll_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll_frame.pack(side="top", fill="both", expand=True, padx=16, pady=4)

        form_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        form_frame.pack(fill="x", padx=8, pady=4)

        # A. Hotkey Selection
        lbl_hotkey = ctk.CTkLabel(
            form_frame,
            text="ปุ่มลัดเริ่มพิมพ์ (Global Hotkey):",
            font=get_ui_font(size=14, weight="bold"),
        )
        lbl_hotkey.grid(row=0, column=0, sticky="w", pady=(6, 2))

        self.hotkey_combo = ctk.CTkComboBox(
            form_frame,
            values=["F2", "F3", "F4", "F7", "F8", "F9", "F10", "ctrl+alt+v"],
            width=220,
            font=get_ui_font(size=13),
        )
        self.hotkey_combo.grid(row=1, column=0, sticky="w", pady=(0, 4))

        hotkey_hint = ctk.CTkLabel(
            form_frame,
            text="* ปุ่มหยุดฉุกเฉิน (Emergency Stop) คือ ESC เสมอ",
            font=get_ui_font(size=11),
            text_color="gray",
        )
        hotkey_hint.grid(row=2, column=0, sticky="w", pady=(0, 10))

        # B. Font / UI Size Setting
        lbl_scale = ctk.CTkLabel(
            form_frame,
            text="ขนาดตัวอักษรและการแสดงผล (Font / UI Size):",
            font=get_ui_font(size=14, weight="bold"),
        )
        lbl_scale.grid(row=3, column=0, sticky="w", pady=(4, 2))

        self.scale_combo = ctk.CTkComboBox(
            form_frame,
            values=list(DISPLAY_TO_SCALE.keys()),
            width=220,
            font=get_ui_font(size=13),
        )
        self.scale_combo.grid(row=4, column=0, sticky="w", pady=(0, 12))

        # C. Countdown duration
        lbl_countdown = ctk.CTkLabel(
            form_frame,
            text="เวลานับถอยหลังก่อนพิมพ์ (วินาที):",
            font=get_ui_font(size=14, weight="bold"),
        )
        lbl_countdown.grid(row=5, column=0, sticky="w", pady=(4, 2))

        self.countdown_combo = ctk.CTkComboBox(
            form_frame,
            values=["1", "2", "3", "4", "5"],
            width=120,
            font=get_ui_font(size=13),
        )
        self.countdown_combo.grid(row=6, column=0, sticky="w", pady=(0, 12))

        # D. Sound Notifications
        self.sound_var = ctk.BooleanVar(value=self.config.sound_enabled)
        self.sound_switch = ctk.CTkSwitch(
            form_frame,
            text="เปิดเสียงแจ้งเตือน (Beep / Chime)",
            variable=self.sound_var,
            font=get_ui_font(size=13),
        )
        self.sound_switch.grid(row=7, column=0, sticky="w", pady=(4, 12))

        # E. Theme
        lbl_theme = ctk.CTkLabel(
            form_frame,
            text="ธีมการแสดงผล (Theme):",
            font=get_ui_font(size=14, weight="bold"),
        )
        lbl_theme.grid(row=8, column=0, sticky="w", pady=(4, 2))

        self.theme_combo = ctk.CTkComboBox(
            form_frame,
            values=["System", "Dark", "Light"],
            width=160,
            font=get_ui_font(size=13),
        )
        self.theme_combo.grid(row=9, column=0, sticky="w", pady=(0, 10))

    def _load_values(self):
        self.hotkey_combo.set(self.config.start_hotkey)
        self.scale_combo.set(SCALE_TO_DISPLAY.get(self.config.ui_scale, "ใหญ่ (115%)"))
        self.countdown_combo.set(str(self.config.countdown_seconds))
        self.sound_var.set(self.config.sound_enabled)
        self.theme_combo.set(self.config.theme)

    def _on_save(self):
        try:
            self.config.start_hotkey = self.hotkey_combo.get().strip() or "F2"
            selected_display = self.scale_combo.get().strip()
            self.config.ui_scale = DISPLAY_TO_SCALE.get(selected_display, "Large")
            self.config.countdown_seconds = int(self.countdown_combo.get())
            self.config.sound_enabled = self.sound_var.get()
            self.config.theme = self.theme_combo.get()

            # Save to file
            save_config(self.config)

            # Apply theme immediately
            ctk.set_appearance_mode(self.config.theme)

            # Callback to update main app
            if self.on_save_callback:
                self.on_save_callback(self.config)

            self.destroy()
        except Exception as e:
            print(f"[SettingsDialog] Error saving: {e}")
