from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, StudentProfileForm, TeacherProfileForm
from .models import User
from quiz.models import StudentInfo 
from django.http import JsonResponse

def register(request):
    if request.method == "POST":
        user_form = UserRegisterForm(request.POST)
        student_form = StudentProfileForm(request.POST)
        teacher_form = TeacherProfileForm(request.POST)

        if user_form.is_valid():
            user = user_form.save(commit=False)
            role = user_form.cleaned_data.get('role')
            user.is_student = role == 'student'
            user.is_teacher = role == 'teacher'
            user.save()

            if user.is_student:
                if student_form.is_valid():
                    profile = student_form.save(commit=False)
                    profile.user = user
                    profile.save()
                    login(request, user)
                    return redirect('student_dashboard')
                else:
                    print(student_form.errors) 
                    messages.error(request, "ตรวจสอบข้อมูลนักเรียน")

            elif user.is_teacher:
                if teacher_form.is_valid():
                    profile = teacher_form.save(commit=False)
                    profile.user = user
                    profile.save()
                    login(request, user)
                    return redirect('teacher_dashboard')
                else:
                    print(teacher_form.errors) 
                    messages.error(request, "ตรวจสอบข้อมูลครู")

        else:
            print(user_form.errors)  
            messages.error(request, "ตรวจสอบข้อมูลผู้ใช้")

    else:
        user_form = UserRegisterForm()
        student_form = StudentProfileForm()
        teacher_form = TeacherProfileForm()

    context = {
        'user_form': user_form,
        'student_form': student_form,
        'teacher_form': teacher_form,
    }
    return render(request, "accounts/register.html", context)


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_teacher:
                return redirect("teacher_dashboard")
            elif user.is_student:
                return redirect("student_dashboard")
            else:
                return redirect("login")   
        else:
            return render(request, "accounts/login.html", {"error": "ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง"})
    return render(request, "accounts/login.html")

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "ออกจากระบบเรียบร้อยแล้ว")
    return redirect("login")
def password_reset_request(request):
    if request.method == "POST":
        email = request.POST.get("email")
        if email:
            # logic ส่งอีเมล reset password
            messages.success(request, "ส่งลิงก์รีเซ็ตรหัสผ่านไปยังอีเมลของคุณเรียบร้อยแล้ว")
        else:
            messages.error(request, "กรุณากรอกอีเมลของคุณ")
    return render(request, "accounts/forgotpassword.html")

def get_student_info(request):
    student_id = request.GET.get('student_id')
    try:
        student = StudentInfo.objects.get(student_id=student_id)
        data = {
            "first_name": student.first_name,
            "last_name": student.last_name,
            "grade_level": student.grade_level,
            "classroom": student.classroom,
        }
        return JsonResponse({"success": True, "data": data})
    except StudentInfo.DoesNotExist:
        return JsonResponse({"success": False, "data": {}})
