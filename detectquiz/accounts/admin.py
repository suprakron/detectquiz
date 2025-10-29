from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_teacher', 'is_student', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_teacher', 'is_student', 'is_staff', 'is_superuser')
    fieldsets = UserAdmin.fieldsets + (
        ('User Role', {'fields': ('is_teacher', 'is_student')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('User Role', {'fields': ('is_teacher', 'is_student')}),
    )


admin.site.register(User, CustomUserAdmin)
