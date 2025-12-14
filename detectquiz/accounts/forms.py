from django import forms
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from .models import User, StudentProfile, TeacherProfile


class UserRegisterForm(UserCreationForm):
    ROLE_CHOICES = (
        ("student", "นักเรียน"),
        ("teacher", "ครู"),
    )

    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))
    role = forms.ChoiceField(
        choices=ROLE_CHOICES, widget=forms.RadioSelect, label="ประเภทผู้ใช้งาน"
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "role"]

    def save(self, commit=True):
        user = super().save(commit=False)
        role = self.cleaned_data.get("role")

        user.is_student = role == "student"
        user.is_teacher = role == "teacher"

        if commit:
            user.save()
        return user


class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ["student_id", "first_name", "last_name", "grade_level", "classroom"]
        widgets = {f: forms.TextInput(attrs={"class": "form-control"}) for f in fields}


class TeacherProfileForm(forms.ModelForm):
    class Meta:
        model = TeacherProfile
        fields = ["first_name", "last_name", "position", "classroom", "subjects"]
        widgets = {f: forms.TextInput(attrs={"class": "form-control"}) for f in fields}


class ApproveTeacherForm(forms.ModelForm):
    class Meta:
        model = TeacherProfile
        fields = ["is_approved"]


class CustomSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["new_password1"].widget.attrs.update(
            {"class": "form-control", "placeholder": "รหัสผ่านใหม่"}
        )
        self.fields["new_password2"].widget.attrs.update(
            {"class": "form-control", "placeholder": "ยืนยันรหัสผ่านใหม่"}
        )
