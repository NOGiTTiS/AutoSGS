"""
Main Application Window for AutoSGS.
Features compact floating view, collapsible preview grid, speed control,
status badge, progress tracking, and integration with TyperEngine and HotkeyManager.
Supports configurable UI Scaling and uses the modern 'Prompt' font.
"""

import sys
import tkinter as tk
from typing import Optional
import customtkinter as ctk

from autosgs.core.config_manager import (
    AppConfig,
    load_config,
    save_config,
    get_scaling_factor,
    MODE_SPECS,
    DISPLAY_TO_MODE,
    MODE_TO_DISPLAY,
    get_mode_delay,
    set_mode_delay,
)
from autosgs.core.clipboard_parser import (
    ScoreMatrix,
    load_matrix_from_clipboard,
    parse_tsv,
    get_clipboard_text,
)
from autosgs.core.typer_engine import TyperEngine
from autosgs.core.hotkey_manager import HotkeyManager
from autosgs.core.sound_notifier import play_countdown_beep, play_success_sound, play_stop_sound
from autosgs.core.font_manager import register_fonts, get_ui_font, FONT_FAMILY, get_asset_path, get_base_dir
from autosgs.ui.settings_dialog import SettingsDialog


class AutoSGSApp(ctk.CTk):
    COMPACT_HEIGHT = 445
    EXPANDED_HEIGHT = 725
    WINDOW_WIDTH = 520

    def __init__(self):
        # Register Prompt font family before creating widgets
        register_fonts()

        super().__init__()

        # Load configurations
        self.config = load_config()
        ctk.set_appearance_mode(self.config.theme)
        ctk.set_default_color_theme("blue")

        # Apply widget scaling for accessibility & larger fonts
        self.current_scaling = get_scaling_factor(self.config.ui_scale)
        ctk.set_widget_scaling(self.current_scaling)

        # Window settings
        self.title("NOGiTTiS : AutoSGS v1.0 - ระบบช่วยพิมพ์คะแนน")
        self.geometry(f"{self.WINDOW_WIDTH}x{self.COMPACT_HEIGHT}")
        self.minsize(self.WINDOW_WIDTH, self.COMPACT_HEIGHT)
        self.attributes("-topmost", self.config.always_on_top)

        # Set window icon
        icon_path = get_asset_path("assets/icon.ico")
        if icon_path.exists() and sys.platform == "win32":
            try:
                self.iconbitmap(str(icon_path))
            except Exception:
                pass

        # State variables
        self.matrix = ScoreMatrix()
        self.is_expanded = False
        self.engine = TyperEngine()
        self._last_clipboard_text = ""

        # Build UI
        self._build_ui()

        # Initialize Hotkey Manager
        self.hotkey_manager = HotkeyManager(
            on_start=self._handle_hotkey_start,
            on_stop=self._handle_hotkey_stop,
            start_hotkey=self.config.start_hotkey,
        )
        self.hotkey_manager.start()

        # Initial clipboard load
        self.refresh_clipboard(show_notice=False)

        # Auto-detect clipboard changes on focus and via lightweight polling loop (800ms)
        self.bind("<FocusIn>", self._on_window_focus)
        self._clipboard_poll_job = self.after(800, self._poll_clipboard)

        # Handle window close
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _build_ui(self):
        # 1. Top Bar (Header, Topmost, Settings)
        top_bar = ctk.CTkFrame(self, fg_color="transparent")
        top_bar.pack(fill="x", padx=16, pady=(12, 6))

        title_lbl = ctk.CTkLabel(
            top_bar,
            text="⚡ AutoSGS",
            font=get_ui_font(size=20, weight="bold"),
            text_color=("#1f538d", "#3b8ed0"),
        )
        title_lbl.pack(side="left")

        # Settings button - prominent dark color
        btn_settings = ctk.CTkButton(
            top_bar,
            text="⚙️ ตั้งค่า",
            width=80,
            height=32,
            fg_color=("#2c3e50", "#1a252f"),
            hover_color=("#1a252f", "#11171d"),
            text_color="white",
            font=get_ui_font(size=13, weight="bold"),
            command=self._open_settings,
        )
        btn_settings.pack(side="right")

        # Always on top switch
        self.topmost_var = ctk.BooleanVar(value=self.config.always_on_top)
        self.topmost_switch = ctk.CTkSwitch(
            top_bar,
            text="อยู่บนสุด",
            variable=self.topmost_var,
            font=get_ui_font(size=13),
            command=self._toggle_always_on_top,
            width=85,
        )
        self.topmost_switch.pack(side="right", padx=(0, 10))

        # 2. Mode Selector
        mode_frame = ctk.CTkFrame(self, fg_color="transparent")
        mode_frame.pack(fill="x", padx=16, pady=(0, 4))

        mode_lbl = ctk.CTkLabel(
            mode_frame,
            text="โหมด:",
            font=get_ui_font(size=13, weight="bold"),
        )
        mode_lbl.pack(side="left", padx=(0, 8))

        self.mode_segmented = ctk.CTkSegmentedButton(
            mode_frame,
            values=[
                MODE_SPECS["scores"]["display_name"],
                MODE_SPECS["characteristics"]["display_name"],
                MODE_SPECS["reading_analysis"]["display_name"],
            ],
            command=self._on_mode_change,
            font=get_ui_font(size=12, weight="bold"),
            height=32,
        )
        self.mode_segmented.pack(side="left", fill="x", expand=True)
        current_display = MODE_TO_DISPLAY.get(self.config.entry_mode, MODE_SPECS["scores"]["display_name"])
        self.mode_segmented.set(current_display)

        # 3. Status Badge & Info
        self.status_frame = ctk.CTkFrame(self, corner_radius=8, fg_color=("gray90", "#2b2b2b"))
        self.status_frame.pack(fill="x", padx=16, pady=4)

        self.status_lbl = ctk.CTkLabel(
            self.status_frame,
            text="🟢 พร้อมทำงาน (กด F2 หรือปุ่มเริ่ม)",
            font=get_ui_font(size=15, weight="bold"),
            text_color=("#27ae60", "#2ecc71"),
        )
        self.status_lbl.pack(pady=(8, 2))

        self.progress_detail_lbl = ctk.CTkLabel(
            self.status_frame,
            text="รอข้อมูลจาก Clipboard",
            font=get_ui_font(size=13),
            text_color="gray",
        )
        self.progress_detail_lbl.pack(pady=(0, 8))

        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(self)
        self.progress_bar.pack(fill="x", padx=16, pady=(4, 8))
        self.progress_bar.set(0.0)

        # Save Reminder Banner (for characteristics and reading_analysis modes)
        self.reminder_frame = ctk.CTkFrame(
            self,
            corner_radius=8,
            fg_color=("#fef3c7", "#451a03"),
            border_width=1.5,
            border_color=("#f59e0b", "#d97706"),
        )
        # Will be packed above btn_action when save reminder is active

        self.reminder_lbl = ctk.CTkLabel(
            self.reminder_frame,
            text="💾 อย่าลืมกดปุ่ม \"บันทึก\" ในระบบ SGS ด้วยนะครับ!",
            font=get_ui_font(size=13, weight="bold"),
            text_color=("#92400e", "#fbbf24"),
        )
        self.reminder_lbl.pack(side="left", padx=(12, 6), pady=6, fill="x", expand=True)

        self.btn_dismiss_reminder = ctk.CTkButton(
            self.reminder_frame,
            text="✕",
            width=24,
            height=24,
            fg_color="transparent",
            hover_color=("#fde68a", "#78350f"),
            text_color=("#92400e", "#fbbf24"),
            font=get_ui_font(size=12, weight="bold"),
            command=self._hide_save_reminder,
        )
        self.btn_dismiss_reminder.pack(side="right", padx=(0, 6), pady=6)

        # 3. Main Action Controls (Start / Stop Button)
        self.btn_action = ctk.CTkButton(
            self,
            text=f"▶ เริ่มพิมพ์ ({self.config.countdown_seconds}s) หรือกด {self.config.start_hotkey}",
            font=get_ui_font(size=16, weight="bold"),
            height=46,
            fg_color="#2980b9",
            hover_color="#3498db",
            command=self._on_action_button_click,
        )
        self.btn_action.pack(fill="x", padx=16, pady=6)

        # 4. Delay / Speed Slider
        slider_frame = ctk.CTkFrame(self, fg_color="transparent")
        slider_frame.pack(fill="x", padx=16, pady=4)

        self.delay_lbl = ctk.CTkLabel(
            slider_frame,
            text="",
            font=get_ui_font(size=13),
        )
        self.delay_lbl.pack(anchor="w")

        self.delay_slider = ctk.CTkSlider(
            slider_frame,
            from_=0.01,
            to=0.50,
            number_of_steps=49,
            command=self._on_delay_change,
        )
        self.delay_slider.pack(fill="x", pady=(2, 6))
        self._update_delay_ui()

        # 5. Collapsible Preview Accordion Header
        preview_header_frame = ctk.CTkFrame(self, fg_color="transparent")
        preview_header_frame.pack(fill="x", padx=16, pady=(6, 2))

        self.btn_toggle_preview = ctk.CTkButton(
            preview_header_frame,
            text="▼ ดูตัวอย่างข้อมูลในคลิปบอร์ด (Preview)",
            font=get_ui_font(size=13, weight="bold"),
            fg_color=("gray85", "#333333"),
            hover_color=("gray75", "#444444"),
            text_color=("black", "white"),
            height=34,
            command=self._toggle_preview,
        )
        self.btn_toggle_preview.pack(side="left", fill="x", expand=True)

        self.btn_refresh = ctk.CTkButton(
            preview_header_frame,
            text="🔄",
            width=38,
            height=34,
            font=get_ui_font(size=15),
            fg_color=("gray85", "#333333"),
            hover_color=("gray75", "#444444"),
            text_color=("black", "white"),
            command=lambda: self.refresh_clipboard(show_notice=True),
        )
        self.btn_refresh.pack(side="right", padx=(6, 0))

        # 6. Preview Panel (Expandable)
        self.preview_panel = ctk.CTkFrame(self, corner_radius=8)
        # (Will be packed when expanded)

        self.preview_summary_lbl = ctk.CTkLabel(
            self.preview_panel,
            text="คลิปบอร์ด: ยังไม่มีข้อมูล",
            font=get_ui_font(size=13, weight="bold"),
            text_color=("#1f538d", "#3b8ed0"),
        )
        self.preview_summary_lbl.pack(padx=10, pady=(8, 4), anchor="w")

        # Scrollable textbox for preview table
        self.preview_text = ctk.CTkTextbox(
            self.preview_panel,
            font=get_ui_font(size=13),
            wrap="none",
        )
        self.preview_text.pack(fill="both", expand=True, padx=10, pady=(4, 10))

    def _toggle_always_on_top(self):
        self.config.always_on_top = self.topmost_var.get()
        self.attributes("-topmost", self.config.always_on_top)
        save_config(self.config)

    def _update_delay_ui(self):
        """Updates slider position and label text according to the current mode's delay setting."""
        current_delay = get_mode_delay(self.config, self.config.entry_mode)
        self.delay_slider.set(current_delay)
        speed_tag = " ⚡ ความเร็วสูงสุด" if current_delay <= 0.02 else ""
        self.delay_lbl.configure(
            text=f"⏱ ความเร็วหน่วงเวลา: {current_delay:.2f} วินาที ({int(current_delay * 1000)} ms){speed_tag}"
        )

    def _on_delay_change(self, value: float):
        val = round(value, 2)
        set_mode_delay(self.config, self.config.entry_mode, val)
        speed_tag = " ⚡ ความเร็วสูงสุด" if val <= 0.02 else ""
        self.delay_lbl.configure(
            text=f"⏱ ความเร็วหน่วงเวลา: {val:.2f} วินาที ({int(val * 1000)} ms){speed_tag}"
        )
        save_config(self.config)

    def _on_mode_change(self, selected_display: str):
        mode_key = DISPLAY_TO_MODE.get(selected_display, "scores")
        self.config.entry_mode = mode_key
        save_config(self.config)
        self._hide_save_reminder()
        self._update_delay_ui()
        self.refresh_clipboard(show_notice=False)

    def _show_save_reminder(self):
        """Displays the amber reminder banner above the main action button."""
        try:
            self.reminder_frame.pack(fill="x", padx=16, pady=(0, 6), before=self.btn_action)
        except Exception:
            self.reminder_frame.pack(fill="x", padx=16, pady=(0, 6))

    def _hide_save_reminder(self):
        """Hides the save reminder banner."""
        self.reminder_frame.pack_forget()

    def _toggle_preview(self):
        self.is_expanded = not self.is_expanded
        if self.is_expanded:
            self.btn_toggle_preview.configure(text="▲ ซ่อนตัวอย่างข้อมูล (Hide Preview)")
            self.geometry(f"{self.WINDOW_WIDTH}x{self.EXPANDED_HEIGHT}")
            self.preview_panel.pack(fill="both", expand=True, padx=16, pady=(4, 12))
            self._render_preview()
        else:
            self.btn_toggle_preview.configure(text="▼ ดูตัวอย่างข้อมูลในคลิปบอร์ด (Preview)")
            self.preview_panel.pack_forget()
            self.geometry(f"{self.WINDOW_WIDTH}x{self.COMPACT_HEIGHT}")

    def _poll_clipboard(self):
        """Lightweight polling loop to auto-refresh preview when clipboard content changes."""
        if not self.engine.is_running:
            try:
                raw_text = get_clipboard_text()
                if raw_text != self._last_clipboard_text:
                    self._last_clipboard_text = raw_text
                    self.refresh_clipboard(show_notice=True)
            except Exception:
                pass
        self._clipboard_poll_job = self.after(800, self._poll_clipboard)

    def _on_window_focus(self, event=None):
        """Auto-refresh immediately when user switches focus to AutoSGS window."""
        if not self.engine.is_running:
            try:
                raw_text = get_clipboard_text()
                if raw_text != self._last_clipboard_text:
                    self._last_clipboard_text = raw_text
                    self.refresh_clipboard(show_notice=True)
            except Exception:
                pass

    def refresh_clipboard(self, show_notice: bool = False):
        raw_text = get_clipboard_text()
        self._last_clipboard_text = raw_text
        self.matrix = parse_tsv(raw_text)

        mode_spec = MODE_SPECS.get(self.config.entry_mode, MODE_SPECS["scores"])
        expected_cols = mode_spec["expected_cols"]

        if self.matrix.is_empty:
            msg = f"รอข้อมูลจากคลิปบอร์ด (โหมด: {mode_spec['label']})"
            self.progress_detail_lbl.configure(text=msg)
            self.preview_summary_lbl.configure(text=f"คลิปบอร์ด: ยังไม่มีข้อมูล (โหมด: {mode_spec['label']})")
        else:
            col_warning = ""
            if expected_cols is not None and self.matrix.total_columns != expected_cols:
                col_warning = f" ⚠️ (แนะนำ {expected_cols} ช่อง)"

            info = f"โหมด: {mode_spec['label']} | ตรวจพบ: {self.matrix.total_rows} คน × {self.matrix.total_columns} ช่อง{col_warning}"
            self.progress_detail_lbl.configure(text=info)
            self.preview_summary_lbl.configure(text=f"📊 {info} (เว้นว่าง {self.matrix.empty_cells_count} ช่อง)")

        if self.is_expanded:
            self._render_preview()

        if show_notice and not self.matrix.is_empty and not self.engine.is_running:
            self._set_status(
                "🟢 พร้อมทำงาน (อัปเดตข้อมูลอัตโนมัติ)",
                f"ตรวจพบข้อมูล {self.matrix.total_rows} คน × {self.matrix.total_columns} ช่อง",
                "#27ae60",
            )

    def _render_preview(self):
        self.preview_text.configure(state="normal")
        self.preview_text.delete("1.0", "end")

        mode_spec = MODE_SPECS.get(self.config.entry_mode, MODE_SPECS["scores"])

        if self.matrix.is_empty:
            self.preview_text.insert(
                "1.0",
                f"📌 โหมดปัจจุบัน: {mode_spec['label']}\n{mode_spec['desc']}\n\n"
                "ยังไม่มีข้อมูลในคลิปบอร์ด\n\nคำแนะนำ:\n"
                "1. ไปที่ Excel หรือ Google Sheets\n"
                "2. ลากคลุมคะแนนที่ต้องการ (1 คอลัมน์ หรือหลายคอลัมน์)\n"
                "3. กด Ctrl+C เพื่อคัดลอก\n"
                "4. กดปุ่ม 🔄 รีเฟรช หรือสลับกลับมาที่โปรแกรม"
            )
        else:
            extra_info = f" | ท้ายแถว: Tab เพิ่ม {mode_spec['extra_row_end_tabs']} ครั้ง" if mode_spec['extra_row_end_tabs'] > 0 else ""
            self.preview_text.insert("1.0", f"โหมด: {mode_spec['label']} ({mode_spec['desc']}){extra_info}\n\n")

            # Header
            header = f"{'คนที่':<6}"
            for c in range(self.matrix.total_columns):
                header += f"| {'ช่อง ' + str(c + 1):<10}"
            if mode_spec['extra_row_end_tabs'] > 0:
                header += f"| {'+Tab x ' + str(mode_spec['extra_row_end_tabs']):<12}"
            self.preview_text.insert("end", header + "\n" + "-" * len(header) + "\n")

            # Data rows
            for idx, row in enumerate(self.matrix.rows, start=1):
                line = f"{idx:<6}"
                for cell in row:
                    val = cell if cell != "" else "(ว่าง)"
                    line += f"| {val:<10}"
                if mode_spec['extra_row_end_tabs'] > 0:
                    line += f"| {'ข้ามคนถัดไป':<12}"
                self.preview_text.insert("end", line + "\n")

        self.preview_text.configure(state="disabled")

    def _set_status(self, title: str, detail: str, color: str):
        self.status_lbl.configure(text=title, text_color=color)
        self.progress_detail_lbl.configure(text=detail)

    def _open_settings(self):
        SettingsDialog(self, self.config, on_save_callback=self._on_settings_saved)

    def _on_settings_saved(self, new_cfg: AppConfig):
        self.config = new_cfg

        # Apply UI Scaling if changed
        new_scale = get_scaling_factor(self.config.ui_scale)
        if new_scale != self.current_scaling:
            self.current_scaling = new_scale
            ctk.set_widget_scaling(new_scale)

        # Update mode if changed
        current_display = MODE_TO_DISPLAY.get(self.config.entry_mode, MODE_SPECS["scores"]["display_name"])
        self.mode_segmented.set(current_display)
        self._update_delay_ui()

        # Update controls
        self.btn_action.configure(
            text=f"▶ เริ่มพิมพ์ ({self.config.countdown_seconds}s) หรือกด {self.config.start_hotkey}"
        )
        self.hotkey_manager.update_start_hotkey(self.config.start_hotkey)
        self.attributes("-topmost", self.config.always_on_top)
        self.topmost_var.set(self.config.always_on_top)

    # ---------------- Automation Control ----------------

    def _on_action_button_click(self):
        if self.engine.is_running:
            self._stop_typing("หยุดฉุกเฉินโดยผู้ใช้กดปุ่มในโปรแกรม")
        else:
            self._start_countdown_typing()

    def _handle_hotkey_start(self):
        # Triggered from background hotkey listener
        self.after(0, self._start_hotkey_typing)

    def _handle_hotkey_stop(self):
        # Triggered from background hotkey listener (ESC)
        self.after(0, lambda: self._stop_typing("หยุดฉุกเฉินโดยการกดปุ่ม ESC"))

    def _start_countdown_typing(self):
        self.refresh_clipboard(show_notice=False)
        if self.matrix.is_empty:
            self._set_status("⚠️ ไม่มีข้อมูล", "กรุณา Ctrl+C ตารางคะแนนจาก Excel ก่อนเริ่มพิมพ์", "#e67e22")
            return

        mode_spec = MODE_SPECS.get(self.config.entry_mode, MODE_SPECS["scores"])
        extra_tabs = mode_spec["extra_row_end_tabs"]
        current_delay = get_mode_delay(self.config, self.config.entry_mode)

        self._prepare_ui_for_typing()
        self.engine.start_typing(
            matrix=self.matrix,
            delay=current_delay,
            countdown=self.config.countdown_seconds,
            extra_row_end_tabs=extra_tabs,
            on_countdown=lambda sec: self.after(0, self._on_countdown_tick, sec),
            on_progress=lambda r, tr, c, tc, val: self.after(0, self._on_typing_progress, r, tr, c, tc, val),
            on_finished=lambda total: self.after(0, self._on_typing_finished, total),
            on_stopped=lambda reason: self.after(0, self._on_typing_stopped, reason),
        )

    def _start_hotkey_typing(self):
        if self.engine.is_running:
            return

        self.refresh_clipboard(show_notice=False)
        if self.matrix.is_empty:
            self._set_status("⚠️ ไม่มีข้อมูล", "ตรวจไม่พบข้อมูลในคลิปบอร์ด", "#e67e22")
            return

        mode_spec = MODE_SPECS.get(self.config.entry_mode, MODE_SPECS["scores"])
        extra_tabs = mode_spec["extra_row_end_tabs"]
        current_delay = get_mode_delay(self.config, self.config.entry_mode)

        self._prepare_ui_for_typing()
        # Direct typing without countdown when triggered by hotkey
        self.engine.start_typing(
            matrix=self.matrix,
            delay=current_delay,
            countdown=0,
            extra_row_end_tabs=extra_tabs,
            on_progress=lambda r, tr, c, tc, val: self.after(0, self._on_typing_progress, r, tr, c, tc, val),
            on_finished=lambda total: self.after(0, self._on_typing_finished, total),
            on_stopped=lambda reason: self.after(0, self._on_typing_stopped, reason),
        )

    def _stop_typing(self, reason: str):
        if self.engine.is_running:
            self.engine.stop(reason)

    def _prepare_ui_for_typing(self):
        self._hide_save_reminder()
        self.btn_action.configure(
            text="⏹ หยุดฉุกเฉิน (ESC)",
            fg_color="#c0392b",
            hover_color="#e74c3c",
        )
        self.progress_bar.set(0.0)

    def _on_countdown_tick(self, sec: int):
        self._set_status(f"⏳ สลับไปคลิกช่องแรก! ({sec})", "กำลังนับถอยหลัง...", "#f39c12")
        play_countdown_beep(self.config.sound_enabled)

    def _on_typing_progress(self, row: int, total_rows: int, cell: int, total_cells: int, val: str):
        ratio = cell / max(total_cells, 1)
        self.progress_bar.set(ratio)
        val_display = val if val else "(ข้ามด้วย Tab)"
        self._set_status(
            f"✍️ กำลังพิมพ์... คนที่ {row}/{total_rows}",
            f"ช่องที่ {cell}/{total_cells} -> {val_display}",
            "#2980b9",
        )

    def _on_typing_finished(self, total_cells: int):
        self.progress_bar.set(1.0)
        self.btn_action.configure(
            text=f"▶ เริ่มพิมพ์ ({self.config.countdown_seconds}s) หรือกด {self.config.start_hotkey}",
            fg_color="#2980b9",
            hover_color="#3498db",
        )

        mode_spec = MODE_SPECS.get(self.config.entry_mode, MODE_SPECS["scores"])
        if mode_spec.get("show_save_reminder", False):
            self.reminder_lbl.configure(
                text=mode_spec.get("reminder_message", "💾 กรุณากดปุ่ม \"บันทึก\" ในระบบ SGS ด้วยนะครับ!")
            )
            self._show_save_reminder()
            self._set_status(
                "🎉 พิมพ์เสร็จแล้ว! 💾 อย่าลืมกดบันทึกใน SGS",
                f"กรอกคะแนนครบถ้วนแล้ว {total_cells} ช่อง 👉 กรุณากดปุ่มบันทึกในระบบ SGS",
                "#d97706",
            )
        else:
            self._hide_save_reminder()
            self._set_status(
                "🎉 พิมพ์คะแนนเสร็จสมบูรณ์!",
                f"กรอกคะแนนเรียบร้อยแล้วทั้งหมด {total_cells} ช่อง",
                "#27ae60",
            )
        play_success_sound(self.config.sound_enabled)

    def _on_typing_stopped(self, reason: str):
        self.btn_action.configure(
            text=f"▶ เริ่มพิมพ์ ({self.config.countdown_seconds}s) หรือกด {self.config.start_hotkey}",
            fg_color="#2980b9",
            hover_color="#3498db",
        )
        self._set_status(
            "🛑 หยุดการพิมพ์แล้ว",
            reason,
            "#e74c3c",
        )
        play_stop_sound(self.config.sound_enabled)

    def _on_close(self):
        # Cancel clipboard poll loop
        if hasattr(self, "_clipboard_poll_job"):
            try:
                self.after_cancel(self._clipboard_poll_job)
            except Exception:
                pass
        # Stop background hotkey listener
        if hasattr(self, "hotkey_manager"):
            self.hotkey_manager.stop()
        if hasattr(self, "engine") and self.engine.is_running:
            self.engine.stop()
        self.destroy()


def run_app():
    register_fonts()
    app = AutoSGSApp()
    app.mainloop()


if __name__ == "__main__":
    run_app()
