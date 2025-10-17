from django.db import models
from accounts.models import User

class Subject(models.Model):
    name = models.CharField(max_length=100)
    grade_level = models.CharField(max_length=50)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subjects')

    def __str__(self):
        return f"{self.name} ({self.grade_level})"

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
