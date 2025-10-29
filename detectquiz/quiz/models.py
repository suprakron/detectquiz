from django.db import models
from accounts.models import User

class Subject(models.Model):
    name = models.CharField(max_length=100, verbose_name="ชื่อรายวิชา")
    grade_level = models.CharField(max_length=20, verbose_name="ระดับชั้น")
    classroom = models.CharField(max_length=20, verbose_name="ห้องเรียน")
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subjects')

    def __str__(self):
        return f"{self.name} ({self.grade_level} - {self.classroom})"

class Test(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    full_score = models.IntegerField()

    def __str__(self):
        return f"{self.title} - {self.subject.name}"

class StudentTestScore(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='scores')
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    score = models.FloatField(null=True, blank=True)
    behavior_score = models.FloatField(null=True, blank=True)
    midterm_score = models.FloatField(null=True, blank=True)
    final_score = models.FloatField(null=True, blank=True)
    assignment_score = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.student.username} - {self.test.title}"

class StudentInfo(models.Model):
    student_id = models.CharField(max_length=20, unique=True, verbose_name="รหัสนักเรียน")
    first_name = models.CharField(max_length=50, verbose_name="ชื่อ")
    last_name = models.CharField(max_length=50, verbose_name="นามสกุล")
    grade_level = models.CharField(max_length=20, verbose_name="ระดับชั้น")
    classroom = models.CharField(max_length=20, verbose_name="ห้องเรียน")
    phone_number = models.CharField(max_length=15, verbose_name="เบอร์โทรศัพท์", blank=True, null=True)
    email = models.EmailField(verbose_name="อีเมล", blank=True, null=True)
    guardian_name = models.CharField(max_length=100, verbose_name="ชื่อผู้ปกครอง")
    guardian_email = models.EmailField(verbose_name="อีเมลผู้ปกครอง", blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.student_id})"

 
   