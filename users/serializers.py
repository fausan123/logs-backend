from rest_framework import serializers
from .models import User, Student, Faculty

class FacultyProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = ['dob', 'address', 'phonenumber', 'position']

class FacultyRegisterSerializer(serializers.ModelSerializer):
    faculty = FacultyProfileSerializer()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password', 'email', 'faculty']

class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']

