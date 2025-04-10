from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime
import json
import os
from tamil_utils import unicode_to_bamini

# Register Tamil font
tamil_font_path = os.path.join(os.path.dirname(__file__), 'static', 'fonts', 'Bamini.ttf')
if os.path.exists(tamil_font_path):
    pdfmetrics.registerFont(TTFont('Bamini', tamil_font_path))

def create_paragraph_with_style(text, style, is_tamil=False):
    if is_tamil and os.path.exists(tamil_font_path):
        style.fontName = 'Bamini'
        # Convert Unicode Tamil to Bamini encoding
        text = unicode_to_bamini(text)
    
    # Remove all special characters and emojis
    import re
    # Remove emojis and special characters
    text = re.sub(r'[^\w\s\u0B80-\u0BFF.,!?;:()\n]', '', text)
    # Remove multiple spaces
    text = re.sub(r'\s+', ' ', text)
    # Remove multiple newlines
    text = re.sub(r'\n+', '\n', text)
    
    return Paragraph(text, style)

def generate_pdf(analysis_results, petition_text, output_path):
    # Create the PDF document
    doc = SimpleDocTemplate(
        output_path,
        pagesize=landscape(letter),
        rightMargin=30,
        leftMargin=30,
        topMargin=30,
        bottomMargin=30
    )

    # Create the story (content) for the PDF
    story = []

    # Add styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=20,
        spaceAfter=30,
        alignment=1,
        fontName='Helvetica-Bold'
    )
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=20,
        alignment=1,
        fontName='Helvetica'
    )
    normal_style = ParagraphStyle(
        'Normal',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        fontName='Helvetica'
    )
    cell_style = ParagraphStyle(
        'CellStyle',
        parent=styles['Normal'],
        fontSize=9,
        leading=12,
        wordWrap='CJK',
        fontName='Helvetica'
    )
    tamil_style = ParagraphStyle(
        'TamilStyle',
        parent=styles['Normal'],
        fontSize=11,  # Increased font size for better readability
        leading=14,
        wordWrap='CJK',
        fontName='Bamini' if os.path.exists(tamil_font_path) else 'Helvetica'
    )

    # Add title
    story.append(Paragraph("PETITION HUB ANALYSIS REPORT", title_style))
    story.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", subtitle_style))
    story.append(Spacer(1, 20))

    # Add petition text section
    story.append(Paragraph("PETITION TEXT", subtitle_style))
    story.append(create_paragraph_with_style(petition_text, normal_style))
    story.append(Spacer(1, 20))
    story.append(PageBreak())

    # Add analysis results section
    story.append(Paragraph("ANALYSIS RESULTS", subtitle_style))
    story.append(Spacer(1, 10))

    # Convert analysis results to table data with wrapped text
    table_data = [
        [Paragraph(header, cell_style) for header in [
            'Section', 'Department', 'Description (English)', 'Description (Tamil)',
            'Suggestions (English)', 'Suggestions (Tamil)', 'Priority'
        ]]
    ]

    for result in analysis_results:
        row = [
            create_paragraph_with_style(result['section'], cell_style),
            create_paragraph_with_style(result['department'], cell_style),
            create_paragraph_with_style(result['desc_eng'], cell_style),
            create_paragraph_with_style(result['desc_tam'], tamil_style, True),
            create_paragraph_with_style(result['sug_eng'], cell_style),
            create_paragraph_with_style(result['sug_tam'], tamil_style, True),
            create_paragraph_with_style(result['priority'], cell_style)
        ]
        table_data.append(row)

    # Create the table with adjusted column widths
    page_width = letter[0]  # In landscape mode, letter[0] is the height which becomes the width
    table_width = 0.9 * page_width  # 90% of page width
    
    # Calculate proportional widths (total = 100)
    width_ratios = {
        'section': 8,      # 8%
        'department': 12,  # 12%
        'desc_eng': 20,    # 20%
        'desc_tam': 20,    # 20%
        'sug_eng': 20,     # 20%
        'sug_tam': 20,     # 20%
        'priority': 8      # 8%
    }
    
    # Convert percentages to actual widths
    col_widths = [
        width_ratios['section'] * table_width / 100,
        width_ratios['department'] * table_width / 100,
        width_ratios['desc_eng'] * table_width / 100,
        width_ratios['desc_tam'] * table_width / 100,
        width_ratios['sug_eng'] * table_width / 100,
        width_ratios['sug_tam'] * table_width / 100,
        width_ratios['priority'] * table_width / 100
    ]
    
    table = Table(table_data, colWidths=col_widths, repeatRows=1)
    
    # Apply table styles with adjusted spacing
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4b6cb7')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),  # Reduced padding
        ('RIGHTPADDING', (0, 0), (-1, -1), 4), # Reduced padding
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))

    story.append(table)
    story.append(Spacer(1, 20))

    # Add footer
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        alignment=1
    )
    story.append(Paragraph("Generated by Petition Hub - Legal Analysis System", footer_style))

    # Build the PDF
    doc.build(story) 