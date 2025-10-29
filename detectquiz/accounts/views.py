from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm
from .models import User

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        print("POST data:", request.POST)
        
        if form.is_valid():
            user = form.save()
            login(request, user)
            if user.is_teacher:
                return redirect("teacher_dashboard")  
            elif user.is_student:
                return redirect("student_dashboard")  
            else:
                return redirect("login")  
        else:
  
            print("Form errors:", form.errors)
            messages.error(request, "กรุณาตรวจสอบข้อมูลให้ถูกต้อง")
    else:
        form = UserRegisterForm()
    return render(request, "accounts/register.html", {"form": form})

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