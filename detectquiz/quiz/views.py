from django.shortcuts import render, redirect
import requests
import json
from datetime import datetime
from django.contrib.auth.decorators import login_required
from .models import Subject, Test, StudentTestScore
from .forms import SubjectForm, TestForm, StudentTestScoreForm
from collections import namedtuple
@login_required
def teacher_dashboard(request):
    subjects = Subject.objects.filter(teacher=request.user)
    return render(request, 'quiz/teacher_dashboard.html', {'subjects': subjects})

# @login_required
# def student_dashboard(request):
#     scores = StudentTestScore.objects.filter(student=request.user)
#     return render(request, 'quiz/student_dashboard.html', {'scores': scores})
StudentTestScoreMock = namedtuple('StudentTestScoreMock', [
    'test', 'score', 'behavior_score', 'midterm_score', 'final_score', 'assignment_score'
])
TestMock = namedtuple('TestMock', ['title'])

@login_required
def student_dashboard(request):
    # สร้าง mock data 5 ชุด
    scores = [
        StudentTestScoreMock(
            test=TestMock(title="แบบทดสอบคณิตศาสตร์ 1"),
            score=85,
            behavior_score=9,
            midterm_score=40,
            final_score=35,
            assignment_score=10
        ),
        StudentTestScoreMock(
            test=TestMock(title="แบบทดสอบวิทยาศาสตร์ 1"),
            score=78,
            behavior_score=8,
            midterm_score=30,
            final_score=40,
            assignment_score=8
        ),
        StudentTestScoreMock(
            test=TestMock(title="แบบทดสอบภาษาอังกฤษ 1"),
            score=92,
            behavior_score=10,
            midterm_score=45,
            final_score=40,
            assignment_score=7
        ),
        StudentTestScoreMock(
            test=TestMock(title="แบบทดสอบประวัติศาสตร์ 1"),
            score=88,
            behavior_score=9,
            midterm_score=38,
            final_score=40,
            assignment_score=10
        ),
        StudentTestScoreMock(
            test=TestMock(title="แบบทดสอบภูมิศาสตร์ 1"),
            score=80,
            behavior_score=7,
            midterm_score=35,
            final_score=38,
            assignment_score=7
        ),
    ]

    return render(request, 'quiz/student_dashboard.html', {'scores': scores})
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


