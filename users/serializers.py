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

class StudentProfileSerializer(serializers.ModelSerializer):
    admission_number = serializers.IntegerField()

    class Meta:
        model = Student
        fields = ['admission_number', 'dob', 'address', 'guardian_name', 'guardian_phonenumber', 'class_name']

class StudentDetailSerializer(serializers.ModelSerializer):
    #TO ADD subject 
    id = serializers.IntegerField()
    username = serializers.CharField()
    profile = StudentProfileSerializer()


    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'date_joined', 'email', 'profile']
