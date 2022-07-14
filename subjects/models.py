from venv import create
from django.db import models
from django.utils import timezone

from users.models import Faculty, Student

# Create your models here.
class Subject(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField()
    created_on = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(Faculty, related_name="subjects", on_delete=models.CASCADE)
    students = models.ManyToManyField(Student, related_name="subjects")

    def __str__(self) -> str:
        return f"Subject: {self.name}"

class LearningOutcome(models.Model):
    name = models.CharField(max_length=50)
    subject = models.ForeignKey(Subject, related_name="learningoutcomes", on_delete=models.CASCADE)
    created_on = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return f"LO: {self.name}"
