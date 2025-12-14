from django.contrib import admin
from .models import Subject, Test, StudentTestScore,StudentInfo,AnswerExam

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'grade_level', 'get_teachers')
    list_filter = ('grade_level',)
    search_fields = ('name', 'teachers__username')

    def get_teachers(self, obj):
        return ", ".join([t.get_full_name() or t.username for t in obj.teachers.all()])
    get_teachers.short_description = "ครูผู้สอน"

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
    list_filter = ('test', 'student')
    search_fields = ('student__username', 'test__title')

@admin.register(StudentInfo)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        'student_id',
        'first_name',
        'last_name',
        'grade_level',
        'classroom',
        'phone_number',
        'email',
        'guardian_name',
        'guardian_email'
    )
    search_fields = ('student_id', 'first_name', 'last_name', 'grade_level', 'classroom')
    list_filter = ('grade_level', 'classroom')
    ordering = ('grade_level', 'classroom', 'last_name', 'first_name')

@admin.register(AnswerExam)
class AnswerExamAdmin(admin.ModelAdmin):
    list_display = (
        "subject_code",
        "subject_name",
        "test_name",
        "teacher_name",
        "exam_date",
        "created_at",
        "display_answer_key",   
    )
    search_fields = ("subject_code", "subject_name", "test_name", "teacher_name")
    list_filter = ("exam_date", "created_at")

    def display_answer_key(self, obj):
        return ", ".join(f"{k}:{v}" for k, v in obj.answer_key.items())
    
    display_answer_key.short_description = "เฉลย"


