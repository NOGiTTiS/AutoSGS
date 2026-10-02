"""
Build high quality PDF User Manual for AutoSGS using Playwright (Edge Chromium).
Features Prompt font, cover page, table of contents, diagrams, screenshots,
page numbers, callout blocks, and styling.
"""

import base64
from pathlib import Path
from playwright.sync_api import sync_playwright

DOCS_DIR = Path("docs")
IMAGES_DIR = DOCS_DIR / "images"
ASSETS_DIR = Path("assets")
OUTPUT_PDF = DOCS_DIR / "AutoSGS_User_Manual.pdf"

def get_base64_image(image_path: Path) -> str:
    if not image_path.exists():
        return ""
    mime = "image/png" if image_path.suffix == ".png" else "image/jpeg"
    with open(image_path, "rb") as f:
        data = base64.b64encode(f.read()).decode("utf-8")
    return f"data:{mime};base64,{data}"

def build_pdf():
    # Pre-encode images to base64 so HTML can load them without local CORS issues
    icon_b64 = get_base64_image(ASSETS_DIR / "icon.png")
    quick_steps_b64 = get_base64_image(IMAGES_DIR / "quick_steps_infographic.png")
    app_main_b64 = get_base64_image(IMAGES_DIR / "autosgs_main_ready.png")
    app_preview_b64 = get_base64_image(IMAGES_DIR / "autosgs_preview_open.png")
    app_reminder_b64 = get_base64_image(IMAGES_DIR / "autosgs_save_reminder.png")
    excel_guide_b64 = get_base64_image(IMAGES_DIR / "excel_copy_guide.png")
    settings_b64 = get_base64_image(IMAGES_DIR / "autosgs_settings.png")
    sgs_mode1_b64 = get_base64_image(IMAGES_DIR / "sgs_mode1_guide.png")
    sgs_mode2_b64 = get_base64_image(IMAGES_DIR / "sgs_mode2_guide.png")
    sgs_mode3_b64 = get_base64_image(IMAGES_DIR / "sgs_mode3_guide.png")

    html_content = f"""<!DOCTYPE html>
<html lang="th">
<head>
  <meta charset="UTF-8">
  <title>คู่มือการใช้งาน AutoSGS</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Prompt:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  <style>
    @page {{
      size: A4;
      margin: 16mm 14mm 16mm 14mm;
      @bottom-right {{
        content: counter(page);
        font-family: 'Prompt', sans-serif;
        font-size: 10pt;
        color: #94a3b8;
      }}
    }}
    
    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}
    
    body {{
      font-family: 'Prompt', 'Segoe UI', Tahoma, sans-serif;
      font-size: 11pt;
      line-height: 1.6;
      color: #1e293b;
      background: #ffffff;
    }}

    .page-break {{
      page-break-before: always;
    }}

    /* Cover Page */
    .cover-page {{
      height: 100vh;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      text-align: center;
      padding: 40px;
      page-break-after: always;
      background: linear-gradient(135deg, #f8fafc 0%, #e0f2fe 100%);
      border-radius: 20px;
      border: 1px solid #bae6fd;
    }}
    
    .cover-icon {{
      width: 140px;
      height: 140px;
      margin-bottom: 24px;
      filter: drop-shadow(0 10px 20px rgba(37,99,235,0.2));
    }}
    
    .cover-title {{
      font-size: 32pt;
      font-weight: 700;
      color: #1e3a8a;
      margin-bottom: 8px;
    }}
    
    .cover-subtitle {{
      font-size: 16pt;
      font-weight: 500;
      color: #0369a1;
      margin-bottom: 20px;
    }}
    
    .cover-tagline {{
      font-size: 12pt;
      color: #475569;
      max-width: 600px;
      margin-bottom: 40px;
      line-height: 1.7;
    }}
    
    .cover-meta {{
      background: white;
      padding: 16px 30px;
      border-radius: 12px;
      box-shadow: 0 4px 15px rgba(0,0,0,0.05);
      border: 1px solid #cbd5e1;
      font-size: 11pt;
      color: #334155;
    }}
    
    /* Header Styles */
    h1 {{
      font-size: 20pt;
      font-weight: 700;
      color: #1e3a8a;
      border-bottom: 2px solid #2563eb;
      padding-bottom: 8px;
      margin-top: 24px;
      margin-bottom: 14px;
      page-break-after: avoid;
    }}
    
    h2 {{
      font-size: 15pt;
      font-weight: 600;
      color: #0369a1;
      margin-top: 18px;
      margin-bottom: 10px;
      page-break-after: avoid;
    }}
    
    h3 {{
      font-size: 13pt;
      font-weight: 600;
      color: #0f172a;
      margin-top: 14px;
      margin-bottom: 8px;
      page-break-after: avoid;
    }}
    
    p {{
      margin-bottom: 10px;
      text-align: justify;
    }}
    
    /* Tables */
    table {{
      width: 100%;
      border-collapse: collapse;
      margin: 14px 0;
      font-size: 10pt;
      page-break-inside: avoid;
    }}
    
    th, td {{
      border: 1px solid #cbd5e1;
      padding: 8px 10px;
      text-align: left;
    }}
    
    th {{
      background-color: #f1f5f9;
      color: #1e293b;
      font-weight: 600;
    }}
    
    tr:nth-child(even) td {{
      background-color: #f8fafc;
    }}
    
    /* Callout Boxes */
    .callout {{
      border-radius: 8px;
      padding: 12px 16px;
      margin: 14px 0;
      font-size: 10.5pt;
      page-break-inside: avoid;
    }}
    
    .callout-info {{
      background-color: #eff6ff;
      border-left: 4px solid #3b82f6;
      color: #1e40af;
    }}
    
    .callout-warning {{
      background-color: #fffbeb;
      border-left: 4px solid #f59e0b;
      color: #92400e;
    }}
    
    .callout-danger {{
      background-color: #fef2f2;
      border-left: 4px solid #ef4444;
      color: #991b1b;
    }}

    .callout-success {{
      background-color: #f0fdf4;
      border-left: 4px solid #10b981;
      color: #065f46;
    }}

    /* Images and Diagrams */
    .img-container {{
      text-align: center;
      margin: 16px 0;
      page-break-inside: avoid;
    }}

    .img-container img {{
      max-width: 100%;
      height: auto;
      border-radius: 8px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.08);
      border: 1px solid #e2e8f0;
    }}

    .img-caption {{
      font-size: 9.5pt;
      color: #64748b;
      margin-top: 6px;
      font-style: italic;
    }}

    .grid-2 {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 14px;
      page-break-inside: avoid;
    }}

    /* Key Tag */
    kbd {{
      background: #f1f5f9;
      border: 1px solid #cbd5e1;
      border-radius: 4px;
      padding: 2px 6px;
      font-family: inherit;
      font-size: 9.5pt;
      font-weight: 600;
      color: #0f172a;
      box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }}

    /* Numbered Steps */
    .step-list {{
      list-style: none;
      counter-reset: step-counter;
      margin: 12px 0;
    }}
    
    .step-list li {{
      counter-increment: step-counter;
      position: relative;
      padding-left: 42px;
      margin-bottom: 12px;
    }}

    .step-list li::before {{
      content: counter(step-counter);
      position: absolute;
      left: 0;
      top: 0;
      width: 28px;
      height: 28px;
      background: #2563eb;
      color: white;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 700;
      font-size: 11pt;
    }}
  </style>
</head>
<body>

  <!-- COVER PAGE -->
  <div class="cover-page">
    <img src="{icon_b64}" class="cover-icon" alt="AutoSGS Logo">
    <div class="cover-title">AutoSGS v1.0</div>
    <div class="cover-subtitle">คู่มือการใช้งานระบบช่วยพิมพ์คะแนนอัตโนมัติ (User Manual)</div>
    <div class="cover-tagline">
      เครื่องมือช่วยอำนวยความสะดวกสำหรับครูผู้สอนในการบันทึกคะแนนในระบบ SGS (Secondary Grading System)
      ลดภาระงาน เพิ่มความเร็ว ปลอดภัย และแม่นยำ 100%
    </div>
    <div class="cover-meta">
      <b>จัดทำโดย:</b> NOGiTTiS & ทีมพัฒนา AutoSGS<br>
      <b>รองรับ:</b> Windows 10/11 & macOS | <b>รูปแบบ:</b> Portable Application (.exe)
    </div>
  </div>

  <!-- SECTION 1: OVERVIEW -->
  <h1>1. ภาพรวมและประโยชน์ของโปรแกรม (Overview)</h1>
  <p>
    ในทุกสิ้นภาคเรียน ครูผู้สอนต้องคัดลอกคะแนนสอบและผลการประเมินจาก Microsoft Excel หรือ Google Sheets 
    มานั่งพิมพ์ลงหน้าเว็บระบบ SGS (Secondary Grading System) ของ สพฐ. ทีละช่องด้วยมือ นักเรียนห้องละ 40–50 คน หลายห้องเรียน 
    ทำให้ต้องเคาะแป้นพิมพ์ตัวเลขและกดปุ่ม Tab นับหลายพันครั้ง เกิดอาการเมื่อยล้าข้อมือ และเสี่ยงต่อการพิมพ์คะแนนผิดช่องหรือตกหล่น
  </p>

  <p>
    <b>AutoSGS</b> ถูกพัฒนาขึ้นเป็น Desktop Utility ขนาดพกพา (Portable) ช่วยอ่านคะแนนที่คุณครู Copy ไว้ใน Clipboard 
    แล้วจำลองการพิมพ์และกด Tab เลื่อนช่องให้อัตโนมัติอย่างรวดเร็ว ปลอดภัย และแม่นยำ พร้อมระบบข้ามช่องสรุปผลให้อัตโนมัติ
  </p>

  <div class="img-container">
    <img src="{quick_steps_b64}" alt="4 Quick Steps">
    <div class="img-caption">รูปที่ 1: ขั้นตอนการทำงาน 4 ขั้นตอนง่าย ๆ ของ AutoSGS</div>
  </div>

  <div class="callout callout-info">
    <b>💡 จุดเด่นสำคัญ:</b> ไม่ต้องติดตั้งโปรแกรม, ไม่ต้องมีความรู้ด้านไอทีหรือการเขียนโปรแกรม, รองรับภาษาไทยสมบูรณ์, 
    และมีระบบตัดการทำงานฉุกเฉิน (Kill Switch) ภายในไม่ถึง 0.05 วินาที
  </div>

  <!-- SECTION 2: UI ANATOMY -->
  <div class="page-break"></div>
  <h1>2. โครงสร้างหน้าต่างและส่วนประกอบ (UI Layout)</h1>
  <p>หน้าต่าง AutoSGS ออกแบบให้มีขนาดกะทัดรัด พร้อมสวิตช์ <b>"อยู่บนสุด" (Always on Top)</b> เพื่อให้ครูมองเห็นสถานะและปุ่มควบคุมตลอดเวลา:</p>

  <div class="img-container">
    <img src="{app_main_b64}" style="max-width: 520px;" alt="AutoSGS Main UI">
    <div class="img-caption">รูปที่ 2: หน้าต่างหลัก AutoSGS ในโหมดพร้อมทำงาน (Ready State)</div>
  </div>

  <table>
    <thead>
      <tr>
        <th style="width: 25%;">ส่วนประกอบ</th>
        <th>หน้าที่และการทำงาน</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><b>1. สวิตช์ "อยู่บนสุด"</b></td>
        <td>ให้หน้าต่าง AutoSGS ลอยอยู่เหนือหน้าเว็บเบราว์เซอร์เสมอ ไม่ต้องคอยกดสลับหน้าจอไปมา</td>
      </tr>
      <tr>
        <td><b>2. แถบเลือก 3 โหมด</b></td>
        <td>เลือกให้ตรงกับหน้างาน SGS: 📊 ผลการเรียน, ⭐ คุณลักษณะฯ (8 ช่อง), 📖 การอ่านฯ (6 ช่อง)</td>
      </tr>
      <tr>
        <td><b>3. กล่องสถานะ & แถบสี</b></td>
        <td>แสดงสถานะเรียลไทม์ พร้อมตรวจนับจำนวนแถวและคอลัมน์จากคลิปบอร์ดให้อัตโนมัติ</td>
      </tr>
      <tr>
        <td><b>4. แถบ Progress Bar</b></td>
        <td>แสดงความคืบหน้าการพิมพ์ตัวเลขแบบเรียลไทม์ตั้งแต่ 0% จนถึง 100%</td>
      </tr>
      <tr>
        <td><b>5. ปุ่มเริ่มพิมพ์ / ปุ่มหยุด</b></td>
        <td>ปุ่มสีน้ำเงินสำหรับเริ่มพิมพ์แบบนับถอยหลัง 3 วินาที หรือกลายเป็นปุ่มสีแดง <b>"⏹ หยุดฉุกเฉิน (ESC)"</b> ขณะพิมพ์</td>
      </tr>
      <tr>
        <td><b>6. แถบ Slider ปรับสปีด</b></td>
        <td>ปรับเวลาหน่วงเคาะแป้นพิมพ์ (0.01s - 0.50s) โดยระบบจะจำค่าความเร็วแยกแต่ละโหมดให้อัตโนมัติ</td>
      </tr>
      <tr>
        <td><b>7. ปุ่ม Preview ข้อมูล</b></td>
        <td>คลิกเพื่อคลี่ดูตารางคะแนนที่ตรวจพบในคลิปบอร์ด เพื่อตรวจสอบความถูกต้องก่อนสั่งพิมพ์จริง</td>
      </tr>
    </tbody>
  </table>

  <!-- SECTION 3: THE 3 MODES -->
  <div class="page-break"></div>
  <h1>3. เจาะลึก 3 โหมดการทำงาน (Grading Modes)</h1>
  <p>ระบบ SGS มีลักษณะตารางคะแนนที่แตกต่างกันในแต่ละหน้า AutoSGS จึงสร้างตรรกะการกดปุ่มให้สัมพันธ์กับหน้าเว็บ SGS โดยเฉพาะ:</p>

  <h2>3.1 โหมดผลการเรียน (Academic Scores)</h2>
  <p>
    ใช้สำหรับกรอกคะแนนเก็บย่อย, คะแนนกลางภาค, ปลายภาค หรือผลการเรียนรายวิชาทั่วไป ทุกช่องจะพิมพ์ <code>คะแนน + Tab 1 ครั้ง</code> 
    เลื่อนไปคนถัดไปทันที รองรับจำนวนคอลัมน์กี่ช่องก็ได้ (1 ถึง N ช่อง)
  </p>
  <div class="img-container">
    <img src="{sgs_mode1_b64}" alt="SGS Mode 1 Form">
    <div class="img-caption">รูปที่ 3: หน้าจอระบบ SGS โหมดผลการเรียนรายวิชาทั่วไป</div>
  </div>

  <h2>3.2 โหมดคุณลักษณะอันพึงประสงค์ (8 ตัวชี้วัด)</h2>
  <p>
    ใช้สำหรับหน้าประเมินคุณลักษณะ 8 ประการ (คะแนน 0–3) ในระบบ SGS แต่ละแถวจะมี 8 ช่องคะแนน 
    จากนั้นจะมีช่องสรุปผลรวม/ฐานนิยม/ผลประเมิน/ปุ่มแก้ไข รวมเป็น <b>4 ช่องที่ถูกล็อก</b> 
    AutoSGS จึงสั่งพิมพ์ 8 ช่องแรก <b>แล้วกด <kbd>Tab</kbd> เพิ่มพิเศษอีก 4 ครั้งท้ายแถว</b> เพื่อข้ามไปยังข้อ 1 ของนักเรียนคนถัดไปพอดี!
  </p>
  <div class="img-container">
    <img src="{sgs_mode2_b64}" alt="SGS Mode 2 Form">
    <div class="img-caption">รูปที่ 4: หน้าจอ SGS โหมดคุณลักษณะอันพึงประสงค์ (8 ช่อง + ข้าม 4 Tab ท้ายแถว)</div>
  </div>

  <h2>3.3 โหมดการอ่าน คิดวิเคราะห์และเขียน (6 ตัวชี้วัด)</h2>
  <p>
    ใช้สำหรับหน้าประเมินการอ่าน คิดวิเคราะห์และเขียน (คะแนน 0–3) มี 6 ช่องคะแนน และมีช่องสรุปผล <b>2 ช่องที่ล็อกไว้</b> 
    AutoSGS จึงสั่งพิมพ์ 6 ช่องแรก <b>แล้วกด <kbd>Tab</kbd> เพิ่มพิเศษอีก 2 ครั้งท้ายแถว</b> เพื่อข้ามไปยังข้อ 1 ของนักเรียนคนถัดไป
  </p>
  <div class="img-container">
    <img src="{sgs_mode3_b64}" alt="SGS Mode 3 Form">
    <div class="img-caption">รูปที่ 5: หน้าจอ SGS โหมดการอ่าน คิดวิเคราะห์และเขียน (6 ช่อง + ข้าม 2 Tab ท้ายแถว)</div>
  </div>

  <!-- SECTION 4: STEP BY STEP GUIDE -->
  <div class="page-break"></div>
  <h1>4. ขั้นตอนการใช้งานจริงแบบ Step-by-Step</h1>

  <h3>ขั้นตอนที่ 1: เตรียมข้อมูลและคัดลอกจาก Excel</h3>
  <p>
    เปิดไฟล์ Excel หรือ Google Sheets แล้วลากเมาส์คลุม <b>เฉพาะตัวเลขคะแนน</b> 
    <span style="color:#ef4444; font-weight:700;">⚠️ ห้ามคลุมหัวตาราง และห้ามคลุมเลขที่หรือชื่อนักเรียน</span> 
    จากนั้นกด <kbd>Ctrl + C</kbd>
  </p>

  <div class="img-container">
    <img src="{excel_guide_b64}" alt="Excel Selection Guide">
    <div class="img-caption">รูปที่ 6: วิธีการลากเมาส์คลุมเฉพาะช่วงคะแนนใน Excel อย่างถูกต้อง</div>
  </div>

  <h3>ขั้นตอนที่ 2: ตรวจสอบข้อมูลใน AutoSGS</h3>
  <p>
    เมื่อคัดลอกแล้ว สลับมาดูที่ AutoSGS โปรแกรมจะตรวจจับคลิปบอร์ดให้อัตโนมัติทันที 
    ครูสามารถคลิกปุ่ม <b>"▼ ดูตัวอย่างข้อมูลในคลิปบอร์ด (Preview)"</b> เพื่อดูตารางคะแนนว่าจำนวนคนและตัวเลขถูกต้องหรือไม่
  </p>

  <div class="img-container">
    <img src="{app_preview_b64}" style="max-width: 540px;" alt="AutoSGS Preview">
    <div class="img-caption">รูปที่ 7: การเปิดแผงพรีวิวตรวจสอบตารางคะแนนจริงก่อนเริ่มพิมพ์</div>
  </div>

  <div class="page-break"></div>
  <h3>ขั้นตอนที่ 3: สั่งพิมพ์คะแนนลงหน้าเว็บ SGS</h3>
  <ol class="step-list">
    <li>
      <b>วิธีที่ 1 (แนะนำ - สะดวกและเร็วที่สุด):</b> สลับไปที่หน้าเว็บเบราว์เซอร์ระบบ SGS $\rightarrow$ 
      คลิกเมาส์ที่ช่องคะแนนแรกของ <b>นักเรียนเลขที่ 1</b> $\rightarrow$ กดปุ่ม <kbd>F2</kbd> บนคีย์บอร์ด $\rightarrow$ ปล่อยมือ นั่งรอโปรแกรมพิมพ์ให้จนครบ
    </li>
    <li>
      <b>วิธีที่ 2 (นับถอยหลัง):</b> คลิกปุ่มสีน้ำเงิน <b>"▶ เริ่มพิมพ์ (3s)"</b> ในโปรแกรม AutoSGS $\rightarrow$ 
      ฟังเสียง Beep นับถอยหลัง (3.. 2.. 1..) พร้อมรีบสลับหน้าจอไปคลิกช่องแรกในเว็บ SGS $\rightarrow$ เมื่อนับครบ โปรแกรมจะเริ่มพิมพ์ทันที
    </li>
  </ol>

  <h3>ขั้นตอนที่ 4: การแจ้งเตือนและกดบันทึกใน SGS</h3>
  <p>
    เมื่อพิมพ์เสร็จสิ้นครบทุกแถว จะมีเสียงกระดิ่ง (Chime) ดังขึ้น 2 ครั้ง และในโหมดคุณลักษณะฯ หรือโหมดการอ่านฯ 
    จะมีแถบเตือนสีส้มเด่นชัดปรากฏขึ้นมา:
  </p>

  <div class="img-container">
    <img src="{app_reminder_b64}" style="max-width: 520px;" alt="Save Reminder Banner">
    <div class="img-caption">รูปที่ 8: แถบเตือนสีส้มแจ้งเตือนให้ครูกดปุ่ม "บันทึก" ในระบบ SGS เสมอ</div>
  </div>

  <div class="callout callout-warning">
    <b>💾 สำคัญมาก:</b> ระบบ SGS จะยังไม่บันทึกคะแนนลงฐานข้อมูลจนกว่าคุณครูจะเลื่อนลงมาคลิกปุ่ม <b>"บันทึก"</b> ที่หน้าเว็บ SGS ด้วยตนเองเสมอ!
  </div>

  <!-- SECTION 5: SAFETY AND SETTINGS -->
  <div class="page-break"></div>
  <h1>5. ระบบความปลอดภัย & การตั้งค่าโปรแกรม</h1>

  <h2>🛑 ปุ่มหยุดฉุกเฉิน (Instant Emergency Kill Switch)</h2>
  <p>
    หากครูคลิกผิดช่อง หรือต้องการยกเลิกการพิมพ์กะทันหัน สามารถกดปุ่ม <kbd>ESC</kbd> บนแป้นพิมพ์คีย์บอร์ดได้ทันที ทุกเวลา! 
    โปรแกรมจะหยุดพิมพ์ทันทีในระดับมิลลิวินาที (Latency &lt; 50 ms) ป้องกันไม่ให้คะแนนเลื่อนผิดช่อง
  </p>

  <h2>⏩ การจัดการช่องว่าง (Empty Cells)</h2>
  <p>
    หากใน Excel มีช่องว่าง (เด็กขาดสอบ / ลาออก / ติด ร.) โปรแกรม AutoSGS จะส่งเฉพาะคำสั่ง <kbd>Tab</kbd> เปล่า 
    ข้ามช่องนั้นไปโดยไม่แตะต้องตัวเลขเดิม ทำให้คะแนนของนักเรียนคนอื่นไม่เลื่อนผิดตำแหน่งแน่นอน
  </p>

  <h2>⚙️ เมนูการตั้งค่า (Settings Dialog)</h2>
  <p>คลิกที่ปุ่ม <b>"⚙️ ตั้งค่า"</b> มุมขวาบน เพื่อปรับแต่งตามความชอบ:</p>

  <div class="grid-2">
    <div>
      <div class="img-container">
        <img src="{settings_b64}" alt="Settings Dialog">
        <div class="img-caption">รูปที่ 9: หน้าต่างตั้งค่าโปรแกรม</div>
      </div>
    </div>
    <div style="font-size: 10pt;">
      <ul style="padding-left: 18px; margin-top: 10px;">
        <li style="margin-bottom: 8px;"><b>ปุ่มลัดเริ่มพิมพ์:</b> เปลี่ยนจาก F2 เป็น F4, F8 หรือ Ctrl+Alt+V ได้</li>
        <li style="margin-bottom: 8px;"><b>ขนาดตัวอักษร:</b> เลือกได้ 3 ขนาด (ปกติ 100%, ใหญ่ 115% แนะนำ, ใหญ่พิเศษ 130% สำหรับสายตาผู้ใหญ่)</li>
        <li style="margin-bottom: 8px;"><b>ธีมการแสดงผล:</b> System (ตามวินโดวส์), Dark Mode หรือ Light Mode</li>
        <li style="margin-bottom: 8px;"><b>เปิด/ปิดเสียง:</b> เลือกเปิดหรือปิดเสียง Beep นับถอยหลัง และเสียง Chime เสร็จสิ้น</li>
        <li style="margin-bottom: 8px;"><b>ความเร็ว Turbo ⚡:</b> ปรับลด Delay เป็น 0.02s ในโหมดประเมินเพื่อความรวดเร็วสูงสุด</li>
      </ul>
    </div>
  </div>

  <!-- SECTION 6: FAQS -->
  <div class="page-break"></div>
  <h1>6. คำถามที่พบบ่อย (FAQs & Troubleshooting)</h1>

  <div class="callout callout-info">
    <b>Q: เปิดโปรแกรมแล้วขึ้นเตือน "Windows protected your PC"?</b><br>
    <b>ตอบ:</b> เป็นการแจ้งเตือนปกติของระบบความปลอดภัย Windows สำหรับโปรแกรมขนาดเล็กที่ไม่มีใบรับรองดิจิทัลรายปี 
    ให้คลิกที่คำว่า <b>"More info" (ข้อมูลเพิ่มเติม)</b> แล้วคลิกปุ่ม <b>"Run anyway" (เรียกใช้ต่อไป)</b> โปรแกรมปลอดภัย 100%
  </div>

  <div class="callout callout-info">
    <b>Q: กดปุ่ม F2 บนโน้ตบุ๊กแล้วไม่มีอะไรเกิดขึ้น?</b><br>
    <b>ตอบ:</b> โน้ตบุ๊กหลายยี่ห้อ (Lenovo, Asus, Dell, HP) แถวปุ่มบนสุดจะถูกตั้งค่าเป็นปุ่มปรับแสง/ปรับเสียง 
    ให้ลองกด <kbd>Fn + F2</kbd> พร้อมกัน หรือเปิดหน้าต่าง <code>⚙️ ตั้งค่า</code> แล้วเปลี่ยนปุ่มลัดเป็นปุ่มอื่น
  </div>

  <div class="callout callout-info">
    <b>Q: ใช้งานบนเครื่อง Mac ได้หรือไม่?</b><br>
    <b>ตอบ:</b> ได้ครับ แต่เนื่องจาก macOS มีระบบความปลอดภัยสูง ต้องเปิดสิทธิ์ Accessibility ก่อน โดยไปที่ 
    <code>System Settings</code> $\rightarrow$ <code>Privacy & Security</code> $\rightarrow$ <code>Accessibility</code> 
    แล้วเปิดสวิตช์อนุญาตให้กับแอปพลิเคชัน <b>AutoSGS</b>
  </div>

  <div class="callout callout-info">
    <b>Q: ถ้าอินเทอร์เน็ตโรงเรียนช้า ควรตั้งค่าอย่างไร?</b><br>
    <b>ตอบ:</b> เลื่อนแถบสไลเดอร์ความเร็วในหน้าต่างหลักเพิ่มเวลาหน่วงเป็น <code>0.15</code> หรือ <code>0.20</code> วินาที 
    เพื่อให้เบราว์เซอร์รับคะแนนและประมวลผลได้ทันโดยไม่ตกหล่น
  </div>

  <div style="text-align: center; margin-top: 40px; color: #64748b; font-size: 10pt; border-top: 1px solid #cbd5e1; padding-top: 16px;">
    AutoSGS — มุ่งมั่นแบ่งเบาภาระงานครูไทย เพื่อเวลาการสอนที่มีคุณค่ายิ่งขึ้น<br>
    โครงการโอเพนซอร์ส ซอร์สโค้ด: https://github.com/NOGiTTiS/AutoSGS
  </div>

</body>
</html>
"""

    print("Generating PDF with Playwright (Edge)...")
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="msedge", headless=True)
        page = browser.new_page()
        page.set_content(html_content, wait_until="networkidle")
        page.pdf(
            path=str(OUTPUT_PDF),
            format="A4",
            print_background=True,
            margin={"top": "16mm", "bottom": "16mm", "left": "14mm", "right": "14mm"},
            display_header_footer=True,
            header_template='<div style="font-family:Prompt,sans-serif; font-size:8pt; color:#94a3b8; width:100%; text-align:right; padding-right:20px;">AutoSGS User Manual</div>',
            footer_template='<div style="font-family:Prompt,sans-serif; font-size:8pt; color:#94a3b8; width:100%; text-align:center;">หน้า <span class="pageNumber"></span> จาก <span class="totalPages"></span></div>'
        )
        browser.close()
    
    print(f"[DONE] Successfully generated PDF: {OUTPUT_PDF}")

if __name__ == "__main__":
    build_pdf()
