"""
Script to generate high-resolution illustrations and screenshots for AutoSGS User Manual.
Uses Playwright with Edge to render pixel-perfect UI mockups with Prompt font.
"""

from pathlib import Path
from playwright.sync_api import sync_playwright

OUTPUT_DIR = Path("docs/images")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Common HTML template with Prompt font
HTML_WRAPPER = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Prompt:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: 'Prompt', -apple-system, BlinkMacSystemFont, sans-serif;
      background: transparent;
      display: flex;
      justify-content: center;
      align-items: center;
      padding: 30px;
    }
    {custom_css}
  </style>
</head>
<body>
  {content}
</body>
</html>
"""

def generate_assets():
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="msedge", headless=True)
        context = browser.new_context(device_scale_factor=2)
        page = context.new_page()

        # -------------------------------------------------------------
        # 1. Quick Steps Infographic (4-Step Banner)
        # -------------------------------------------------------------
        steps_css = """
        .card-container {
          background: #ffffff;
          border-radius: 16px;
          padding: 24px 30px;
          box-shadow: 0 10px 30px rgba(0,0,0,0.08);
          border: 1px solid #e2e8f0;
          max-width: 960px;
          width: 100%;
        }
        .header {
          text-align: center;
          margin-bottom: 24px;
        }
        .header h2 {
          color: #1e3a8a;
          font-size: 24px;
          font-weight: 700;
        }
        .header p {
          color: #64748b;
          font-size: 14px;
        }
        .steps-grid {
          display: grid;
          grid-template-columns: repeat(4, 1fr);
          gap: 16px;
          position: relative;
        }
        .step-box {
          background: #f8fafc;
          border: 2px solid #e2e8f0;
          border-radius: 12px;
          padding: 20px 16px;
          text-align: center;
          position: relative;
          transition: all 0.2s;
        }
        .step-badge {
          width: 36px;
          height: 36px;
          background: #2563eb;
          color: white;
          border-radius: 50%;
          display: flex;
          align-items: center;
          justify-content: center;
          font-weight: 700;
          font-size: 16px;
          margin: 0 auto 12px auto;
          box-shadow: 0 4px 10px rgba(37,99,235,0.3);
        }
        .step-icon {
          font-size: 32px;
          margin-bottom: 8px;
        }
        .step-title {
          font-size: 16px;
          font-weight: 700;
          color: #1e293b;
          margin-bottom: 6px;
        }
        .step-desc {
          font-size: 12px;
          color: #64748b;
          line-height: 1.5;
        }
        .step-key {
          display: inline-block;
          background: #1e293b;
          color: #f8fafc;
          padding: 2px 8px;
          border-radius: 6px;
          font-weight: 600;
          font-size: 12px;
          margin-top: 6px;
        }
        """

        steps_content = """
        <div class="card-container">
          <div class="header">
            <h2>🚀 เริ่มต้นใช้งาน AutoSGS ใน 4 ขั้นตอนง่าย ๆ</h2>
            <p>บันทึกคะแนนรวดเร็ว แม่นยำ ปลอดภัยในเสี้ยววินาที</p>
          </div>
          <div class="steps-grid">
            <div class="step-box">
              <div class="step-badge">1</div>
              <div class="step-icon">📋</div>
              <div class="step-title">คัดลอกจาก Excel</div>
              <div class="step-desc">ลากคลุมเฉพาะตัวเลขคะแนน<br>(ไม่เอาหัวตารางและชื่อ)</div>
              <span class="step-key">Ctrl + C</span>
            </div>
            <div class="step-box">
              <div class="step-badge">2</div>
              <div class="step-icon">⚡</div>
              <div class="step-title">เลือกโหมดใน AutoSGS</div>
              <div class="step-desc">โปรแกรมจับข้อมูลทันที<br>เลือกโหมดให้ตรงกับ SGS</div>
              <span class="step-key" style="background:#059669;">พร้อมทำงาน 🟢</span>
            </div>
            <div class="step-box">
              <div class="step-badge">3</div>
              <div class="step-icon">🎯</div>
              <div class="step-title">คลิกช่องแรก & กด F2</div>
              <div class="step-desc">คลิกที่ช่องเลขที่ 1 ใน SGS<br>แล้วกดปุ่มลัดเริ่มพิมพ์</div>
              <span class="step-key" style="background:#2563eb;">กด F2</span>
            </div>
            <div class="step-box">
              <div class="step-badge">4</div>
              <div class="step-icon">💾</div>
              <div class="step-title">กดบันทึกใน SGS</div>
              <div class="step-desc">พิมพ์เสร็จมีเสียงเตือน<br>คลิกปุ่มบันทึกในหน้าเว็บ SGS</div>
              <span class="step-key" style="background:#d97706;">กด บันทึก</span>
            </div>
          </div>
        </div>
        """

        page.set_content(HTML_WRAPPER.replace("{custom_css}", steps_css).replace("{content}", steps_content))
        element = page.query_selector(".card-container")
        element.screenshot(path=str(OUTPUT_DIR / "quick_steps_infographic.png"))
        print("[OK] Created quick_steps_infographic.png")

        # -------------------------------------------------------------
        # 2. AutoSGS Main Window UI (Dark Mode - Modern Prompt Font)
        # -------------------------------------------------------------
        app_css = """
        .app-window {
          width: 500px;
          background: #242424;
          border-radius: 12px;
          box-shadow: 0 16px 40px rgba(0,0,0,0.5);
          border: 1px solid #383838;
          overflow: hidden;
          color: #ffffff;
        }
        .window-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 14px 18px;
          background: #1e1e1e;
          border-bottom: 1px solid #333333;
        }
        .window-title {
          font-size: 18px;
          font-weight: 700;
          color: #3b8ed0;
          display: flex;
          align-items: center;
          gap: 6px;
        }
        .header-actions {
          display: flex;
          align-items: center;
          gap: 12px;
        }
        .switch-box {
          display: flex;
          align-items: center;
          gap: 6px;
          font-size: 13px;
          color: #cbd5e1;
        }
        .switch-pill {
          width: 34px;
          height: 18px;
          background: #3b8ed0;
          border-radius: 10px;
          position: relative;
        }
        .switch-circle {
          width: 14px;
          height: 14px;
          background: white;
          border-radius: 50%;
          position: absolute;
          right: 2px;
          top: 2px;
        }
        .btn-settings {
          background: #1a252f;
          border: 1px solid #34495e;
          color: white;
          font-size: 12px;
          font-weight: 600;
          padding: 5px 12px;
          border-radius: 6px;
        }
        .app-body {
          padding: 16px 18px;
        }
        .mode-row {
          display: flex;
          align-items: center;
          gap: 8px;
          margin-bottom: 12px;
        }
        .mode-label {
          font-size: 13px;
          font-weight: 700;
          color: #cbd5e1;
        }
        .mode-segmented {
          display: flex;
          flex: 1;
          background: #1a1a1a;
          border-radius: 8px;
          padding: 3px;
          gap: 3px;
        }
        .mode-tab {
          flex: 1;
          text-align: center;
          padding: 6px 4px;
          font-size: 12px;
          font-weight: 600;
          border-radius: 6px;
          color: #94a3b8;
        }
        .mode-tab.active {
          background: #3b8ed0;
          color: white;
        }
        .status-box {
          background: #2b2b2b;
          border-radius: 8px;
          padding: 12px;
          text-align: center;
          margin-bottom: 8px;
          border: 1px solid #383838;
        }
        .status-text {
          font-size: 15px;
          font-weight: 700;
          color: #2ecc71;
          margin-bottom: 4px;
        }
        .status-sub {
          font-size: 12px;
          color: #94a3b8;
        }
        .progress-track {
          width: 100%;
          height: 8px;
          background: #1a1a1a;
          border-radius: 4px;
          overflow: hidden;
          margin-bottom: 14px;
        }
        .progress-bar-fill {
          width: 0%;
          height: 100%;
          background: #3b8ed0;
        }
        .btn-start {
          width: 100%;
          background: #2980b9;
          color: white;
          font-size: 15px;
          font-weight: 700;
          padding: 12px;
          border-radius: 8px;
          border: none;
          text-align: center;
          margin-bottom: 14px;
          box-shadow: 0 4px 12px rgba(41,128,185,0.3);
        }
        .speed-control {
          margin-bottom: 12px;
        }
        .speed-label {
          display: flex;
          justify-content: space-between;
          font-size: 12px;
          color: #cbd5e1;
          margin-bottom: 6px;
        }
        .turbo-badge {
          background: #f59e0b;
          color: #1e1e1e;
          font-weight: 700;
          font-size: 11px;
          padding: 1px 6px;
          border-radius: 4px;
        }
        .slider-track {
          width: 100%;
          height: 6px;
          background: #383838;
          border-radius: 3px;
          position: relative;
        }
        .slider-fill {
          width: 15%;
          height: 100%;
          background: #3b8ed0;
          border-radius: 3px;
        }
        .slider-knob {
          width: 14px;
          height: 14px;
          background: white;
          border-radius: 50%;
          position: absolute;
          left: 15%;
          top: -4px;
          transform: translateX(-50%);
        }
        .btn-preview {
          width: 100%;
          background: #333333;
          color: #cbd5e1;
          font-size: 13px;
          font-weight: 600;
          padding: 9px;
          border-radius: 8px;
          border: none;
          text-align: center;
        }
        """

        app_ready_content = """
        <div class="app-window">
          <div class="window-header">
            <div class="window-title">⚡ AutoSGS</div>
            <div class="header-actions">
              <div class="switch-box">
                <span>อยู่บนสุด</span>
                <div class="switch-pill"><div class="switch-circle"></div></div>
              </div>
              <div class="btn-settings">⚙️ ตั้งค่า</div>
            </div>
          </div>
          <div class="app-body">
            <div class="mode-row">
              <span class="mode-label">โหมด:</span>
              <div class="mode-segmented">
                <div class="mode-tab active">📊 ผลการเรียน</div>
                <div class="mode-tab">⭐ คุณลักษณะฯ</div>
                <div class="mode-tab">📖 การอ่านฯ</div>
              </div>
            </div>
            <div class="status-box">
              <div class="status-text">🟢 พร้อมทำงาน (กด F2 หรือปุ่มเริ่ม)</div>
              <div class="status-sub">ข้อมูล: 40 แถว × 3 คอลัมน์ (พร้อมพิมพ์)</div>
            </div>
            <div class="progress-track"><div class="progress-bar-fill"></div></div>
            <div class="btn-start">▶ เริ่มพิมพ์ (3s) หรือกด F2</div>
            <div class="speed-control">
              <div class="speed-label">
                <span>หน่วงเวลาต่อช่อง: 0.10 วินาที (100 ms)</span>
                <span style="color:#94a3b8;">มาตรฐาน</span>
              </div>
              <div class="slider-track">
                <div class="slider-fill" style="width: 20%;"></div>
                <div class="slider-knob" style="left: 20%;"></div>
              </div>
            </div>
            <div class="btn-preview">▼ ดูตัวอย่างข้อมูลในคลิปบอร์ด (Preview)</div>
          </div>
        </div>
        """

        page.set_content(HTML_WRAPPER.replace("{custom_css}", app_css).replace("{content}", app_ready_content))
        element = page.query_selector(".app-window")
        element.screenshot(path=str(OUTPUT_DIR / "autosgs_main_ready.png"))
        print("[OK] Created autosgs_main_ready.png")

        # -------------------------------------------------------------
        # 3. AutoSGS Save Reminder Banner State (Characteristics Mode)
        # -------------------------------------------------------------
        reminder_css = app_css + """
        .reminder-banner {
          background: #451a03;
          border: 1.5px solid #d97706;
          border-radius: 8px;
          padding: 8px 12px;
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 12px;
        }
        .reminder-text {
          font-size: 13px;
          font-weight: 700;
          color: #fbbf24;
          display: flex;
          align-items: center;
          gap: 6px;
        }
        .reminder-close {
          color: #fbbf24;
          font-size: 14px;
          font-weight: 700;
          cursor: pointer;
        }
        """

        app_reminder_content = """
        <div class="app-window">
          <div class="window-header">
            <div class="window-title">⚡ AutoSGS</div>
            <div class="header-actions">
              <div class="switch-box">
                <span>อยู่บนสุด</span>
                <div class="switch-pill"><div class="switch-circle"></div></div>
              </div>
              <div class="btn-settings">⚙️ ตั้งค่า</div>
            </div>
          </div>
          <div class="app-body">
            <div class="mode-row">
              <span class="mode-label">โหมด:</span>
              <div class="mode-segmented">
                <div class="mode-tab">📊 ผลการเรียน</div>
                <div class="mode-tab active">⭐ คุณลักษณะฯ</div>
                <div class="mode-tab">📖 การอ่านฯ</div>
              </div>
            </div>
            <div class="status-box">
              <div class="status-text" style="color: #60a5fa;">✨ พิมพ์คะแนนเสร็จสมบูรณ์</div>
              <div class="status-sub">พิมพ์ครบทั้งหมด 40 แถว (320 ช่องคะแนน)</div>
            </div>
            <div class="progress-track"><div class="progress-bar-fill" style="width: 100%; background: #10b981;"></div></div>
            
            <div class="reminder-banner">
              <div class="reminder-text">💾 กรุณากดปุ่ม "บันทึก" ในระบบ SGS ด้วยนะครับ!</div>
              <div class="reminder-close">✕</div>
            </div>

            <div class="btn-start">▶ เริ่มพิมพ์ (3s) หรือกด F2</div>
            <div class="speed-control">
              <div class="speed-label">
                <span>หน่วงเวลาต่อช่อง: 0.02 วินาที (20 ms)</span>
                <span class="turbo-badge">⚡ ความเร็วสูงสุด</span>
              </div>
              <div class="slider-track">
                <div class="slider-fill" style="width: 4%; background: #f59e0b;"></div>
                <div class="slider-knob" style="left: 4%;"></div>
              </div>
            </div>
            <div class="btn-preview">▼ ดูตัวอย่างข้อมูลในคลิปบอร์ด (Preview)</div>
          </div>
        </div>
        """

        page.set_content(HTML_WRAPPER.replace("{custom_css}", reminder_css).replace("{content}", app_reminder_content))
        element = page.query_selector(".app-window")
        element.screenshot(path=str(OUTPUT_DIR / "autosgs_save_reminder.png"))
        print("[OK] Created autosgs_save_reminder.png")

        # -------------------------------------------------------------
        # 4. AutoSGS Preview Expanded State
        # -------------------------------------------------------------
        preview_css = app_css + """
        .preview-box {
          margin-top: 10px;
          background: #1a1a1a;
          border-radius: 8px;
          padding: 10px;
          border: 1px solid #333;
        }
        .preview-table {
          width: 100%;
          border-collapse: collapse;
          font-size: 11px;
          text-align: center;
        }
        .preview-table th {
          background: #2b2b2b;
          color: #94a3b8;
          padding: 4px;
          border: 1px solid #383838;
        }
        .preview-table td {
          padding: 4px;
          border: 1px solid #2e2e2e;
          color: #e2e8f0;
        }
        .preview-table tr:nth-child(even) td {
          background: #222222;
        }
        """

        app_preview_content = """
        <div class="app-window" style="width: 520px;">
          <div class="window-header">
            <div class="window-title">⚡ AutoSGS</div>
            <div class="header-actions">
              <div class="switch-box"><span>อยู่บนสุด</span><div class="switch-pill"><div class="switch-circle"></div></div></div>
              <div class="btn-settings">⚙️ ตั้งค่า</div>
            </div>
          </div>
          <div class="app-body">
            <div class="mode-row">
              <span class="mode-label">โหมด:</span>
              <div class="mode-segmented">
                <div class="mode-tab">📊 ผลการเรียน</div>
                <div class="mode-tab active">⭐ คุณลักษณะฯ</div>
                <div class="mode-tab">📖 การอ่านฯ</div>
              </div>
            </div>
            <div class="status-box">
              <div class="status-text">🟢 พร้อมทำงาน (กด F2 หรือปุ่มเริ่ม)</div>
              <div class="status-sub">ตรวจพบคลิปบอร์ด: 40 แถว × 8 คอลัมน์ (ตรงตามเกณฑ์ 8 ตัวชี้วัด)</div>
            </div>
            <div class="btn-start">▶ เริ่มพิมพ์ (3s) หรือกด F2</div>
            <div class="btn-preview" style="background:#2563eb; color:white;">▲ ซ่อนตัวอย่างข้อมูล (Preview ตรวจสอบความถูกต้อง)</div>
            
            <div class="preview-box">
              <table class="preview-table">
                <thead>
                  <tr>
                    <th>ลำดับ</th><th>ข้อ 1</th><th>ข้อ 2</th><th>ข้อ 3</th><th>ข้อ 4</th><th>ข้อ 5</th><th>ข้อ 6</th><th>ข้อ 7</th><th>ข้อ 8</th>
                  </tr>
                </thead>
                <tbody>
                  <tr><td>1</td><td>3</td><td>3</td><td>3</td><td>3</td><td>3</td><td>3</td><td>3</td><td>3</td></tr>
                  <tr><td>2</td><td>3</td><td>2</td><td>3</td><td>3</td><td>2</td><td>3</td><td>3</td><td>3</td></tr>
                  <tr><td>3</td><td>2</td><td>3</td><td>3</td><td>2</td><td>3</td><td>3</td><td>2</td><td>3</td></tr>
                  <tr><td>4</td><td>3</td><td>3</td><td>3</td><td>3</td><td>3</td><td>3</td><td>3</td><td>3</td></tr>
                  <tr><td>5</td><td>3</td><td>3</td><td>2</td><td>3</td><td>3</td><td>3</td><td>3</td><td>2</td></tr>
                </tbody>
              </table>
              <div style="text-align:center; font-size:11px; color:#64748b; margin-top:6px;">... แสดง 5 แถวแรกจากทั้งหมด 40 แถว ...</div>
            </div>
          </div>
        </div>
        """

        page.set_content(HTML_WRAPPER.replace("{custom_css}", preview_css).replace("{content}", app_preview_content))
        element = page.query_selector(".app-window")
        element.screenshot(path=str(OUTPUT_DIR / "autosgs_preview_open.png"))
        print("[OK] Created autosgs_preview_open.png")

        # -------------------------------------------------------------
        # 5. Excel Selection Guide (Correct vs Incorrect)
        # -------------------------------------------------------------
        excel_css = """
        .excel-card {
          background: #ffffff;
          border-radius: 12px;
          border: 1px solid #cbd5e1;
          box-shadow: 0 10px 25px rgba(0,0,0,0.08);
          padding: 24px;
          max-width: 820px;
          width: 100%;
        }
        .excel-title {
          font-size: 18px;
          font-weight: 700;
          color: #1e293b;
          margin-bottom: 6px;
          display: flex;
          align-items: center;
          gap: 8px;
        }
        .excel-sub {
          font-size: 13px;
          color: #64748b;
          margin-bottom: 16px;
        }
        .sheet-window {
          border: 1.5px solid #0f766e;
          border-radius: 8px;
          overflow: hidden;
          font-family: 'Segoe UI', Tahoma, sans-serif;
          font-size: 12px;
        }
        .sheet-bar {
          background: #0f766e;
          color: white;
          padding: 8px 14px;
          font-weight: 600;
          display: flex;
          justify-content: space-between;
        }
        .sheet-table {
          width: 100%;
          border-collapse: collapse;
          text-align: center;
        }
        .sheet-table th {
          background: #f1f5f9;
          border: 1px solid #cbd5e1;
          padding: 6px 8px;
          color: #475569;
          font-weight: 600;
        }
        .sheet-table td {
          border: 1px solid #e2e8f0;
          padding: 6px 8px;
          color: #1e293b;
        }
        .col-header {
          background: #e2e8f0 !important;
          font-weight: 700 !important;
        }
        .selected-zone {
          background-color: #dbeafe !important;
          border: 2px dashed #2563eb !important;
          font-weight: 700;
          color: #1e40af;
          position: relative;
        }
        .badge-do {
          background: #10b981;
          color: white;
          padding: 2px 8px;
          border-radius: 4px;
          font-size: 11px;
          font-weight: 700;
          margin-left: 6px;
        }
        .badge-dont {
          background: #ef4444;
          color: white;
          padding: 2px 8px;
          border-radius: 4px;
          font-size: 11px;
          font-weight: 700;
          margin-left: 6px;
        }
        .legend {
          display: flex;
          gap: 20px;
          margin-top: 14px;
          font-size: 13px;
        }
        .legend-item {
          display: flex;
          align-items: center;
          gap: 6px;
        }
        """

        excel_content = """
        <div class="excel-card">
          <div class="excel-title">📊 วิธีการลากคลุมคะแนนใน Microsoft Excel / Google Sheets</div>
          <div class="excel-sub">ลากคลุมเฉพาะช่วงคะแนนที่ต้องการบันทึก ห้ามลากคลุมหัวตารางหรือรายชื่อนักเรียน</div>
          
          <div class="sheet-window">
            <div class="sheet-bar">
              <span>📗 คะแนน ม.3_1.xlsx - Excel</span>
              <span>100% Zoom</span>
            </div>
            <table class="sheet-table">
              <thead>
                <tr>
                  <th class="col-header"></th>
                  <th class="col-header">A</th>
                  <th class="col-header">B</th>
                  <th class="col-header">C</th>
                  <th class="col-header">D</th>
                  <th class="col-header">E</th>
                </tr>
                <tr>
                  <th class="col-header">1</th>
                  <th>เลขที่ <span class="badge-dont">❌ ไม่คลุม</span></th>
                  <th>ชื่อ - นามสกุล <span class="badge-dont">❌ ไม่คลุม</span></th>
                  <th style="background:#fef3c7; color:#92400e;">เก็บ 1 (20)</th>
                  <th style="background:#fef3c7; color:#92400e;">กลางภาค (20)</th>
                  <th style="background:#fef3c7; color:#92400e;">ปลายภาค (30)</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <th class="col-header">2</th>
                  <td>1</td>
                  <td style="text-align:left;">ด.ช. กิตติศักดิ์ เจริญพร</td>
                  <td class="selected-zone">18</td>
                  <td class="selected-zone">16</td>
                  <td class="selected-zone">25</td>
                </tr>
                <tr>
                  <th class="col-header">3</th>
                  <td>2</td>
                  <td style="text-align:left;">ด.ญ. กัญญารัตน์ สมบูรณ์</td>
                  <td class="selected-zone">19</td>
                  <td class="selected-zone">18</td>
                  <td class="selected-zone">28</td>
                </tr>
                <tr>
                  <th class="col-header">4</th>
                  <td>3</td>
                  <td style="text-align:left;">ด.ช. ชัยวัฒน์ วงศ์สุวรรณ</td>
                  <td class="selected-zone">15</td>
                  <td class="selected-zone"></td>
                  <td class="selected-zone">22</td>
                </tr>
                <tr>
                  <th class="col-header">5</th>
                  <td>4</td>
                  <td style="text-align:left;">ด.ญ. ณัฐธิดา สุขเกษม</td>
                  <td class="selected-zone">20</td>
                  <td class="selected-zone">19</td>
                  <td class="selected-zone">29</td>
                </tr>
              </tbody>
            </table>
          </div>

          <div class="legend">
            <div class="legend-item">
              <span style="display:inline-block; width:16px; height:16px; background:#dbeafe; border:2px dashed #2563eb; border-radius:3px;"></span>
              <b>ช่วงที่ต้องคลุม (Ctrl + C):</b> เฉพาะเซลล์ตัวเลขคะแนน C2:E5
            </div>
            <div class="legend-item">
              <span style="color:#d97706; font-weight:700;">💡 ช่องว่าง:</span>
              เด็กขาดสอบ ให้เว้นว่างไว้ โปรแกรมจะเคาะ Tab ข้ามให้อัตโนมัติ
            </div>
          </div>
        </div>
        """

        page.set_content(HTML_WRAPPER.replace("{custom_css}", excel_css).replace("{content}", excel_content))
        element = page.query_selector(".excel-card")
        element.screenshot(path=str(OUTPUT_DIR / "excel_copy_guide.png"))
        print("[OK] Created excel_copy_guide.png")

        # -------------------------------------------------------------
        # 6. Settings Dialog UI
        # -------------------------------------------------------------
        settings_css = """
        .settings-dialog {
          width: 440px;
          background: #2b2b2b;
          border-radius: 12px;
          border: 1px solid #444;
          box-shadow: 0 20px 50px rgba(0,0,0,0.6);
          color: #ffffff;
          overflow: hidden;
        }
        .settings-header {
          padding: 14px 18px;
          background: #1f1f1f;
          border-bottom: 1px solid #383838;
          font-size: 16px;
          font-weight: 700;
          color: #3b8ed0;
        }
        .settings-body {
          padding: 18px;
          display: flex;
          flex-direction: column;
          gap: 14px;
        }
        .form-row {
          display: flex;
          justify-content: space-between;
          align-items: center;
        }
        .form-label {
          font-size: 13px;
          color: #cbd5e1;
        }
        .form-select {
          background: #1a1a1a;
          border: 1px solid #444;
          color: white;
          padding: 6px 12px;
          border-radius: 6px;
          font-size: 13px;
          font-family: 'Prompt', sans-serif;
          min-width: 140px;
          text-align: right;
        }
        .dialog-actions {
          display: flex;
          justify-content: flex-end;
          gap: 10px;
          margin-top: 10px;
          padding-top: 14px;
          border-top: 1px solid #383838;
        }
        .btn-reset {
          background: #475569;
          border: none;
          color: white;
          padding: 8px 14px;
          border-radius: 6px;
          font-size: 13px;
          font-weight: 600;
        }
        .btn-save {
          background: #2563eb;
          border: none;
          color: white;
          padding: 8px 18px;
          border-radius: 6px;
          font-size: 13px;
          font-weight: 600;
        }
        """

        settings_content = """
        <div class="settings-dialog">
          <div class="settings-header">⚙️ การตั้งค่า AutoSGS</div>
          <div class="settings-body">
            <div class="form-row">
              <span class="form-label">ปุ่มลัดเริ่มพิมพ์ (Global Hotkey)</span>
              <div class="form-select">F2 ▼</div>
            </div>
            <div class="form-row">
              <span class="form-label">ขนาดตัวอักษร / Scaling</span>
              <div class="form-select">ใหญ่ (115%) ▼</div>
            </div>
            <div class="form-row">
              <span class="form-label">ธีมการแสดงผล (Theme)</span>
              <div class="form-select">System (ตามวินโดวส์) ▼</div>
            </div>
            <div class="form-row">
              <span class="form-label">เปิดใช้งานเสียงแจ้งเตือน</span>
              <div style="color:#10b981; font-weight:700; font-size:13px;">✔ เปิดเสียง (Beep/Chime)</div>
            </div>
            <div class="form-row">
              <span class="form-label">เวลานับถอยหลังก่อนพิมพ์</span>
              <div class="form-select" style="min-width:70px; text-align:center;">3 วินาที</div>
            </div>
            
            <div class="dialog-actions">
              <button class="btn-reset">คืนค่าเริ่มต้น</button>
              <button class="btn-save">บันทึกการตั้งค่า</button>
            </div>
          </div>
        </div>
        """

        page.set_content(HTML_WRAPPER.replace("{custom_css}", settings_css).replace("{content}", settings_content))
        element = page.query_selector(".settings-dialog")
        element.screenshot(path=str(OUTPUT_DIR / "autosgs_settings.png"))
        print("[OK] Created autosgs_settings.png")

        # -------------------------------------------------------------
        # 7. SGS Mock Forms (Mode 1, Mode 2, Mode 3)
        # -------------------------------------------------------------
        # Load mock_sgs.html and switch modes, then take high-res snapshots
        mock_file = Path("tests/mock_sgs.html").resolve().as_uri()
        page.goto(mock_file)
        page.wait_for_timeout(500)

        # Mode 1
        page.click("#nav_scores")
        page.click("#btnSampleMain")
        page.wait_for_timeout(300)
        table_el = page.query_selector(".header-card")
        page.screenshot(path=str(OUTPUT_DIR / "sgs_mode1_guide.png"), clip={"x": 20, "y": 20, "width": 1050, "height": 480})
        print("[OK] Created sgs_mode1_guide.png")

        # Mode 2 (Characteristics - 8 columns)
        page.click("#nav_characteristics")
        page.click("#btnSampleMain")
        page.wait_for_timeout(300)
        page.screenshot(path=str(OUTPUT_DIR / "sgs_mode2_guide.png"), clip={"x": 20, "y": 20, "width": 1050, "height": 500})
        print("[OK] Created sgs_mode2_guide.png")

        # Mode 3 (Reading Analysis - 6 columns)
        page.click("#nav_reading_analysis")
        page.click("#btnSampleMain")
        page.wait_for_timeout(300)
        page.screenshot(path=str(OUTPUT_DIR / "sgs_mode3_guide.png"), clip={"x": 20, "y": 20, "width": 1050, "height": 500})
        print("[OK] Created sgs_mode3_guide.png")

        browser.close()
        print("\n[DONE] All illustrations generated successfully in docs/images/!")

if __name__ == "__main__":
    generate_assets()
