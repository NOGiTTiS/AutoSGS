# AutoSGS: ระบบช่วยพิมพ์คะแนนอัตโนมัติจาก Clipboard

<p align="center">
  <img src="assets/icon.png" width="128" height="128" alt="AutoSGS Icon">
  <br>
  <b>เครื่องมือช่วยอำนวยความสะดวกสำหรับครูผู้สอนในการบันทึกคะแนนในระบบ SGS (Secondary Grading System)</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20macOS-brightgreen.svg" alt="Platform">
  <img src="https://img.shields.io/badge/Tests-27%2F27%20Passed-success.svg" alt="Tests">
  <img src="https://img.shields.io/badge/License-MIT-orange.svg" alt="License">
</p>

<p align="center">
  <a href="https://github.com/NOGiTTiS/AutoSGS/releases/latest">
    <img src="https://img.shields.io/badge/Download-AutoSGS%20Latest%20Release-2ea44f?style=for-the-badge&logo=github&logoColor=white" alt="Download AutoSGS">
  </a>
</p>

### 📥 ดาวน์โหลดโปรแกรมพร้อมใช้งาน (Latest Release)

| ระบบปฏิบัติการ | ไฟล์ดาวน์โหลด | รูปแบบ | คำแนะนำการใช้งาน |
| :--- | :--- | :--- | :--- |
| **Windows 10 / 11** | [📥 **AutoSGS.exe**](https://github.com/NOGiTTiS/AutoSGS/releases/latest) | Standalone Portable (.exe) | ดับเบิลคลิกเปิดใช้งานได้ทันที ไม่ต้องติดตั้ง |
| **macOS** | [📥 **AutoSGS-macOS.zip**](https://github.com/NOGiTTiS/AutoSGS/releases/latest) | App Bundle (.zip) | แตกไฟล์ ย้ายเข้า Applications และเปิดสิทธิ์ Accessibility |

---

## 💡 จุดเด่นของ AutoSGS (Key Features)

- ⚡ **Auto-Sync Clipboard:** คัดลอก (Ctrl+C) จาก Excel/Google Sheets ข้อมูลจะซิงค์เข้าโปรแกรมทันที ไม่ต้องกดรีเฟรชเอง
- 🎯 **3 โหมดการกรอกตรงตามระบบ SGS:**
  1. **ผลการเรียน:** คะแนนรายวิชาทั่วไป (พิมพ์ + Tab ทุกช่อง)
  2. **คุณลักษณะอันพึงประสงค์:** 8 ช่อง (พิมพ์+Tab) + **กด Tab เพิ่มอีก 4 ครั้งท้ายแถว** ข้ามไปคนถัดไปทันที
  3. **การอ่าน คิดวิเคราะห์และเขียน:** 5 ช่อง (พิมพ์+Tab) + **กด Tab เพิ่มอีก 3 ครั้งท้ายแถว** ข้ามไปคนถัดไปทันที
- ⚡ **ความเร็วแยกอิสระตามโหมด (Per-Mode Speed):**
  - โหมดผลการเรียน: ค่าเริ่มต้น `0.10s` (ปลอดภัย มีเสถียรภาพ)
  - โหมดคุณลักษณะฯ & การอ่านฯ: ค่าเริ่มต้น `0.02s ⚡` (ความเร็วสูงสุด Turbo เหมาะกับการบันทึกครั้งเดียวท้ายฟอร์ม)
  - สามารถปรับ Slider แยกอิสระตามโหมด และระบบจดจำความเร็วแยกกันอัตโนมัติ
- 💾 **ระบบเตือนกดบันทึกใน SGS:** แสดงแถบเตือนสีส้มเด่นชัดหลังพิมพ์ครบในโหมดประเมิน ป้องกันการลืมกดบันทึก
- 📑 **รองรับทั้ง 1 คอลัมน์ หรือหลายคอลัมน์:** พิมพ์เรียงตามแนวนอนทีละคน ($Row_i, Col_1 \rightarrow Col_2 \dots \rightarrow Col_n$) อย่างถูกต้อง
- ⏩ **ข้ามช่องว่างอัตโนมัติ:** ช่องคะแนนที่ว่าง (เด็กขาด/ยังไม่มีคะแนน) โปรแกรมจะส่งเฉพาะ `Tab` ข้ามไปอย่างแม่นยำ
- 🎯 **Dual Trigger:** สั่งเริ่มพิมพ์ได้ 2 ช่องทาง: ปุ่มลัด Global Hotkey (`F2`) หรือปุ่มเริ่มแบบนับถอยหลัง 3 วินาที
- 🛑 **Emergency Stop (Kill Switch):** กดปุ่ม `ESC` หยุดพิมพ์ทันทีในระดับมิลลิวินาที ($< 50$ms)
- 🖥 **Modern UI & Prompt Font:** ดีไซน์โมเดิร์นด้วย CustomTkinter พร้อมใช้ฟอนต์ **Prompt** สวยงาม คมชัด สบายตา
- 🔎 **ปรับขนาดตัวอักษรได้:** เลือกขนาดการแสดงผลได้ 3 ระดับ (ปกติ 100%, ใหญ่ 115%, ใหญ่พิเศษ 130%)
- 📦 **Portable Standalone:** คลิกเปิดใช้งานได้ทันที ไม่ต้องติดตั้งโปรแกรมหรือ Python

---

## 📖 คู่มือการใช้งาน (Documentation)

- 📘 **[คู่มือการใช้งานสำหรับคุณครู (Markdown User Guide)](docs/user_guide.md)**
- 📕 **[ดาวน์โหลดคู่มือการใช้งานฉบับสมบูรณ์ (PDF Manual)](docs/AutoSGS_User_Manual.pdf)**
- 📊 **[ดาวน์โหลดสไลด์นำเสนออบรมการใช้งาน (PowerPoint PPTX Presentation)](docs/AutoSGS_User_Manual.pptx)**
- 🔨 **[คู่มือขั้นตอนการ Build และคอมไพล์โปรแกรม (Build Guide)](docs/build_guide.md)**
- 📋 **[เอกสารข้อกำหนดของระบบ (System Specification)](docs/spec.md)**
- 📐 **[แผนการนำไปปฏิบัติและสถาปัตยกรรม (Implementation Plan)](docs/plan.md)**
- 🧠 **[Project Brain & Context (gemini.md)](gemini.md)**

---

## 🛠 สำหรับนักพัฒนา (Developer Guide)

### 1. ติดตั้ง Dependencies
```bash
git clone https://github.com/NOGiTTiS/AutoSGS.git
cd AutoSGS
pip install -r requirements.txt
```

### 2. รันแอปพลิเคชัน
```bash
python main.py
```

### 3. รันการทดสอบ (Automated Tests)
```bash
pytest -v
```

### 4. บิลด์ไฟล์พกพา (Build Standalone Executable)
- **Windows:** รัน `packaging\build_windows.bat` $\rightarrow$ ได้ไฟล์ `dist\AutoSGS.exe`
- **macOS:** รัน `./packaging/build_mac.sh` $\rightarrow$ ได้ไฟล์ `dist/AutoSGS.app`

---

## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.
