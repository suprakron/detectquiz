from django.contrib import admin
from .models import Subject, Test, StudentTestScore

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'grade_level', 'teacher') 
    list_filter = ('grade_level', 'teacher')           
    search_fields = ('name', 'teacher__username')      


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'full_score')
    list_filter = ('subject',)
    search_fields = ('title', 'subject__name')


@admin.register(StudentTestScore)
class StudentTestScoreAdmin(admin.ModelAdmin):
    list_display = (
        'student',
        'test',
        'score',
        'behavior_score',
        'midterm_score',
        'final_score',
        'assignment_score'
    )
    list_filter = ('test__subject', 'student')
    search_fields = ('student__username', 'test__title', 'test__subject__name')
    ordering = ('student__username',)

    list_editable = (
        'score',
        'behavior_score',
        'midterm_score',
        'final_score',
        'assignment_score'
    )
