from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, StudentProfile, TeacherProfile
from django.contrib.auth.forms import SetPasswordForm

# class UserRegisterForm(UserCreationForm):
#     is_teacher = forms.BooleanField(required=False)
#     is_student = forms.BooleanField(required=False)

#     class Meta:
#         model = User
#         fields = [
#             "username",
#             "email",
#             "password1",
#             "password2",
#             "is_teacher",
#             "is_student",
#         ]
# class UserRegisterForm(UserCreationForm):
#     username = forms.CharField(
#         label="ชื่อผู้ใช้",
#         max_length=150,
#         widget=forms.TextInput(attrs={'class':'form-control','placeholder':'ชื่อผู้ใช้'})
#     )
#     email = forms.EmailField(
#         label="อีเมล",
#         widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'อีเมล'})
#     )
#     password1 = forms.CharField(
#         label="รหัสผ่าน",
#         widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'รหัสผ่าน'})
#     )
#     password2 = forms.CharField(
#         label="ยืนยันรหัสผ่าน",
#         widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'ยืนยันรหัสผ่าน'})
#     )
#     is_teacher = forms.BooleanField(label="เป็นครู", required=False)
#     is_student = forms.BooleanField(label="เป็นนักเรียน", required=False)

#     class Meta:
#         model = User
#         fields = ["username","email","password1","password2","is_teacher","is_student"]

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.is_teacher = self.cleaned_data.get('is_teacher')
#         user.is_student = self.cleaned_data.get('is_student')
#         if commit:
#             user.save()
#         return user

# class RegisterForm(UserCreationForm):
#     ROLE_CHOICES = [
#         ("teacher", "Teacher"),
#         ("student", "Student"),
#     ]
#     role = forms.ChoiceField(choices=ROLE_CHOICES, label="ลงทะเบียนเป็น")

#     class Meta:
#         model = User
#         fields = ["username", "email", "password1", "password2", "role"]

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         role = self.cleaned_data["role"]
#         if role == "teacher":
#             user.is_teacher = True
#         else:
#             user.is_student = True
#         if commit:
#             user.save()
#         return user


class UserRegisterForm(UserCreationForm):
    ROLE_CHOICES = (
        ('student', 'นักเรียน'),
        ('teacher', 'ครู'),
    )
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.RadioSelect,
        label="ประเภทผู้ใช้งาน"
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role']

    def save(self, commit=True):
        user = super().save(commit=False)
        role = self.cleaned_data.get('role')
        user.is_student = role == 'student'
        user.is_teacher = role == 'teacher'
        if commit:
            user.save()
        return user


class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ['student_id','first_name','last_name','grade_level','classroom']
        widgets = {
            'student_id': forms.TextInput(attrs={'class':'form-control'}),
            'first_name': forms.TextInput(attrs={'class':'form-control'}),
            'last_name': forms.TextInput(attrs={'class':'form-control'}),
            'grade_level': forms.TextInput(attrs={'class':'form-control'}),
            'classroom': forms.TextInput(attrs={'class':'form-control'}),
        }

class TeacherProfileForm(forms.ModelForm):
    class Meta:
        model = TeacherProfile
        fields = ['first_name','last_name','position','classroom','subjects']
        widgets = {
            'first_name': forms.TextInput(attrs={'class':'form-control'}),
            'last_name': forms.TextInput(attrs={'class':'form-control'}),
            'position': forms.TextInput(attrs={'class':'form-control'}),
            'classroom': forms.TextInput(attrs={'class':'form-control'}),
            'subjects': forms.TextInput(attrs={'class':'form-control'}),
        }
class CustomSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'รหัสผ่านใหม่'})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'ยืนยันรหัสผ่านใหม่'})