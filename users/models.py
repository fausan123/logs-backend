from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver

from django.conf import settings
from django.db.models.signals import post_save
from django.forms import ValidationError
from rest_framework.authtoken.models import Token

# Create your models here.
class User(AbstractUser):
    is_approved = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ["is_student"]
        else:
            return []

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

class Student(models.Model):
    user = models.OneToOneField(User, related_name="students", on_delete=models.CASCADE)
    dob = models.DateField()
    address = models.TextField()
    admission_number = models.IntegerField()
    guardian_name = models.CharField(max_length=50)
    guardian_phonenumber = models.CharField(max_length=10)
    class_name = models.CharField(max_length=10)

    def clean(self):
        if not self.user.is_student:
            raise ValidationError("Cannot create a student profile for faculty user !!")
    
    def __str__(self) -> str:
        return f"Student: {self.user.first_name}"

class Faculty(models.Model):
    user = models.OneToOneField(User, related_name="faculties", on_delete=models.CASCADE)
    dob = models.DateField()
    address = models.TextField()
    phonenumber = models.CharField(max_length=10)
    position = models.CharField(max_length=20)  # add options later?

    def clean(self):
        if self.user.is_student:
            raise ValidationError("Cannot create a faculty profile for student user !!")

    def __str__(self) -> str:
        return f"Faculty: {self.user.first_name}"

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)