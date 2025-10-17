from django import forms
from .models import Subject, Test, StudentTestScore

# class SubjectForm(forms.ModelForm):
#     class Meta:
#         model = Subject
#         fields = ['name', 'grade_level']

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'grade_level']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ชื่อรายวิชา',  
            }),
            'grade_level': forms.Select(attrs={
                'class': 'form-select',
            }),
        }
        labels = {
            'name': 'ชื่อรายวิชา',
            'grade_level': 'ระดับชั้น',
        }
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
