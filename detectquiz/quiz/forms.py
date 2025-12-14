import os
from django import forms
from .models import Subject, Test, StudentTestScore, StudentInfo, AnswerExam, User
from accounts.models import TeacherProfile


# =========================
# Subject
# =========================
class SubjectForm(forms.ModelForm):
    grade_level = forms.ChoiceField(label="ระดับชั้น", choices=[], required=False)
    classroom = forms.ChoiceField(label="ห้อง", choices=[], required=False)
    new_grade_level = forms.CharField(label="เพิ่มระดับชั้น", max_length=50, required=False)
    new_classroom = forms.CharField(label="เพิ่มห้อง", max_length=50, required=False)

    class Meta:
        model = Subject
        fields = [
            "name",
            "grade_level",
            "classroom",
            "new_grade_level",
            "new_classroom",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "ชื่อรายวิชา"}),
            "grade_level": forms.Select(attrs={"class": "form-select"}),
            "classroom": forms.Select(attrs={"class": "form-select"}),
            "new_grade_level": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "เพิ่มระดับชั้นใหม่"}
            ),
            "new_classroom": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "เพิ่มห้องใหม่"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        grade_levels = StudentInfo.objects.values_list("grade_level", flat=True).distinct()
        classrooms = StudentInfo.objects.values_list("classroom", flat=True).distinct()

        self.fields["grade_level"].choices = [("", "เลือกระดับชั้น")] + [(g, g) for g in grade_levels]
        self.fields["classroom"].choices = [("", "เลือกห้อง")] + [(c, c) for c in classrooms]


# =========================
# Test
# =========================
class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ["subject", "title", "full_score"]
        widgets = {
            "subject": forms.Select(attrs={"class": "form-select"}),
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "ชื่อแบบทดสอบ"}),
            "full_score": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "คะแนนเต็ม", "min": 0}
            ),
        }
        labels = {
            "subject": "รายวิชา",
            "title": "ชื่อแบบทดสอบ",
            "full_score": "คะแนนเต็ม",
        }


# =========================
# Student Test Score
# =========================
class StudentTestScoreForm(forms.ModelForm):
    class Meta:
        model = StudentTestScore
        fields = [
            "student",
            "test",
            "score",
            "behavior_score",
            "midterm_score",
            "final_score",
            "assignment_score",
        ]
        widgets = {
            "student": forms.Select(attrs={"class": "form-select"}),
            "test": forms.Select(attrs={"class": "form-select"}),
            "score": forms.NumberInput(attrs={"class": "form-control"}),
            "behavior_score": forms.NumberInput(attrs={"class": "form-control"}),
            "midterm_score": forms.NumberInput(attrs={"class": "form-control"}),
            "final_score": forms.NumberInput(attrs={"class": "form-control"}),
            "assignment_score": forms.NumberInput(attrs={"class": "form-control"}),
        }


# =========================
# Student
# =========================
class StudentForm(forms.ModelForm):
    class Meta:
        model = StudentInfo
        fields = [
            "student_id",
            "first_name",
            "last_name",
            "grade_level",
            "classroom",
            "phone_number",
            "email",
            "guardian_name",
            "guardian_email",
        ]
        widgets = {
            "student_id": forms.TextInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "grade_level": forms.TextInput(attrs={"class": "form-control"}),
            "classroom": forms.TextInput(attrs={"class": "form-control"}),
            "phone_number": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "guardian_name": forms.TextInput(attrs={"class": "form-control"}),
            "guardian_email": forms.EmailInput(attrs={"class": "form-control"}),
        }


# =========================
# Excel Upload
# =========================
class ExcelUploadForm(forms.Form):
    file = forms.FileField(
        label="อัปโหลดไฟล์ Excel",
        widget=forms.ClearableFileInput(attrs={"class": "form-control"}),
    )


# =========================
# Answer Exam (สำคัญ)
# =========================
class AnswerExamForm(forms.ModelForm):
    upload_file = forms.FileField(
        required=False,
        label="อัปโหลดไฟล์เฉลย (Excel / PDF / JPG / PNG)",
        widget=forms.ClearableFileInput(
            attrs={
                "class": "form-control",
                "accept": ".xlsx,.xls,.pdf,.jpg,.jpeg,.png",
            }
        ),
    )

    answer_key_raw = forms.CharField(
        required=False,
        label="เฉลย (รูปแบบ 1:A,2:B,3:C)",
        widget=forms.Textarea(
            attrs={"rows": 6, "class": "form-control", "placeholder": "1:A,2:B,3:C"}
        ),
    )

    class Meta:
        model = AnswerExam
        fields = [
            "subject_code",
            "subject_name",
            "test_name",
            "full_score",
            "teacher_name",
            "exam_date",
            "upload_file",
        ]
        widgets = {
            "subject_code": forms.TextInput(attrs={"class": "form-control"}),
            "subject_name": forms.TextInput(attrs={"class": "form-control"}),
            "test_name": forms.TextInput(attrs={"class": "form-control"}),
            "full_score": forms.NumberInput(attrs={"class": "form-control"}),
            "teacher_name": forms.TextInput(attrs={"class": "form-control"}),
            "exam_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
        }

    # ✅ clean ต้องอยู่ตรงนี้
    def clean(self):
        cleaned_data = super().clean()

        upload_file = cleaned_data.get("upload_file")
        raw = cleaned_data.get("answer_key_raw", "").strip()

        # ตรวจเฉลยที่พิมพ์เอง
        if raw:
            try:
                answer_dict = {}
                for pair in raw.split(","):
                    k, v = pair.split(":")
                    answer_dict[k.strip()] = v.strip().upper()
                cleaned_data["answer_key"] = answer_dict
            except Exception:
                raise forms.ValidationError({
                    "answer_key_raw": "รูปแบบเฉลยไม่ถูกต้อง ควรเป็น 1:A,2:B,3:C"
                })

        # ตรวจชนิดไฟล์
        if upload_file:
            ext = os.path.splitext(upload_file.name)[1].lower()
            allowed_ext = [".xlsx", ".xls", ".pdf", ".jpg", ".jpeg", ".png"]

            if ext not in allowed_ext:
                raise forms.ValidationError({
                    "upload_file": "รองรับเฉพาะ Excel, PDF, JPG, PNG"
                })

class UploadFileForm(forms.Form):
    upload_file = forms.FileField(label='อัปโหลดไฟล์')