from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class UserRegisterForm(UserCreationForm):
    is_teacher = forms.BooleanField(required=False)
    is_student = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password1",
            "password2",
            "is_teacher",
            "is_student",
        ]


class RegisterForm(UserCreationForm):
    ROLE_CHOICES = [
        ("teacher", "Teacher"),
        ("student", "Student"),
    ]
    role = forms.ChoiceField(choices=ROLE_CHOICES, label="ลงทะเบียนเป็น")

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "role"]

    def save(self, commit=True):
        user = super().save(commit=False)
        role = self.cleaned_data["role"]
        if role == "teacher":
            user.is_teacher = True
        else:
            user.is_student = True
        if commit:
            user.save()
        return user
