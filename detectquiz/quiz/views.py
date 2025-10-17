from django.shortcuts import render, redirect
import requests
import json
from datetime import datetime
from django.contrib.auth.decorators import login_required
from .models import Subject, Test, StudentTestScore
from .forms import SubjectForm, TestForm, StudentTestScoreForm

@login_required
def teacher_dashboard(request):
    subjects = Subject.objects.filter(teacher=request.user)
    return render(request, 'quiz/teacher_dashboard.html', {'subjects': subjects})

@login_required
def student_dashboard(request):
    scores = StudentTestScore.objects.filter(student=request.user)
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

@login_required
def score_realtime(request):
    api_url = "http://127.0.0.1:8001/getExamResults"
    processed = []

    try:
        resp = requests.get(api_url, timeout=5)
        resp.raise_for_status()
        raw = resp.json()  # คาดว่าเป็น list ของ dict
    except requests.RequestException as e:
        raw = []
        print("API request failed:", e)

    for item in raw:
        # copy to avoid mutating original
        row = dict(item)

        # 1) แปลง exam_detail (ถ้าเป็น JSON string)
        ed = row.get("exam_detail")
        parsed = None
        if ed:
            if isinstance(ed, str):
                try:
                    parsed = json.loads(ed)
                except json.JSONDecodeError:
                    # ถ้าเก็บเป็น string แบบ escape หรือ single quotes -> พยายามแก้
                    try:
                        parsed = json.loads(ed.replace("'", '"'))
                    except Exception:
                        parsed = {"raw": ed}
            elif isinstance(ed, dict):
                parsed = ed
            else:
                parsed = {"raw": ed}
        row["exam_detail_parsed"] = parsed  # dict or None
        row["exam_detail_json"] = json.dumps(parsed, ensure_ascii=False, indent=2) if parsed else ""

        # 2) format created_at ให้สวย (รองรับแบบ "YYYY-MM-DD HH:MM:SS(.micro)")
        created = row.get("created_at")
        if created:
            try:
                # ถ้าเป็น string
                if isinstance(created, str):
                    try:
                        dt = datetime.strptime(created, "%Y-%m-%d %H:%M:%S.%f")
                    except ValueError:
                        try:
                            dt = datetime.strptime(created, "%Y-%m-%d %H:%M:%S")
                        except ValueError:
                            dt = None
                    row["created_at_fmt"] = dt.strftime("%d %b %Y %H:%M:%S") if dt else created
                else:
                    # ถ้าเป็น datetime object
                    row["created_at_fmt"] = created.strftime("%d %b %Y %H:%M:%S")
            except Exception:
                row["created_at_fmt"] = str(created)
        else:
            row["created_at_fmt"] = "-"

        # 3) ensure lists are accessible (correct_list/wrong_list)
        for k in ("correct_list", "wrong_list"):
            v = row.get(k)
            if v is None:
                row[k + "_list"] = []
            else:
                if isinstance(v, str):
                    # แยก comma
                    row[k + "_list"] = [x.strip() for x in v.split(",") if x.strip()]
                elif isinstance(v, list):
                    row[k + "_list"] = v
                else:
                    row[k + "_list"] = [str(v)]

        processed.append(row)

    return render(request, "quiz/scorerealtime.html", {"exam_results": processed})