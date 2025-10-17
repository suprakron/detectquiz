from django import forms
from .models import Subject, Test, StudentTestScore

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'grade_level']

class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ['subject', 'title', 'full_score']

class StudentTestScoreForm(forms.ModelForm):
    class Meta:
        model = StudentTestScore
        fields = ['student', 'test', 'score', 'behavior_score', 'midterm_score', 'final_score', 'assignment_score']
