# คู่มือขั้นตอนการ Build และคอมไพล์โปรแกรม AutoSGS (Build Guide)

> **AutoSGS** — ระบบช่วยพิมพ์คะแนนอัตโนมัติจาก Clipboard สำหรับครูผู้สอนบันทึกคะแนนในระบบ SGS  
> เอกสารนี้อธิบายขั้นตอนการคอมไพล์ซอร์สโค้ดภาษา Python ให้กลายเป็นไฟล์พกพา (Standalone Executable) พร้อมใช้งานสำหรับ Windows (`.exe`) และ macOS (`.app`)

---

## 📋 1. ข้อกำหนดเบื้องต้นของสภาพแวดล้อม (Prerequisites)

ก่อนเริ่มทำการ Build โปรแกรม กรุณาตรวจสอบว่าระบบของคุณมีสิ่งต่อไปนี้:

1. **Python:** เวอร์ชัน **3.10** ขึ้นไป (ทดสอบและแนะนำบน Python 3.10 – 3.13)
2. **Dependencies ทั้งหมดของโปรเจกต์:** ติดตั้งผ่านคำสั่ง
   ```bash
   pip install -r requirements.txt
   ```
3. **PyInstaller:** เครื่องมือสร้างไฟล์ Executable (เวอร์ชัน 6.0 ขึ้นไป)
   ```bash
   pip install pyinstaller
   ```
4. **ไฟล์ทรัพยากร (Assets):** ต้องมีอยู่ในโฟลเดอร์ `assets/`
   - `assets/icon.ico` (ไอคอนสำหรับ Windows)
   - `assets/icon.png` (ไอคอนสำหรับ macOS / เอกสาร)
   - `assets/fonts/Prompt-Regular.ttf` และ `assets/fonts/Prompt-SemiBold.ttf` (ฟอนต์ Prompt)

---

## 🪟 2. การคอมไพล์และ Build บนระบบปฏิบัติการ Windows

### วิธีที่ 1: รันผ่านสคริปต์อัตโนมัติ (แนะนำ สะดวกที่สุด)
เปิด Terminal หรือ Command Prompt ในโฟลเดอร์โปรเจกต์ (`D:\TUNorth\apps\sgs`) แล้วรันคำสั่ง:

```cmd
packaging\build_windows.bat
```

> 💡 สคริปต์นี้จะล้างโฟลเดอร์ `build/` และ `dist/` เดิม, รันคำสั่งคอมไพล์ และทำสำเนาไฟล์ผลลัพธ์เป็นทั้ง `dist\TUNorth - AutoSGS.exe` และ `dist\AutoSGS.exe` ให้โดยอัตโนมัติ

---

### วิธีที่ 2: รันคำสั่ง PyInstaller ด้วยตนเอง (Manual Command)

คุณสามารถสั่งการผ่าน PowerShell หรือ Command Prompt ได้โดยตรง ดังนี้:

#### คำสั่งสำหรับ Command Prompt (cmd):
```cmd
pyinstaller --noconfirm --onefile --windowed ^
    --name="TUNorth - AutoSGS" ^
    --icon="assets/icon.ico" ^
    --add-data="assets/fonts;assets/fonts" ^
    --add-data="assets/icon.ico;assets" ^
    --collect-all="customtkinter" ^
    --hidden-import="pynput.keyboard._win32" ^
    --hidden-import="pynput.mouse._win32" ^
    main.py
```

#### คำสั่งสำหรับ PowerShell:
```powershell
pyinstaller --noconfirm --onefile --windowed `
    --name="TUNorth - AutoSGS" `
    --icon="assets/icon.ico" `
    --add-data="assets/fonts;assets/fonts" `
    --add-data="assets/icon.ico;assets" `
    --collect-all="customtkinter" `
    --hidden-import="pynput.keyboard._win32" `
    --hidden-import="pynput.mouse._win32" `
    main.py
```

---

### 🔍 คำอธิบายพารามิเตอร์ของ PyInstaller ใน Windows

| พารามิเตอร์ | ความหมายและเหตุผลที่ต้องใช้ |
| :--- | :--- |
| `--noconfirm` | เขียนทับไฟล์หรือโฟลเดอร์ผลลัพธ์เดิมทันทีโดยไม่ต้องหยุดถามยืนยัน |
| `--onefile` | รวมโค้ดและไลบรารีทั้งหมดให้เป็น **ไฟล์ `.exe` เดี่ยวไฟล์เดียว (Portable)** ดับเบิลคลิกใช้งานได้ทันที |
| `--windowed` | ซ่อนหน้าต่างจอดำ (Console Window) เปิดเฉพาะหน้าต่าง GUI ของโปรแกรม |
| `--name="..."` | กำหนดชื่อไฟล์ของ Executable ผลลัพธ์ |
| `--icon="..."` | กำหนดไฟล์รูปไอคอนของโปรแกรม (`.ico`) |
| `--add-data="assets/fonts;assets/fonts"` | ผนึกโฟลเดอร์ฟอนต์ `Prompt` เข้าไปในตัว `.exe` (บน Windows ใช้เครื่องหมาย `;` คั่น) |
| `--add-data="assets/icon.ico;assets"` | ผนึกไฟล์ไอคอนไว้ใช้สำหรับ Window Title Bar |
| `--collect-all="customtkinter"` | รวบรวมทรัพยากรทั้งหมดของ `customtkinter` (รวมถึงไฟล์ ธีมสี `.json` และไอคอนภายใน) |
| `--hidden-import="pynput.keyboard._win32"` | นำเข้า Backend ของคีย์บอร์ดบน Windows ให้สมบูรณ์ ป้องกันปัญหากด Hotkey ไม่ติด |
| `--hidden-import="pynput.mouse._win32"` | นำเข้า Backend ของเมาส์บน Windows |

---

## 🍎 3. การคอมไพล์และ Build บนระบบปฏิบัติการ macOS

### วิธีที่ 1: รันผ่านเชลล์สคริปต์
เปิด Terminal บน macOS ในโฟลเดอร์โปรเจกต์ แล้วรันคำสั่ง:

```bash
chmod +x packaging/build_mac.sh
./packaging/build_mac.sh
```

### วิธีที่ 2: รันคำสั่ง PyInstaller บน Terminal (macOS)
```bash
pyinstaller --noconfirm --onedir --windowed \
    --name="AutoSGS" \
    --icon="assets/icon.icns" \
    --add-data="assets/fonts:assets/fonts" \
    --collect-all="customtkinter" \
    --hidden-import="pynput.keyboard._darwin" \
    --hidden-import="pynput.mouse._darwin" \
    main.py
```

> ⚠️ **ข้อแตกต่างสำคัญบน macOS:**
> - พารามิเตอร์ `--add-data` บน macOS / Linux จะใช้เครื่องหมายโคลอน (`:`) คั่นระหว่างโฟลเดอร์ต้นทางและปลายทาง (ต่างจาก Windows ที่ใช้ `;`)
> - บน macOS แนะนำให้ใช้ `--onedir` เพื่อให้ได้ Bundle `.app` ที่ถูกต้องตามมาตรฐานระบบความปลอดภัยของ Apple
> - สคริปต์จะทำการบีบอัดเป็น `dist/AutoSGS-macOS.zip` พร้อมสำหรับการแจกจ่าย

---

## 🛠 4. การแก้ไขปัญหาที่พบบ่อยขณะ Build (Troubleshooting)

### ปัญหาที่ 1: `PermissionError: [WinError 5] Access is denied`
```text
PermissionError: [WinError 5] Access is denied: '...dist\\TUNorth - AutoSGS.exe'
```
- **สาเหตุ:** มีโปรแกรม AutoSGS กำลังเปิดใช้งานหรือรันค้างอยู่ในหน่วยความจำ ทำให้ Windows ล็อกไฟล์ไว้ไม่ยอมให้ลบหรือเขียนทับ
- **วิธีแก้ไข:** สั่งปิดโปรแกรมที่ค้างอยู่ผ่าน PowerShell ก่อนเริ่ม Build:
  ```powershell
  Stop-Process -Name "TUNorth - AutoSGS" -Force -ErrorAction SilentlyContinue
  Stop-Process -Name "AutoSGS" -Force -ErrorAction SilentlyContinue
  ```
  จากนั้นจึงรันคำสั่ง Build ใหม่อีกครั้ง

---

### ปัญหาที่ 2: ฟอนต์ Prompt ไม่แสดง หรือหน้าต่างแจ้งเตือนฟอนต์หาย
- **สาเหตุ:** ลืมใส่พารามิเตอร์ `--add-data="assets/fonts;assets/fonts"`
- **วิธีแก้ไข:** ตรวจสอบว่าในโฟลเดอร์ `assets/fonts/` มีไฟล์ `.ttf` ครบถ้วน และใช้คำสั่ง Build ที่มี `--add-data` ครบตามตัวอย่าง

---

### ปัญหาที่ 3: หน้าต่างโปรแกรมไม่ขึ้น หรือแจ้งข้อผิดพลาด CustomTkinter Theme
- **สาเหตุ:** PyInstaller ไม่ได้นำเข้าไฟล์ธีมสี `.json` ของ CustomTkinter
- **วิธีแก้ไข:** ต้องใส่พารามิเตอร์ `--collect-all="customtkinter"` เสมอ ห้ามตัดออก

---

### ปัญหาที่ 4: Windows SmartScreen / Defender แจ้งเตือน "Windows protected your PC"
- **สาเหตุ:** เป็นพฤติกรรมปกติของระบบปฏิบัติการ Windows สำหรับไฟล์ `.exe` ที่สร้างขึ้นเองและยังไม่ได้ซื้อใบรับรอง Digital Signature รายปี
- **วิธีแก้ไข:**
  1. คลิกที่ข้อความ **"More info" (ข้อมูลเพิ่มเติม)**
  2. คลิกปุ่ม **"Run anyway" (เรียกใช้ต่อไป)**
  3. โปรแกรมจะเปิดขึ้นมาทำงานตามปกติ

---

## ✅ 5. ขั้นตอนตรวจสอบความถูกต้องหลัง Build (Post-Build Verification)

เมื่อคำสั่งเสร็จสิ้น ให้ตรวจสอบไฟล์ผลลัพธ์ตามขั้นตอนดังนี้:

1. **ตรวจสอบตำแหน่งไฟล์:**
   - ตรวจสอบว่ามีไฟล์ `dist\TUNorth - AutoSGS.exe` (หรือ `dist\AutoSGS.exe`) เกิดขึ้นจริง
   - ขนาดไฟล์ปกติจะอยู่ที่ประมาณ **18–20 MB** (เนื่องจากรวม Python Runtime และไลบรารีทั้งหมดไว้ในตัว)
2. **เปิดทดสอบการทำงาน:**
   - ดับเบิลคลิกเปิดไฟล์ `.exe`
   - ตรวจสอบว่าหน้าต่าง UI เปิดขึ้นมาได้อย่างรวดเร็ว ไม่แสดงหน้าต่างคอนโซลสีดำ
   - ฟอนต์ภาษาไทย **Prompt** แสดงผลคมชัดสวยงาม
   - ลองคลิกสลับโหมด 3 โหมด (ผลการเรียน, คุณลักษณะฯ, การอ่านฯ) และสังเกตการเปลี่ยนสลับค่าความเร็ว
3. **รัน Automated Tests ควบคู่:**
   ```bash
   pytest -v
   ```
   (ชุดการทดสอบทั้งหมด 27 รายการควรผ่าน 100%)
