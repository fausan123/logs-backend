from enum import unique
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

class Assessment(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    subject = models.ForeignKey(Subject, related_name="assessments", on_delete=models.CASCADE)
    created_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.title}"

class AssessmentQuestion(models.Model):
    question = models.TextField()
    assessment = models.ForeignKey(Assessment, related_name="questions", on_delete=models.CASCADE)
    learningoutcomes = models.ManyToManyField(LearningOutcome, related_name="questions")

    def __str__(self):
        return f"{self.assessment.id} - {self.question}"

class AssessmentSubmission(models.Model):
    student = models.ForeignKey(Student, related_name="submissions", on_delete=models.CASCADE)
    assessment = models.ForeignKey(Assessment, related_name="submissions", on_delete=models.CASCADE)
    submitted_on = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('student', 'assessment')

    def __str__(self) -> str:
        return f"{self.student.user} - {self.assessment}"

class QAGrade(models.Model):
    submission = models.ForeignKey(AssessmentSubmission, related_name="qagrades", on_delete=models.CASCADE)
    question = models.ForeignKey(AssessmentQuestion, related_name="qagrades", on_delete=models.CASCADE)
    mark = models.IntegerField()  #change to float ?

    class Meta:
        unique_together = ('submission', 'question')
    
    def __str__(self):
        return f"{self.submission} - Question {self.question.id}"