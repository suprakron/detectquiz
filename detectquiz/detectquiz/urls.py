"""
URL configuration for detectquiz project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from accounts import views as accounts_views
from quiz import views as quiz_views
from reports import views as reports_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", accounts_views.login_view, name="login"),
    path("register/", accounts_views.register, name="register"),
    path("logout/", accounts_views.logout_view, name="logout"),
    path(
        "password-reset/", accounts_views.password_reset_request, name="password_reset"
    ),
    path("get_student_info/", accounts_views.get_student_info, name="get_student_info"),
    path("subjects/", quiz_views.subject_list, name="subject_list"),
    path("assign_teacher/", quiz_views.assign_teacher, name="assign_teacher"),
    path(
        "subjects/<int:subject_id>/remove_teacher/<int:teacher_id>/",
        quiz_views.remove_teacher,
        name="remove_teacher",
    ),
    path("teacher/", quiz_views.teacher_dashboard, name="teacher_dashboard"),
    path("addanswer/", quiz_views.add_answer, name="addanswer"),
    path("preview_answers/", quiz_views.preview_answers, name="preview_answers"),
    path("addstudent/", quiz_views.addstudent, name="addstudent"),
    path("result/", quiz_views.result, name="result"),
    path(
        "student/<int:student_id>/scores/",
        quiz_views.student_score_chart,
        name="student_score_chart",
    ),
    path("parentreport/", quiz_views.parentreport, name="parentreport"),
    path("preview/", quiz_views.preview_file, name="preview_file"),
    path("ocr_from_boxes/", quiz_views.ocr_from_boxes, name="ocr_from_boxes"),
    path("student/", quiz_views.student_dashboard, name="student_dashboard"),
    path("subject/create/", quiz_views.create_subject, name="create_subject"),
    path("scorerealtime/", quiz_views.score_realtime, name="scorereal"),
    path("test/create/", quiz_views.create_test, name="create_test"),
    path("scores/enter/", quiz_views.enter_scores, name="enter_scores"),
    path("student/download_pdf/", reports_views.download_pdf, name="download_pdf"),
]
