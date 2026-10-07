"""
Script to build a professional 16:9 Widescreen PPTX User Guide for AutoSGS.
Uses python-pptx with Prompt/Segoe UI typography, cards, diagrams, and screenshots.
"""

from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

DOCS_DIR = Path("docs")
IMAGES_DIR = DOCS_DIR / "images"
ASSETS_DIR = Path("assets")
OUTPUT_PPTX = DOCS_DIR / "AutoSGS_User_Manual.pptx"

# Color Palette
COLOR_BG = RGBColor(248, 250, 252)        # Slate 50
COLOR_PRIMARY = RGBColor(37, 99, 235)      # Blue 600
COLOR_PRIMARY_DARK = RGBColor(30, 58, 138) # Blue 900
COLOR_ACCENT = RGBColor(217, 119, 6)       # Amber 600
COLOR_SUCCESS = RGBColor(5, 150, 105)      # Emerald 600
COLOR_TEXT_DARK = RGBColor(15, 23, 42)     # Slate 900
COLOR_TEXT_MUTED = RGBColor(100, 116, 139) # Slate 500
COLOR_CARD_BG = RGBColor(255, 255, 255)    # White
COLOR_CARD_BORDER = RGBColor(226, 232, 240)# Slate 200

FONT_MAIN = "Prompt"
FONT_BACKUP = "Segoe UI"

def set_shape_flat(shape, fill_color, line_color=None, line_width=1):
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    if line_color:
        shape.line.color.rgb = line_color
        shape.line.width = Pt(line_width)
    else:
        shape.line.fill.background()

def add_header(slide, title_text, category_text="AutoSGS คู่มือการใช้งาน"):
    # Category tag
    tb_cat = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.5), Inches(0.4))
    p_cat = tb_cat.text_frame.paragraphs[0]
    p_cat.text = category_text.upper()
    p_cat.font.name = FONT_MAIN
    p_cat.font.size = Pt(11)
    p_cat.font.bold = True
    p_cat.font.color.rgb = COLOR_PRIMARY
    
    # Title
    tb_title = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.5), Inches(0.7))
    p_title = tb_title.text_frame.paragraphs[0]
    p_title.text = title_text
    p_title.font.name = FONT_MAIN
    p_title.font.size = Pt(22)
    p_title.font.bold = True
    p_title.font.color.rgb = COLOR_PRIMARY_DARK

def add_card(slide, left, top, width, height, bg_color=COLOR_CARD_BG, border_color=COLOR_CARD_BORDER):
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    set_shape_flat(card, bg_color, border_color, 1.2)
    return card

def build_pptx():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # =========================================================================
    # SLIDE 1: Cover Slide
    # =========================================================================
    slide1 = prs.slides.add_slide(blank_layout)
    bg1 = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    set_shape_flat(bg1, RGBColor(241, 245, 249))

    # Center card
    card1 = add_card(slide1, Inches(1.5), Inches(0.9), Inches(10.333), Inches(5.7), COLOR_CARD_BG, RGBColor(186, 230, 253))
    
    # Logo
    icon_path = ASSETS_DIR / "icon.png"
    if icon_path.exists():
        slide1.shapes.add_picture(str(icon_path), Inches(5.866), Inches(1.3), width=Inches(1.6))

    # Titles
    tb_title = slide1.shapes.add_textbox(Inches(2.0), Inches(3.1), Inches(9.333), Inches(1.0))
    p1 = tb_title.text_frame.paragraphs[0]
    p1.alignment = PP_ALIGN.CENTER
    p1.text = "⚡ AutoSGS v1.1.0"
    p1.font.name = FONT_MAIN
    p1.font.size = Pt(36)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_PRIMARY_DARK

    tb_sub = slide1.shapes.add_textbox(Inches(2.0), Inches(4.1), Inches(9.333), Inches(0.8))
    p2 = tb_sub.text_frame.paragraphs[0]
    p2.alignment = PP_ALIGN.CENTER
    p2.text = "คู่มือการใช้งานระบบช่วยพิมพ์คะแนนอัตโนมัติลงระบบ SGS"
    p2.font.name = FONT_MAIN
    p2.font.size = Pt(20)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_PRIMARY

    tb_meta = slide1.shapes.add_textbox(Inches(2.0), Inches(5.0), Inches(9.333), Inches(1.0))
    p3 = tb_meta.text_frame.paragraphs[0]
    p3.alignment = PP_ALIGN.CENTER
    p3.text = "สำหรับครูผู้สอนบันทึกผลการเรียน คุณลักษณะอันพึงประสงค์ และการอ่านคิดวิเคราะห์ฯ\nรวดเร็ว • แม่นยำ • ปลอดภัย 100% | จัดทำโดย NOGiTTiS"
    p3.font.name = FONT_MAIN
    p3.font.size = Pt(13)
    p3.font.color.rgb = COLOR_TEXT_MUTED

    # =========================================================================
    # SLIDE 2: ปัญหาจริง & ทางออก (Pain Point vs Solution)
    # =========================================================================
    slide2 = prs.slides.add_slide(blank_layout)
    add_header(slide2, "ทำไมต้องใช้ AutoSGS? ปัญหาจริงของครูผู้สอน")

    # Card 1: ปัญหาเดิม
    card_pain = add_card(slide2, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.3), RGBColor(254, 242, 242), RGBColor(254, 202, 202))
    tb_pain = slide2.shapes.add_textbox(Inches(1.1), Inches(1.8), Inches(5.0), Inches(4.8))
    tf_p = tb_pain.text_frame
    tf_p.word_wrap = True
    p = tf_p.paragraphs[0]
    p.text = "❌ วิธีเดิม: พิมพ์มือทีละช่อง"
    p.font.name = FONT_MAIN
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = RGBColor(185, 28, 28)

    points_pain = [
      "นักเรียน 1 ห้องมี 40-50 คน หากสอน 5 ห้อง รวมกว่า 200 คน",
      "ต้องเคาะแป้นตัวเลข + กด Tab ซ้ำ ๆ กว่า 4,000–5,000 ครั้ง!",
      "อาการปวดเมื่อยข้อมือ นิ้วล็อก และสายตาอ่อนล้า",
      "เสี่ยงคลิกผิดช่อง คะแนนเลื่อนทั้งแถว ต้องไล่หาและแก้ใหม่",
      "เสียเวลาตรวจและพิมพ์ข้อมูลหลายวันในแต่ละช่วงสิ้นเทอม"
    ]
    for pt in points_pain:
        p = tf_p.add_paragraph()
        p.text = f"• {pt}"
        p.font.name = FONT_MAIN
        p.font.size = Pt(13.5)
        p.font.color.rgb = RGBColor(127, 29, 29)
        p.space_before = Pt(10)

    # Card 2: ทางออกด้วย AutoSGS
    card_sol = add_card(slide2, Inches(6.8), Inches(1.5), Inches(5.6), Inches(5.3), RGBColor(240, 253, 244), RGBColor(187, 247, 208))
    tb_sol = slide2.shapes.add_textbox(Inches(7.1), Inches(1.8), Inches(5.0), Inches(4.8))
    tf_s = tb_sol.text_frame
    tf_s.word_wrap = True
    p = tf_s.paragraphs[0]
    p.text = "⚡ ทางออกด้วย AutoSGS"
    p.font.name = FONT_MAIN
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = RGBColor(4, 120, 87)

    points_sol = [
      "คัดลอก (Ctrl+C) จาก Excel โปรแกรมจับข้อมูลคลิปบอร์ดทันที",
      "คลิกช่องแรกในเว็บ SGS แล้วกด F2 เริ่มพิมพ์อัตโนมัติ",
      "กด Tab ข้ามช่องสรุปให้อัตโนมัติ (ข้าม 4 ช่อง / 2 ช่อง)",
      "พิมพ์เสร็จ 1 ห้องในไม่กี่วินาที ด้วยโหมด Turbo ⚡ (20ms)",
      "มีระบบหยุดฉุกเฉิน (ESC) หยุดได้ในพริบตา (<50ms) ปลอดภัย 100%"
    ]
    for pt in points_sol:
        p = tf_s.add_paragraph()
        p.text = f"• {pt}"
        p.font.name = FONT_MAIN
        p.font.size = Pt(13.5)
        p.font.color.rgb = RGBColor(6, 78, 59)
        p.space_before = Pt(10)

    # =========================================================================
    # SLIDE 3: ภาพรวมขั้นตอนการใช้งาน (Quick Steps Infographic)
    # =========================================================================
    slide3 = prs.slides.add_slide(blank_layout)
    add_header(slide3, "ขั้นตอนการทำงาน 4 ขั้นตอนง่าย ๆ (Workflow)")

    img_steps = IMAGES_DIR / "quick_steps_infographic.png"
    if img_steps.exists():
        slide3.shapes.add_picture(str(img_steps), Inches(1.0), Inches(1.6), width=Inches(11.333))

    tb_flow_notes = slide3.shapes.add_textbox(Inches(1.0), Inches(5.9), Inches(11.333), Inches(1.0))
    p = tb_flow_notes.text_frame.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    p.text = "💡 เคล็ดลับ: การกดปุ่ม F2 เป็นวิธีที่สะดวกและแนะนำมากที่สุด เพียงคลิกช่องแรกแล้วกด F2 โปรแกรมจะทำงานให้ทันที"
    p.font.name = FONT_MAIN
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_PRIMARY

    # =========================================================================
    # SLIDE 4: ขั้นตอนที่ 1: การคลุมช่วงคะแนนใน Excel
    # =========================================================================
    slide4 = prs.slides.add_slide(blank_layout)
    add_header(slide4, "ขั้นตอนที่ 1: คัดลอกจาก Excel / Google Sheets")

    img_excel = IMAGES_DIR / "excel_copy_guide.png"
    if img_excel.exists():
        slide4.shapes.add_picture(str(img_excel), Inches(0.8), Inches(1.5), width=Inches(7.2))

    card_ex_rules = add_card(slide4, Inches(8.3), Inches(1.5), Inches(4.2), Inches(5.3))
    tb_rules = slide4.shapes.add_textbox(Inches(8.5), Inches(1.7), Inches(3.8), Inches(4.9))
    tf_r = tb_rules.text_frame
    tf_r.word_wrap = True
    p = tf_r.paragraphs[0]
    p.text = "📌 กฎเหล็กในการคลุมคะแนน"
    p.font.name = FONT_MAIN
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = COLOR_PRIMARY_DARK

    excel_rules = [
      "คลุมเฉพาะ 'ตัวเลขคะแนน' เท่านั้น",
      "❌ ห้ามคลุมหัวตาราง (เช่น ข้อ 1, สอบกลางภาค)",
      "❌ ห้ามคลุมเลขที่ หรือชื่อ-นามสกุลนักเรียน",
      "เรียงลำดับเลขที่ใน Excel ให้ตรงกับหน้าเว็บ SGS",
      "หากมีเด็กขาดสอบ ให้เว้นเซลล์ว่างไว้ โปรแกรมจะกด Tab เปล่าข้ามให้อัตโนมัติ",
      "เมื่อคลุมเสร็จแล้ว กด Ctrl + C เพื่อคัดลอก"
    ]
    for r in excel_rules:
        p = tf_r.add_paragraph()
        p.text = f"• {r}"
        p.font.name = FONT_MAIN
        p.font.size = Pt(12)
        p.font.color.rgb = COLOR_TEXT_DARK
        p.space_before = Pt(8)

    # =========================================================================
    # SLIDE 5: ขั้นตอนที่ 2: หน้าต่าง AutoSGS & ตรวจเช็ค
    # =========================================================================
    slide5 = prs.slides.add_slide(blank_layout)
    add_header(slide5, "ขั้นตอนที่ 2: หน้าต่าง AutoSGS & การตรวจเช็คข้อมูล")

    img_app = IMAGES_DIR / "autosgs_main_ready.png"
    if img_app.exists():
        slide5.shapes.add_picture(str(img_app), Inches(1.0), Inches(1.5), height=Inches(5.3))

    card_ui_desc = add_card(slide5, Inches(5.8), Inches(1.5), Inches(6.7), Inches(5.3))
    tb_ui_desc = slide5.shapes.add_textbox(Inches(6.1), Inches(1.7), Inches(6.1), Inches(4.9))
    tf_u = tb_ui_desc.text_frame
    tf_u.word_wrap = True
    p = tf_u.paragraphs[0]
    p.text = "🔍 ส่วนประกอบและจุดสังเกตสำคัญ"
    p.font.name = FONT_MAIN
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = COLOR_PRIMARY_DARK

    ui_points = [
      ("สวิตช์ 'อยู่บนสุด' (Always on Top)", "หน้าต่างโปรแกรมจะลอยอยู่มุมจอเสมอ มองเห็นสถานะได้ตลอดเวลา"),
      ("แถบเลือกโหมด 3 โหมด", "เลือกให้ตรงกับหน้า SGS ที่กำลังจะพิมพ์ (คะแนน / คุณลักษณะฯ / การอ่านฯ)"),
      ("กล่องสถานะอัจฉริยะ", "สังเกตสีเขียว 'พร้อมทำงาน' พร้อมระบุจำนวนแถวและคอลัมน์ที่ตรวจพบ"),
      ("แถบ Slider ปรับสปีด", "เลือกความเร็วได้อิสระ โหมดประเมินใช้ Turbo 0.02s ⚡ ได้รวดเร็วมาก"),
      ("ปุ่ม Preview ข้อมูล", "คลิกเพื่อคลี่ดูตารางคะแนนในคลิปบอร์ด มั่นใจ 100% ก่อนเริ่มพิมพ์")
    ]
    for title, desc in ui_points:
        p = tf_u.add_paragraph()
        p.text = f"✔ {title}: "
        p.font.name = FONT_MAIN
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = COLOR_PRIMARY
        p.space_before = Pt(8)
        
        p_desc = tf_u.add_paragraph()
        p_desc.text = f"    {desc}"
        p_desc.font.name = FONT_MAIN
        p_desc.font.size = Pt(11.5)
        p_desc.font.color.rgb = COLOR_TEXT_MUTED

    # =========================================================================
    # SLIDE 6: ตารางเปรียบเทียบ 3 โหมดการทำงาน
    # =========================================================================
    slide6 = prs.slides.add_slide(blank_layout)
    add_header(slide6, "เจาะลึก 3 โหมดการกรอกคะแนนในระบบ SGS")

    modes = [
      ("📊 1. ผลการเรียน", "คะแนนรายวิชาทั่วไป", "อิสระ (1 - N ช่อง)", "พิมพ์ + Tab 1 ครั้งทุกช่อง", "ไม่มี Tab พิเศษ", "0.10s (ปลอดภัย)", RGBColor(239, 246, 255), COLOR_PRIMARY),
      ("⭐ 2. คุณลักษณะฯ", "ประเมินคุณลักษณะ 8 ข้อ", "8 ตัวชี้วัด", "พิมพ์ + Tab (8 ช่อง)", "กด Tab เพิ่ม 4 ครั้งท้ายแถว!", "0.02s ⚡ Turbo", RGBColor(254, 243, 199), COLOR_ACCENT),
      ("📖 3. การอ่าน คิดวิเคราะห์ฯ", "ประเมินการอ่านฯ 5 ข้อ", "5 ตัวชี้วัด", "พิมพ์ + Tab (5 ช่อง)", "กด Tab เพิ่ม 3 ครั้งท้ายแถว!", "0.02s ⚡ Turbo", RGBColor(236, 253, 245), COLOR_SUCCESS),
    ]

    for idx, (m_title, m_desc, m_cols, m_action, m_tabs, m_speed, bg_c, border_c) in enumerate(modes):
        left = Inches(0.8 + idx * 3.9)
        add_card(slide6, left, Inches(1.5), Inches(3.7), Inches(5.3), bg_c, border_c)
        tb_m = slide6.shapes.add_textbox(left + Inches(0.2), Inches(1.7), Inches(3.3), Inches(4.9))
        tf_m = tb_m.text_frame
        tf_m.word_wrap = True
        
        p = tf_m.paragraphs[0]
        p.text = m_title
        p.font.name = FONT_MAIN
        p.font.size = Pt(17)
        p.font.bold = True
        p.font.color.rgb = border_c

        details = [
          ("ประเภทงาน", m_desc),
          ("จำนวนช่อง", m_cols),
          ("พฤติกรรมในแถว", m_action),
          ("ท้ายแถวคน", m_tabs),
          ("สปีดแนะนำ", m_speed),
        ]
        for lbl, val in details:
            p = tf_m.add_paragraph()
            p.text = f"• {lbl}:"
            p.font.name = FONT_MAIN
            p.font.size = Pt(11.5)
            p.font.bold = True
            p.font.color.rgb = COLOR_TEXT_DARK
            p.space_before = Pt(8)

            p_val = tf_m.add_paragraph()
            p_val.text = f"  {val}"
            p_val.font.name = FONT_MAIN
            p_val.font.size = Pt(12)
            p_val.font.color.rgb = COLOR_PRIMARY_DARK if lbl == "ท้ายแถวคน" else COLOR_TEXT_MUTED

    # =========================================================================
    # SLIDE 7: โหมด 1: ผลการเรียน (Academic Scores)
    # =========================================================================
    slide7 = prs.slides.add_slide(blank_layout)
    add_header(slide7, "โหมดที่ 1: ผลการเรียนรายวิชาทั่วไป (Academic Scores)")

    img_m1 = IMAGES_DIR / "sgs_mode1_guide.png"
    if img_m1.exists():
        slide7.shapes.add_picture(str(img_m1), Inches(0.8), Inches(1.5), width=Inches(8.2))

    card_m1 = add_card(slide7, Inches(9.3), Inches(1.5), Inches(3.2), Inches(5.3))
    tb_m1 = slide7.shapes.add_textbox(Inches(9.5), Inches(1.7), Inches(2.8), Inches(4.9))
    tf_1 = tb_m1.text_frame
    tf_1.word_wrap = True
    p = tf_1.paragraphs[0]
    p.text = "📊 การใช้งานโหมด 1"
    p.font.name = FONT_MAIN
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = COLOR_PRIMARY

    m1_points = [
      "เหมาะสำหรับคะแนนเก็บย่อย กลางภาค ปลายภาค",
      "รองรับทั้งคัดลอก 1 คอลัมน์ หรือหลายคอลัมน์พร้อมกัน",
      "พิมพ์คะแนน + Tab 1 ครั้งทุกช่อง ไม่มี Tab พิเศษ",
      "ความเร็วแนะนำ: 0.10s เพื่อให้สูตรคำนวณใน SGS ประมวลผลทัน"
    ]
    for pt in m1_points:
        p = tf_1.add_paragraph()
        p.text = f"• {pt}"
        p.font.name = FONT_MAIN
        p.font.size = Pt(11.5)
        p.font.color.rgb = COLOR_TEXT_DARK
        p.space_before = Pt(8)

    # =========================================================================
    # SLIDE 8: โหมด 2: คุณลักษณะอันพึงประสงค์ (8 ตัวชี้วัด)
    # =========================================================================
    slide8 = prs.slides.add_slide(blank_layout)
    add_header(slide8, "โหมดที่ 2: คุณลักษณะอันพึงประสงค์ (8 ตัวชี้วัด + ข้าม 4 Tab)")

    img_m2 = IMAGES_DIR / "sgs_mode2_guide.png"
    if img_m2.exists():
        slide8.shapes.add_picture(str(img_m2), Inches(0.8), Inches(1.5), width=Inches(8.2))

    card_m2 = add_card(slide8, Inches(9.3), Inches(1.5), Inches(3.2), Inches(5.3))
    tb_m2 = slide8.shapes.add_textbox(Inches(9.5), Inches(1.7), Inches(2.8), Inches(4.9))
    tf_2 = tb_m2.text_frame
    tf_2.word_wrap = True
    p = tf_2.paragraphs[0]
    p.text = "⭐ การใช้งานโหมด 2"
    p.font.name = FONT_MAIN
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = COLOR_ACCENT

    m2_points = [
      "ช่อง 1 ถึง 8 พิมพ์คะแนน + Tab",
      "⚡ โปรแกรมส่ง Tab เปล่าเพิ่มอีก 4 ครั้งท้ายแถวอัตโนมัติ เพื่อข้ามช่องรวม/ฐานนิยม/ผลประเมิน/แก้ไข",
      "เคอร์เซอร์จะลงช่องข้อ 1 ของนักเรียนคนถัดไปพอดี 100%",
      "ความเร็วแนะนำ: 0.02s (Turbo ⚡) บันทึก 40 คนเสร็จในไม่กี่วินาที"
    ]
    for pt in m2_points:
        p = tf_2.add_paragraph()
        p.text = f"• {pt}"
        p.font.name = FONT_MAIN
        p.font.size = Pt(11.5)
        p.font.color.rgb = COLOR_TEXT_DARK
        p.space_before = Pt(8)

    # =========================================================================
    # SLIDE 9: โหมด 3: การอ่าน คิดวิเคราะห์และเขียน (5 ตัวชี้วัด)
    # =========================================================================
    slide9 = prs.slides.add_slide(blank_layout)
    add_header(slide9, "โหมดที่ 3: การอ่าน คิดวิเคราะห์และเขียน (5 ตัวชี้วัด + ข้าม 3 Tab)")

    img_m3 = IMAGES_DIR / "sgs_mode3_guide.png"
    if img_m3.exists():
        slide9.shapes.add_picture(str(img_m3), Inches(0.8), Inches(1.5), width=Inches(8.2))

    card_m3 = add_card(slide9, Inches(9.3), Inches(1.5), Inches(3.2), Inches(5.3))
    tb_m3 = slide9.shapes.add_textbox(Inches(9.5), Inches(1.7), Inches(2.8), Inches(4.9))
    tf_3 = tb_m3.text_frame
    tf_3.word_wrap = True
    p = tf_3.paragraphs[0]
    p.text = "📖 การใช้งานโหมด 3"
    p.font.name = FONT_MAIN
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = COLOR_SUCCESS

    m3_points = [
      "ช่อง 1 ถึง 5 พิมพ์คะแนน + Tab",
      "⚡ โปรแกรมส่ง Tab เปล่าเพิ่มอีก 3 ครั้งท้ายแถวอัตโนมัติ เพื่อข้ามช่องผลรวม/ผลประเมิน/แก้ไข",
      "เคอร์เซอร์จะลงช่องข้อ 1 ของนักเรียนคนถัดไปพอดี 100%",
      "ความเร็วแนะนำ: 0.02s (Turbo ⚡) พิมพ์เสร็จรวดเร็วทันใจ"
    ]
    for pt in m3_points:
        p = tf_3.add_paragraph()
        p.text = f"• {pt}"
        p.font.name = FONT_MAIN
        p.font.size = Pt(11.5)
        p.font.color.rgb = COLOR_TEXT_DARK
        p.space_before = Pt(8)

    # =========================================================================
    # SLIDE 10: สั่งเริ่มพิมพ์ & การกดบันทึกใน SGS
    # =========================================================================
    slide10 = prs.slides.add_slide(blank_layout)
    add_header(slide10, "ขั้นตอนที่ 3 & 4: สั่งพิมพ์คะแนน และกดบันทึกใน SGS")

    img_rem = IMAGES_DIR / "autosgs_save_reminder.png"
    if img_rem.exists():
        slide10.shapes.add_picture(str(img_rem), Inches(0.8), Inches(1.5), height=Inches(5.3))

    card_step34 = add_card(slide10, Inches(5.6), Inches(1.5), Inches(6.9), Inches(5.3))
    tb_s34 = slide10.shapes.add_textbox(Inches(5.9), Inches(1.7), Inches(6.3), Inches(4.9))
    tf_34 = tb_s34.text_frame
    tf_34.word_wrap = True

    p = tf_34.paragraphs[0]
    p.text = "🎯 2 วิธีการสั่งพิมพ์ที่เลือกได้"
    p.font.name = FONT_MAIN
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = COLOR_PRIMARY_DARK

    p1 = tf_34.add_paragraph()
    p1.text = "• วิธีที่ 1 (แนะนำมากที่สุด): สลับไปเว็บ SGS คลิกช่องแรกของเลขที่ 1 แล้วกดปุ่ม F2 บนคีย์บอร์ดเพียงครั้งเดียว"
    p1.font.name = FONT_MAIN
    p1.font.size = Pt(12)
    p1.font.color.rgb = COLOR_TEXT_DARK
    p1.space_before = Pt(6)

    p2 = tf_34.add_paragraph()
    p2.text = "• วิธีที่ 2: กดปุ่ม '▶ เริ่มพิมพ์ (3s)' ในโปรแกรม ฟังเสียงนับถอยหลัง แล้วสลับไปคลิกช่องแรกใน SGS"
    p2.font.name = FONT_MAIN
    p2.font.size = Pt(12)
    p2.font.color.rgb = COLOR_TEXT_DARK
    p2.space_before = Pt(6)

    p3 = tf_34.add_paragraph()
    p3.text = "💾 สำคัญมาก: การกดปุ่ม 'บันทึก' ในระบบ SGS"
    p3.font.name = FONT_MAIN
    p3.font.size = Pt(17)
    p3.font.bold = True
    p3.font.color.rgb = COLOR_ACCENT
    p3.space_before = Pt(14)

    p4 = tf_34.add_paragraph()
    p4.text = "• เมื่อพิมพ์เสร็จสิ้น จะมีแถบเตือนสีส้มแจ้งเตือนเสมอ\n• คุณครูต้องเลื่อนลงไปคลิกปุ่ม 'บันทึก' ในหน้าเว็บ SGS ด้วยตนเองเสมอ คะแนนจึงจะถูกบันทึกเข้าฐานข้อมูลโรงเรียนอย่างสมบูรณ์"
    p4.font.name = FONT_MAIN
    p4.font.size = Pt(12)
    p4.font.color.rgb = COLOR_TEXT_DARK
    p4.space_before = Pt(6)

    # =========================================================================
    # SLIDE 11: ความปลอดภัยสูงสุด & Preview
    # =========================================================================
    slide11 = prs.slides.add_slide(blank_layout)
    add_header(slide11, "ระบบความปลอดภัย & การตรวจสอบข้อมูลด้วย Preview")

    img_prev = IMAGES_DIR / "autosgs_preview_open.png"
    if img_prev.exists():
        slide11.shapes.add_picture(str(img_prev), Inches(0.8), Inches(1.5), width=Inches(6.0))

    card_safety = add_card(slide11, Inches(7.1), Inches(1.5), Inches(5.4), Inches(5.3), RGBColor(254, 242, 242), RGBColor(239, 68, 68))
    tb_safe = slide11.shapes.add_textbox(Inches(7.4), Inches(1.7), Inches(4.8), Inches(4.9))
    tf_sf = tb_safe.text_frame
    tf_sf.word_wrap = True

    p = tf_sf.paragraphs[0]
    p.text = "🛑 ระบบหยุดฉุกเฉิน (Kill Switch)"
    p.font.name = FONT_MAIN
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = RGBColor(185, 28, 28)

    safe_points = [
      "หากคลิกผิดช่อง หรือต้องการยกเลิกกะทันหัน",
      "กดปุ่ม ESC บนคีย์บอร์ดได้ทันที ทุกเวลา!",
      "โปรแกรมหยุดทันทีในระดับมิลลิวินาที (<50ms)",
      "ไม่เกิดการพิมพ์ค้างหรือพิมพ์เกิน ปลอดภัย 100%",
      "⏩ ช่องว่าง (เด็กขาดสอบ / ยังไม่มีคะแนน) โปรแกรมจะส่งเฉพาะ Tab เปล่าข้ามไป ไม่กระทบเพื่อนคนอื่น"
    ]
    for sp in safe_points:
        p = tf_sf.add_paragraph()
        p.text = f"• {sp}"
        p.font.name = FONT_MAIN
        p.font.size = Pt(12.5)
        p.font.color.rgb = RGBColor(127, 29, 29)
        p.space_before = Pt(8)

    # =========================================================================
    # SLIDE 12: การตั้งค่าที่ปรับแต่งได้ (Settings)
    # =========================================================================
    slide12 = prs.slides.add_slide(blank_layout)
    add_header(slide12, "การตั้งค่าโปรแกรมโดยละเอียด (Settings Dialog)")

    img_set = IMAGES_DIR / "autosgs_settings.png"
    if img_set.exists():
        slide12.shapes.add_picture(str(img_set), Inches(0.8), Inches(1.5), width=Inches(5.0))

    card_set_info = add_card(slide12, Inches(6.1), Inches(1.5), Inches(6.4), Inches(5.3))
    tb_set_info = slide12.shapes.add_textbox(Inches(6.4), Inches(1.7), Inches(5.8), Inches(4.9))
    tf_si = tb_set_info.text_frame
    tf_si.word_wrap = True

    p = tf_si.paragraphs[0]
    p.text = "⚙️ ปรับแต่งได้ตามความต้องการ"
    p.font.name = FONT_MAIN
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = COLOR_PRIMARY_DARK

    settings_items = [
      ("ปุ่มลัดเริ่มพิมพ์ (Global Hotkey)", "เปลี่ยนเป็น F4, F8 หรือ Ctrl+Alt+V ได้"),
      ("ขนาดตัวอักษรและการแสดงผล", "ปกติ (100%), ใหญ่ (115% แนะนำ), ใหญ่พิเศษ (130%) เหมาะสำหรับสายตาผู้ใหญ่"),
      ("ธีมการแสดงผล", "System (ตามธีม Windows), Dark Mode หรือ Light Mode"),
      ("เสียงแจ้งเตือน", "เปิด/ปิดเสียง Beep นับถอยหลัง และเสียง Chime เมื่อเสร็จ"),
      ("จดจำความเร็วแยกแต่ละโหมด", "จำสปีดของแต่ละโหมดแยกกันอัตโนมัติ ไม่ต้องปรับใหม่ทุกครั้ง")
    ]
    for k, v in settings_items:
        p = tf_si.add_paragraph()
        p.text = f"✔ {k}:"
        p.font.name = FONT_MAIN
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = COLOR_PRIMARY
        p.space_before = Pt(6)

        p_sub = tf_si.add_paragraph()
        p_sub.text = f"    {v}"
        p_sub.font.name = FONT_MAIN
        p_sub.font.size = Pt(11.5)
        p_sub.font.color.rgb = COLOR_TEXT_MUTED

    # =========================================================================
    # SLIDE 13: 5 เทคนิคเพื่อความแม่นยำสูงสุด (Pro Tips)
    # =========================================================================
    slide13 = prs.slides.add_slide(blank_layout)
    add_header(slide13, "5 ข้อควรระวังและเทคนิคเพื่อความแม่นยำ 100%")

    tips = [
      ("1. ตรวจสอบจำนวนแถวเสมอ", "สังเกตกล่องสถานะว่าจำนวนแถวตรงกับจำนวนนักเรียนในห้องหรือไม่ (เช่น 40 แถว)"),
      ("2. ปรับซูมหน้าเว็บ SGS ไว้ที่ 100%", "เพื่อป้องกันไม่ให้ตารางคะแนนตกหล่นหรือเลื่อนผิดช่อง"),
      ("3. ห้ามแตะเมาส์ขณะโปรแกรมกำลังพิมพ์", "ปล่อยมือจากเมาส์และแป้นพิมพ์ รอจนมีเสียงกระดิ่งเตือนว่าเสร็จสิ้น"),
      ("4. เน็ตโรงเรียนช้า ให้ปรับเพิ่ม Delay", "หากหน้าเว็บ SGS ตอบสนองช้า ให้เลื่อนสไลเดอร์ความเร็วเป็น 0.15s – 0.20s"),
      ("5. สามารถแบ่งกรอกทีละครึ่งห้องได้", "ลากคลุมคนที่ 1–20 แล้วสั่งพิมพ์ จากนั้นค่อยคลุมคนที่ 21–40 มาคลิกช่อง 21 แล้วสั่งพิมพ์ต่อ")
    ]

    for idx, (t_title, t_desc) in enumerate(tips):
        top_pos = Inches(1.5 + idx * 1.05)
        card_tip = add_card(slide13, Inches(0.8), top_pos, Inches(11.733), Inches(0.9), RGBColor(255, 255, 255), COLOR_PRIMARY)
        tb_tip = slide13.shapes.add_textbox(Inches(1.1), top_pos + Inches(0.12), Inches(11.1), Inches(0.7))
        p = tb_tip.text_frame.paragraphs[0]
        p.text = f"{t_title}: "
        p.font.name = FONT_MAIN
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = COLOR_PRIMARY_DARK

        p_desc = tb_tip.text_frame.add_paragraph()
        p_desc.text = t_desc
        p_desc.font.name = FONT_MAIN
        p_desc.font.size = Pt(11.5)
        p_desc.font.color.rgb = COLOR_TEXT_MUTED

    # =========================================================================
    # SLIDE 14: คำถามที่พบบ่อย (FAQs & Troubleshooting)
    # =========================================================================
    slide14 = prs.slides.add_slide(blank_layout)
    add_header(slide14, "คำถามที่พบบ่อย (FAQs & Troubleshooting)")

    faqs = [
      ("Q: เปิดโปรแกรมแล้วขึ้น 'Windows protected your PC'?", "คลิก 'More info' (ข้อมูลเพิ่มเติม) แล้วกดปุ่ม 'Run anyway' (เรียกใช้ต่อไป) ปลอดภัย 100%"),
      ("Q: กดปุ่ม F2 แล้วไม่มีการพิมพ์เกิดขึ้น?", "โน้ตบุ๊กบางรุ่นต้องกดปุ่ม Fn + F2 หรือตรวจสอบว่าได้คลิกโฟกัสช่องแรกในเว็บ SGS หรือยัง"),
      ("Q: มีนักเรียนย้ายออก ลาออก หรือติด ร. ต้องทำอย่างไร?", "ใน Excel ให้เว้นเซลล์ว่างไว้ โปรแกรมจะกด Tab ข้ามให้อัตโนมัติ ไม่เลื่อนผิดช่อง"),
      ("Q: ใช้งานบนเครื่อง Mac ได้หรือไม่?", "ได้ครับ โดยต้องไปเปิดสิทธิ์ Accessibility ที่ System Settings > Privacy & Security")
    ]

    for idx, (q, a) in enumerate(faqs):
        top_pos = Inches(1.5 + idx * 1.3)
        add_card(slide14, Inches(0.8), top_pos, Inches(11.733), Inches(1.15), RGBColor(248, 250, 252), RGBColor(203, 213, 225))
        tb_faq = slide14.shapes.add_textbox(Inches(1.1), top_pos + Inches(0.1), Inches(11.1), Inches(0.95))
        
        p = tb_faq.text_frame.paragraphs[0]
        p.text = q
        p.font.name = FONT_MAIN
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = COLOR_PRIMARY_DARK

        p_ans = tb_faq.text_frame.add_paragraph()
        p_ans.text = f"ตอบ: {a}"
        p_ans.font.name = FONT_MAIN
        p_ans.font.size = Pt(12)
        p_ans.font.color.rgb = COLOR_SUCCESS

    # =========================================================================
    # SLIDE 15: สรุปและการดาวน์โหลด (Download & Conclusion)
    # =========================================================================
    slide15 = prs.slides.add_slide(blank_layout)
    add_header(slide15, "สรุปและช่องทางดาวน์โหลดโปรแกรม AutoSGS")

    card_dl = add_card(slide15, Inches(1.5), Inches(1.5), Inches(10.333), Inches(5.3), RGBColor(240, 249, 255), RGBColor(186, 230, 253))
    tb_dl = slide15.shapes.add_textbox(Inches(2.0), Inches(2.0), Inches(9.333), Inches(4.3))
    tf_dl = tb_dl.text_frame
    tf_dl.word_wrap = True

    p = tf_dl.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    p.text = "🎉 ดาวน์โหลดโปรแกรม AutoSGS เวอร์ชันล่าสุดได้ฟรี!"
    p.font.name = FONT_MAIN
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = COLOR_PRIMARY_DARK

    p_body = tf_dl.add_paragraph()
    p_body.alignment = PP_ALIGN.CENTER
    p_body.text = "\n• เป็นไฟล์พกพา (Portable .exe) ดับเบิลคลิกเปิดใช้ได้ทันที ไม่ต้องติดตั้งโปรแกรม\n• รองรับทั้ง Windows 10/11 และ macOS\n• โครงการโอเพนซอร์สเพื่อสนับสนุนการศึกษาไทย\n\n🔗 GitHub Release: https://github.com/NOGiTTiS/AutoSGS"
    p_body.font.name = FONT_MAIN
    p_body.font.size = Pt(14)
    p_body.font.color.rgb = COLOR_TEXT_DARK

    p_end = tf_dl.add_paragraph()
    p_end.alignment = PP_ALIGN.CENTER
    p_end.text = "\nขอให้คุณครูทุกท่านมีความสุขและสะดวกสบายกับการบันทึกคะแนนในทุกสิ้นภาคเรียนครับ ❤️"
    p_end.font.name = FONT_MAIN
    p_end.font.size = Pt(13)
    p_end.font.bold = True
    p_end.font.color.rgb = COLOR_ACCENT

    prs.save(str(OUTPUT_PPTX))
    print(f"[DONE] Successfully generated PPTX: {OUTPUT_PPTX}")

if __name__ == "__main__":
    build_pptx()
