from django.shortcuts import render, redirect, get_object_or_404
import requests
import json
from datetime import datetime
from django.contrib.auth.decorators import login_required
from .models import Subject, Test, StudentTestScore,StudentInfo 
from accounts.models import StudentProfile 
from .forms import SubjectForm, TestForm, StudentTestScoreForm,StudentForm, ExcelUploadForm
import pandas as pd
from django.contrib import messages
from collections import namedtuple
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.mail import send_mail
from django.utils.safestring import mark_safe


@login_required
def teacher_dashboard(request):
    subjects = Subject.objects.filter(teacher=request.user)
    return render(request, 'quiz/teacher_dashboard.html', {'subjects': subjects})


StudentTestScoreMock = namedtuple('StudentTestScoreMock', [
    'test', 'score', 'behavior_score', 'midterm_score', 'final_score', 'assignment_score'
])
TestMock = namedtuple('TestMock', ['title'])

@login_required
def student_dashboard(request):
    try:
        student_info = StudentInfo.objects.get(student_id=request.user.username)
    except StudentInfo.DoesNotExist:
        student_info = None
    scores = StudentTestScore.objects.filter(student=request.user).select_related('test', 'test__subject')

    return render(request, 'quiz/student_dashboard.html', {
        'student_info': student_info,
        'scores': scores,
    })


@login_required
def create_subject(request):
    if request.method == "POST":
        form = SubjectForm(request.POST)
        if form.is_valid():
            subject = form.save(commit=False)
            subject.teacher = request.user
            subject.save()
            return redirect('teacher_dashboard')
    else:
        form = SubjectForm()

    return render(request, 'quiz/create_subject.html', {'form': form})

@login_required
def create_test(request):
    if request.method == "POST":
        form = TestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('teacher_dashboard')
    else:
        form = TestForm()
    return render(request, 'quiz/create_test.html', {'form': form})

@login_required
def enter_scores(request):
    if request.method == "POST":
        form = StudentTestScoreForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('teacher_dashboard')
    else:
        form = StudentTestScoreForm()
    return render(request, 'quiz/enter_scores.html', {'form': form})

@login_required
def result(request):
    scores = StudentTestScore.objects.select_related('student', 'test').all().order_by('student__username')
    return render(request, 'quiz/result.html', {'scores': scores})


User = get_user_model()
@login_required
def student_score_chart(request, student_id):
    student_scores = StudentTestScore.objects.filter(student__id=student_id)

    labels = [score.test.title for score in student_scores]
    scores = [score.score or 0 for score in student_scores]
    behavior_scores = [score.behavior_score or 0 for score in student_scores]
    midterm_scores = [score.midterm_score or 0 for score in student_scores]
    final_scores = [score.final_score or 0 for score in student_scores]
    assignment_scores = [score.assignment_score or 0 for score in student_scores]

    context = {
        "student": student_scores.first().student if student_scores.exists() else None,
        "labels": mark_safe(json.dumps(labels)),
        "scores": mark_safe(json.dumps(scores)),
        "behavior_scores": mark_safe(json.dumps(behavior_scores)),
        "midterm_scores": mark_safe(json.dumps(midterm_scores)),
        "final_scores": mark_safe(json.dumps(final_scores)),
        "assignment_scores": mark_safe(json.dumps(assignment_scores)),
    }

    return render(request, 'quiz/student_score_chart.html', context)

@login_required
def addstudent(request):
    if request.method == 'POST':
        if 'upload_excel' in request.POST:
            excel_form = ExcelUploadForm(request.POST, request.FILES)
            if excel_form.is_valid():
                file = excel_form.cleaned_data['file']
                try:
                    df = pd.read_excel(file)
                    for _, row in df.iterrows():
                        StudentInfo.objects.update_or_create(
                            student_id=row['student_id'],
                            defaults={
                                'first_name': row.get('first_name', ''),
                                'last_name': row.get('last_name', ''),
                                'grade_level': row.get('grade_level', ''),
                                'classroom': row.get('classroom', ''),
                                'phone_number': row.get('phone_number', ''),
                                'email': row.get('email', ''),
                                'guardian_name': row.get('guardian_name', ''),
                                'guardian_email': row.get('guardian_email', ''),
                            }
                        )
                    messages.success(request, "อัปโหลด Excel สำเร็จ!")
                    return redirect('teacher_dashboard')
                except Exception as e:
                    messages.error(request, f"เกิดข้อผิดพลาด: {str(e)}")
        else:
            form = StudentForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "บันทึกข้อมูลนักเรียนเรียบร้อย")
                return redirect('teacher_dashboard')
    else:
        form = StudentForm()
        excel_form = ExcelUploadForm()
    
    context = {
        'form': form,
        'excel_form': excel_form
    }
    return render(request, 'quiz/add_student.html', context)


from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import StudentInfo, StudentTestScore

@login_required
def parentreport(request):
    selected_grade = request.GET.get('grade', '')
    grade_levels = StudentInfo.objects.values_list('grade_level', flat=True).distinct()
    if selected_grade:
        students = StudentInfo.objects.filter(grade_level=selected_grade)
    else:
        students = StudentInfo.objects.all()

    student_data = []
    for s in students:
        scores = StudentTestScore.objects.filter(student__username=s.student_id)
        if scores.exists():
            avg_score = sum([sc.score or 0 for sc in scores]) / len(scores)
        else:
            avg_score = 0

        student_data.append({
            'student_id': s.student_id,
            'student_name': f"{s.first_name} {s.last_name}",
            'grade_level': s.grade_level,
            'classroom': s.classroom,
            'guardian_name': s.guardian_name,
            'guardian_email': s.guardian_email,
            'average_score': round(avg_score, 2)
        })

    return render(request, 'quiz/parentreport.html', {
        'students': student_data,
        'grade_levels': grade_levels,
        'selected_grade': selected_grade,
    })


def send_parent_notification(email, student_name, score):
    subject = f"แจ้งคะแนนของ {student_name}"
    message = f"เรียนผู้ปกครอง\n\nคะแนนของ {student_name} คือ {score}\n\nขอบคุณครับ"
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])

# @login_required
# def score_realtime(request):
#     api_url = "http://127.0.0.1:8001/getExamResults"
#     processed = []

#     try:
#         resp = requests.get(api_url, timeout=5)
#         resp.raise_for_status()
#         raw = resp.json()  # คาดว่าเป็น list ของ dict
#     except requests.RequestException as e:
#         raw = []
#         print("API request failed:", e)

#     for item in raw:
#         # copy to avoid mutating original
#         row = dict(item)

#         # 1) แปลง exam_detail (ถ้าเป็น JSON string)
#         ed = row.get("exam_detail")
#         parsed = None
#         if ed:
#             if isinstance(ed, str):
#                 try:
#                     parsed = json.loads(ed)
#                 except json.JSONDecodeError:
#                     # ถ้าเก็บเป็น string แบบ escape หรือ single quotes -> พยายามแก้
#                     try:
#                         parsed = json.loads(ed.replace("'", '"'))
#                     except Exception:
#                         parsed = {"raw": ed}
#             elif isinstance(ed, dict):
#                 parsed = ed
#             else:
#                 parsed = {"raw": ed}
#         row["exam_detail_parsed"] = parsed  # dict or None
#         row["exam_detail_json"] = json.dumps(parsed, ensure_ascii=False, indent=2) if parsed else ""

#         # 2) format created_at ให้สวย (รองรับแบบ "YYYY-MM-DD HH:MM:SS(.micro)")
#         created = row.get("created_at")
#         if created:
#             try:
#                 # ถ้าเป็น string
#                 if isinstance(created, str):
#                     try:
#                         dt = datetime.strptime(created, "%Y-%m-%d %H:%M:%S.%f")
#                     except ValueError:
#                         try:
#                             dt = datetime.strptime(created, "%Y-%m-%d %H:%M:%S")
#                         except ValueError:
#                             dt = None
#                     row["created_at_fmt"] = dt.strftime("%d %b %Y %H:%M:%S") if dt else created
#                 else:
#                     # ถ้าเป็น datetime object
#                     row["created_at_fmt"] = created.strftime("%d %b %Y %H:%M:%S")
#             except Exception:
#                 row["created_at_fmt"] = str(created)
#         else:
#             row["created_at_fmt"] = "-"

#         # 3) ensure lists are accessible (correct_list/wrong_list)
#         for k in ("correct_list", "wrong_list"):
#             v = row.get(k)
#             if v is None:
#                 row[k + "_list"] = []
#             else:
#                 if isinstance(v, str):
#                     # แยก comma
#                     row[k + "_list"] = [x.strip() for x in v.split(",") if x.strip()]
#                 elif isinstance(v, list):
#                     row[k + "_list"] = v
#                 else:
#                     row[k + "_list"] = [str(v)]

#         processed.append(row)

#     return render(request, "quiz/scorerealtime.html", {"exam_results": processed})
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import json
from datetime import datetime
import requests

@login_required
def score_realtime(request):
    api_url = "http://127.0.0.1:8001/getExamResults"
    processed = []

    # ===== MOCK DATA SECTION =====
    # ใช้ข้อมูลจำลอง 5 ชุดในกรณีที่ API ใช้งานไม่ได้
    mock_data = [
        {
            "id": 1,
            "full_name": "ทดสอบ ระบบ1",
            "student_number": "001",
            "exam_topic": "บทที่ 1 การวัดผล",
            "exam_name": "แบบทดสอบก่อนเรียน",
            "score": 85.0,
            "correct_count": 17,
            "wrong_count": 3,
            "exam_detail": json.dumps({
                "Q1": True, "Q2": True, "Q3": True, "Q4": False, "Q5": True,
                "Q6": True, "Q7": True, "Q8": True, "Q9": True, "Q10": False,
                "Q11": True, "Q12": True, "Q13": True, "Q14": True, "Q15": True,
                "Q16": True, "Q17": False, "Q18": True, "Q19": True, "Q20": True
            }),
            "created_at": "2025-10-17 09:30:00"
        },
        {
            "id": 2,
            "full_name": "ทดสอบ ระบบ2",
            "student_number": "002",
            "exam_topic": "บทที่ 1 การวัดผล",
            "exam_name": "แบบทดสอบก่อนเรียน",
            "score": 72.5,
            "correct_count": 15,
            "wrong_count": 5,
            "exam_detail": json.dumps({
                "Q1": True, "Q2": False, "Q3": True, "Q4": True, "Q5": True,
                "Q6": False, "Q7": True, "Q8": True, "Q9": True, "Q10": True,
                "Q11": True, "Q12": False, "Q13": True, "Q14": True, "Q15": True,
                "Q16": True, "Q17": True, "Q18": False, "Q19": True, "Q20": True
            }),
            "created_at": "2025-10-17 09:31:00"
        },
        {
            "id": 3,
            "full_name": "ทดสอบ ระบบ3",
            "student_number": "003",
            "exam_topic": "บทที่ 1 การวัดผล",
            "exam_name": "แบบทดสอบก่อนเรียน",
            "score": 48.0,
            "correct_count": 10,
            "wrong_count": 10,
            "exam_detail": json.dumps({
                "Q1": False, "Q2": True, "Q3": False, "Q4": True, "Q5": True,
                "Q6": False, "Q7": True, "Q8": False, "Q9": True, "Q10": False,
                "Q11": True, "Q12": False, "Q13": False, "Q14": True, "Q15": True,
                "Q16": False, "Q17": False, "Q18": True, "Q19": True, "Q20": False
            }),
            "created_at": "2025-10-17 09:33:00"
        },
        {
            "id": 4,
            "full_name": "ทดสอบ ระบบ4",
            "student_number": "004",
            "exam_topic": "บทที่ 2 การประเมินผล",
            "exam_name": "แบบทดสอบหลังเรียน",
            "score": 91.0,
            "correct_count": 18,
            "wrong_count": 2,
            "exam_detail": json.dumps({
                "Q1": True, "Q2": True, "Q3": True, "Q4": True, "Q5": True,
                "Q6": True, "Q7": False, "Q8": True, "Q9": True, "Q10": True,
                "Q11": True, "Q12": True, "Q13": True, "Q14": True, "Q15": True,
                "Q16": True, "Q17": True, "Q18": True, "Q19": True, "Q20": False
            }),
            "created_at": "2025-10-17 09:35:00"
        },
        {
            "id": 5,
            "full_name": "ทดสอบ ระบบ5",
            "student_number": "005",
            "exam_topic": "บทที่ 2 การประเมินผล",
            "exam_name": "แบบทดสอบหลังเรียน",
            "score": 65.0,
            "correct_count": 13,
            "wrong_count": 7,
            "exam_detail": json.dumps({
                "Q1": True, "Q2": True, "Q3": False, "Q4": False, "Q5": True,
                "Q6": True, "Q7": True, "Q8": True, "Q9": False, "Q10": True,
                "Q11": True, "Q12": False, "Q13": True, "Q14": False, "Q15": True,
                "Q16": True, "Q17": True, "Q18": True, "Q19": False, "Q20": False
            }),
            "created_at": "2025-10-17 09:37:00"
        },
    ]
    # ===== END MOCK DATA SECTION =====

    try:
        resp = requests.get(api_url, timeout=5)
        resp.raise_for_status()
        raw = resp.json()
        if not isinstance(raw, list) or len(raw) == 0:
            raw = mock_data  # ใช้ mock ถ้า API ไม่มีข้อมูล
    except requests.RequestException as e:
        print("API request failed:", e)
        raw = mock_data  # ถ้า API ล่ม → ใช้ mock data แทน

    # ===== PROCESSING SECTION =====
    for item in raw:
        row = dict(item)
        ed = row.get("exam_detail")
        parsed = None
        if ed:
            if isinstance(ed, str):
                try:
                    parsed = json.loads(ed)
                except Exception:
                    parsed = {"raw": ed}
            elif isinstance(ed, dict):
                parsed = ed
        row["exam_detail_parsed"] = parsed
        row["exam_detail_json"] = json.dumps(parsed, ensure_ascii=False, indent=2) if parsed else ""

        created = row.get("created_at")
        if created:
            try:
                dt = datetime.strptime(created, "%Y-%m-%d %H:%M:%S")
                row["created_at_fmt"] = dt.strftime("%d %b %Y %H:%M:%S")
            except Exception:
                row["created_at_fmt"] = str(created)
        else:
            row["created_at_fmt"] = "-"

        processed.append(row)

    return render(request, "quiz/scorerealtime.html", {"exam_results": processed})


