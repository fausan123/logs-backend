from django.db import models
from django.utils import timezone

from subjects.models import Subject
from users.models import Faculty, Student

# Create your models here.
class Feedback(models.Model):
    title = models.CharField(max_length=50)
    created_on = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(Faculty, related_name="feedbacks", on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, related_name="feedbacks", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.title}"

class FeedbackResponse(models.Model):
    student = models.ForeignKey(Student, related_name="feedbacks", on_delete=models.CASCADE)
    feedback = models.ForeignKey(Feedback, related_name="responses", on_delete=models.CASCADE)
    response = models.TextField()
    submitted_on = models.DateTimeField(default=timezone.now)
    # TODO: Add a sentiment field, preferably a boolean

    class Meta:
        unique_together = ('student', 'feedback')

    def __str__(self) -> str:
        return f"{self.feedback} - {self.response}"