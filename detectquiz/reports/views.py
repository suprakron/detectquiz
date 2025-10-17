from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime

# Mockup classes
class TestMock:
    def __init__(self, title):
        self.title = title

class StudentTestScoreMock:
    def __init__(self, test, score, behavior_score, midterm_score, final_score, assignment_score):
        self.test = test
        self.score = score
        self.behavior_score = behavior_score
        self.midterm_score = midterm_score
        self.final_score = final_score
        self.assignment_score = assignment_score

@login_required
def download_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="score_report.pdf"'

    # Clean mockup data
    scores = [
        StudentTestScoreMock(TestMock("แบบทดสอบคณิตศาสตร์ 1"), 85, 9, 40, 35, 10),
        StudentTestScoreMock(TestMock("แบบทดสอบวิทยาศาสตร์ 1"), 78, 8, 30, 40, 8),
        StudentTestScoreMock(TestMock("แบบทดสอบภาษาอังกฤษ 1"), 92, 10, 45, 40, 7),
        StudentTestScoreMock(TestMock("แบบทดสอบประวัติศาสตร์ 1"), 88, 9, 38, 40, 10),
        StudentTestScoreMock(TestMock("แบบทดสอบภูมิศาสตร์ 1"), 80, 7, 35, 38, 7),
    ]

    doc = SimpleDocTemplate(response, pagesize=landscape(A4), rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=18)
    elements = []

    styles = getSampleStyleSheet()
    elements.append(Paragraph(f"รายงานคะแนนของ {request.user.username}", styles['Title']))
    elements.append(Spacer(1, 12))
    now = datetime.now().strftime("%d/%m/%Y %H:%M")
    elements.append(Paragraph(f"วันที่สร้างรายงาน: {now}", styles['Normal']))
    elements.append(Spacer(1, 12))

    # Table header + data
    data = [["ชื่อข้อสอบ", "คะแนนข้อสอบ", "พฤติกรรม", "กลางภาค", "ปลายภาค", "คะแนนเก็บ"]]
    for score in scores:
        data.append([
            score.test.title,
            str(score.score),
            str(score.behavior_score),
            str(score.midterm_score),
            str(score.final_score),
            str(score.assignment_score)
        ])

    col_widths = [200, 80, 80, 80, 80, 80]
    table = Table(data, colWidths=col_widths, hAlign='CENTER')

    # Table style
    style = TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#5DADE2')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 12),
        ('BOTTOMPADDING', (0,0), (-1,0), 8),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
    ])
    for i in range(1, len(data)):
        bg_color = colors.HexColor('#D6EAF8') if i % 2 == 0 else colors.white
        style.add('BACKGROUND', (0,i), (-1,i), bg_color)

    table.setStyle(style)
    elements.append(table)

    doc.build(elements)
    return response
