"""
Phase 1 Interactive Manual Test Script for AutoSGS.
Run this script to test the Core Engine, Hotkeys, Sound, and Traversal logic.
"""

import sys
import time
import pyperclip
from autosgs.core.clipboard_parser import load_matrix_from_clipboard, parse_tsv
from autosgs.core.typer_engine import TyperEngine
from autosgs.core.hotkey_manager import HotkeyManager
from autosgs.core.sound_notifier import play_countdown_beep, play_success_sound, play_stop_sound


def print_banner():
    print("=" * 60)
    print("        AutoSGS - Phase 1 Core Engine Interactive Test")
    print("=" * 60)


def run_clipboard():
    print("\n--- 1. ทดสอบอ่านข้อมูลจาก Clipboard ---")
    matrix = load_matrix_from_clipboard()
    if matrix.is_empty:
        print("[!] คลิปบอร์ดว่าง หรือไม่ได้ก๊อปปี้ข้อความมา")
        print("    กำลังใส่ตัวอย่างคะแนน 3 แถว x 3 คอลัมน์ (มีช่องว่าง) ลงคลิปบอร์ดให้ทดสอบ...")
        sample_tsv = "18\t19\t20\r\n15\t\t17\r\n20\t19.5\t18\r\n"
        pyperclip.copy(sample_tsv)
        matrix = parse_tsv(sample_tsv)

    print(f"ผลการวิเคราะห์คลิปบอร์ด: {matrix.summary()}")
    print("\nตัวอย่างข้อมูลในตาราง:")
    for idx, row in enumerate(matrix.rows, start=1):
        formatted_cells = [f"[{cell if cell != '' else 'ว่าง'}]" for cell in row]
        print(f"  แถวที่ {idx}: {' -> '.join(formatted_cells)}")
    return matrix


def run_sounds():
    print("\n--- 2. ทดสอบระบบเสียงแจ้งเตือน ---")
    print("กำลังเล่นเสียงนับถอยหลัง (Beep)...")
    play_countdown_beep()
    time.sleep(0.5)
    print("กำลังเล่นเสียงสำเร็จ (Success Chime)...")
    play_success_sound()
    time.sleep(0.5)
    print("กำลังเล่นเสียงหยุดฉุกเฉิน (Stop Alert)...")
    play_stop_sound()
    time.sleep(0.5)
    print("[✓] ทดสอบเสียงเสร็จสิ้น")


def run_countdown_typing(matrix):
    print("\n--- 3. ทดสอบนับถอยหลัง 3 วินาที แล้วพิมพ์ลงช่อง ---")
    print("คำแนะนำ: เมื่อกดยืนยัน ให้สลับหน้าต่างไปที่ Notepad หรือ mock_sgs.html และคลิกช่องแรก")
    input("กด [Enter] เพื่อเริ่มนับถอยหลัง 3 วินาที...")

    engine = TyperEngine()

    def on_cd(sec):
        print(f"  [นับถอยหลัง] {sec}...")
        play_countdown_beep()

    def on_prog(row, total_rows, cell, total_cells, val):
        display_val = val if val else "(ว่าง-กดTab)"
        print(f"  [กำลังพิมพ์] แถว {row}/{total_rows} | ช่อง {cell}/{total_cells} -> {display_val}")

    def on_fin(total):
        print(f"\n[✓] พิมพ์คะแนนเสร็จสิ้นครบทั้ง {total} ช่องแล้ว!")
        play_success_sound()

    def on_stp(reason):
        print(f"\n[!] หยุดการพิมพ์: {reason}")
        play_stop_sound()

    engine.start_typing(
        matrix=matrix,
        delay=0.15,
        countdown=3,
        on_countdown=on_cd,
        on_progress=on_prog,
        on_finished=on_fin,
        on_stopped=on_stp,
    )

    # Wait for typing to finish or user to stop
    while engine.is_running:
        time.sleep(0.1)


def run_hotkey_typing(matrix):
    print("\n--- 4. ทดสอบพิมพ์ด้วยปุ่มลัด Global Hotkey (F2) และหยุดด้วย (ESC) ---")
    print("คำแนะนำ:")
    print("  1. สลับไปที่ Notepad หรือ mock_sgs.html และคลิกที่ช่องแรก")
    print("  2. กดปุ่ม [F2] บนคีย์บอร์ดของคุณเพื่อเริ่มพิมพ์อัตโนมัติ")
    print("  3. กดปุ่ม [ESC] ได้ทุกเมื่อเพื่อทดสอบ 'หยุดฉุกเฉิน'")
    print("  (กด Ctrl+C ในหน้าต่างนี้เพื่อออกจากการทดสอบ)\n")

    engine = TyperEngine()

    def do_start():
        if engine.is_running:
            print("[Hotkey] โปรแกรมกำลังทำงานอยู่แล้ว")
            return
        print("[Hotkey] ตรวจพบการกด F2 -> เริ่มพิมพ์ทันที!")
        engine.start_typing(
            matrix=matrix,
            delay=0.15,
            countdown=0,
            on_progress=lambda r, tr, c, tc, v: print(f"  [F2 พิมพ์] ช่อง {c}/{tc} -> {v if v else '(Tab)'}"),
            on_finished=lambda total: (print(f"[✓] สำเร็จ {total} ช่อง!"), play_success_sound()),
            on_stopped=lambda reason: (print(f"[!] {reason}"), play_stop_sound()),
        )

    def do_stop():
        if engine.is_running:
            print("[Hotkey] ตรวจพบการกด ESC -> สั่งหยุดฉุกเฉินทันที!")
            engine.stop("หยุดฉุกเฉินโดยการกด ESC")

    hotkey_mgr = HotkeyManager(on_start=do_start, on_stop=do_stop, start_hotkey="F2")
    if not hotkey_mgr.start():
        print("[!] ไม่สามารถเริ่ม Hotkey Listener ได้")
        return

    print(">> Hotkey Listener เปิดทำงานแล้ว (F2 = เริ่ม, ESC = หยุดฉุกเฉิน) <<")
    print("กด Enter เพื่อจบการทดสอบ Hotkey...")
    try:
        input()
    finally:
        hotkey_mgr.stop()
        print("ปิด Hotkey Listener เรียบร้อย")


def main():
    print_banner()
    matrix = run_clipboard()

    while True:
        print("\nเมนูทดสอบ:")
        print("1. ทดสอบเสียง (Sound Notifier)")
        print("2. ทดสอบนับถอยหลัง 3 วินาทีแล้วเริ่มพิมพ์ (Countdown Typing)")
        print("3. ทดสอบปุ่มลัด F2 เพื่อเริ่มพิมพ์ และ ESC เพื่อหยุดฉุกเฉิน (Global Hotkey)")
        print("4. รีเฟรชข้อมูลจาก Clipboard")
        print("0. จบการทดสอบ")
        choice = input("เลือกเมนู (0-4): ").strip()

        if choice == "1":
            run_sounds()
        elif choice == "2":
            run_countdown_typing(matrix)
        elif choice == "3":
            run_hotkey_typing(matrix)
        elif choice == "4":
            matrix = run_clipboard()
        elif choice == "0":
            print("สิ้นสุดการทดสอบ Phase 1 ขอบคุณครับ!")
            break
        else:
            print("กรุณาเลือก 0-4")


if __name__ == "__main__":
    main()
