from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, StudentProfile, TeacherProfile
 
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'is_teacher', 'is_student', 'is_staff', 'is_active')
    list_filter = ('is_teacher', 'is_student', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Role', {'fields': ('is_teacher', 'is_student')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_teacher', 'is_student'),
        }),
    )
    search_fields = ('username', 'email')
    ordering = ('username',)

admin.site.register(User, UserAdmin)
 
@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'student_id', 'first_name', 'last_name', 'grade_level', 'classroom')
    search_fields = ('user__username', 'student_id', 'first_name', 'last_name')
    list_filter = ('grade_level', 'classroom')

 
@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'position', 'classroom', 'subjects')
    search_fields = ('user__username', 'first_name', 'last_name', 'position', 'subjects')
    list_filter = ('classroom', 'position')
