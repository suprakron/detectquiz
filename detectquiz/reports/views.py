from django.http import HttpResponse
from reportlab.pdfgen import canvas
from quiz.models import StudentTestScore
from django.contrib.auth.decorators import login_required

@login_required
def download_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="score_report.pdf"'

    p = canvas.Canvas(response)
    scores = StudentTestScore.objects.filter(student=request.user)
    y = 800
    p.setFont("Helvetica-Bold", 14)
    p.drawString(100, y, f"รายงานคะแนนของ {request.user.username}")
    y -= 30
    p.setFont("Helvetica", 12)
    for score in scores:
        line = f"{score.test.title}: ข้อสอบ {score.score}, พฤติกรรม {score.behavior_score}, " \
               f"กลางภาค {score.midterm_score}, ปลายภาค {score.final_score}, เก็บ {score.assignment_score}"
        p.drawString(50, y, line)
        y -= 20
    p.showPage()
    p.save()
    return response
