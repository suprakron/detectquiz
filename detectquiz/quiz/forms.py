from django import forms
from .models import Subject, Test, StudentTestScore,StudentInfo

# class SubjectForm(forms.ModelForm):
#     class Meta:
#         model = Subject
#         fields = ['name', 'grade_level']

# forms.py
class SubjectForm(forms.ModelForm):
    grade_level = forms.ChoiceField(label="ระดับชั้น", choices=[])
    classroom = forms.ChoiceField(label="ห้อง", choices=[])

    class Meta:
        model = Subject
        fields = ['name', 'grade_level', 'classroom']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ชื่อรายวิชา'}),
            'grade_level': forms.Select(attrs={'class': 'form-select'}),
            'classroom': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        grade_levels = StudentInfo.objects.values_list('grade_level', flat=True).distinct()
        classrooms = StudentInfo.objects.values_list('classroom', flat=True).distinct()
        self.fields['grade_level'].choices = [('', 'เลือกระดับชั้น')] + [(g, g) for g in grade_levels]
        self.fields['classroom'].choices = [('', 'เลือกห้อง')] + [(c, c) for c in classrooms]





# class TestForm(forms.ModelForm):
#     class Meta:
#         model = Test
#         fields = ['subject', 'title', 'full_score']
class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ['subject', 'title', 'full_score']
        widgets = {
            'subject': forms.Select(attrs={
                'class': 'form-select',
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ชื่อแบบทดสอบ',
            }),
            'full_score': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'คะแนนเต็ม',
                'min': 0,
            }),
        }
        labels = {
            'subject': 'รายวิชา',
            'title': 'ชื่อแบบทดสอบ',
            'full_score': 'คะแนนเต็ม',
        }


class StudentTestScoreForm(forms.ModelForm):
    class Meta:
        model = StudentTestScore
        fields = [
            'student', 'test', 'score',
            'behavior_score', 'midterm_score',
            'final_score', 'assignment_score'
        ]
        widgets = {
            'student': forms.Select(attrs={'class': 'form-select'}),
            'test': forms.Select(attrs={'class': 'form-select'}),
            'score': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'คะแนนกลางภาค'}),
            'behavior_score': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'คะแนนพฤติกรรม'}),
            'midterm_score': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'คะแนนกลางภาค'}),
            'final_score': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'คะแนนปลายภาค'}),
            'assignment_score': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'คะแนนการบ้าน'}),
        }
        labels = {
            'student': 'นักเรียน',
            'test': 'แบบทดสอบ',
            'score': 'คะแนนรวม',
            'behavior_score': 'คะแนนพฤติกรรม',
            'midterm_score': 'คะแนนกลางภาค',
            'final_score': 'คะแนนปลายภาค',
            'assignment_score': 'คะแนนการบ้าน',
        }


# class StudentTestScoreForm(forms.ModelForm):
#     class Meta:
#         model = StudentTestScore
#         fields = ['student', 'test', 'score', 'behavior_score', 'midterm_score', 'final_score', 'assignment_score']

class StudentForm(forms.ModelForm):
    class Meta:
        model = StudentInfo
        fields = [
            'student_id',
            'first_name',
            'last_name',
            'grade_level',
            'classroom',
            'phone_number',
            'email',
            'guardian_name',
            'guardian_email'
        ]
        widgets = {
            'student_id': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'grade_level': forms.TextInput(attrs={'class': 'form-control'}),
            'classroom': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'guardian_name': forms.TextInput(attrs={'class': 'form-control'}),
            'guardian_email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class ExcelUploadForm(forms.Form):
    file = forms.FileField(
        label="อัปโหลดไฟล์ Excel",
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )