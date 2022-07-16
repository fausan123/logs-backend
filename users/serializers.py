from rest_framework import serializers
from .models import User, Student, Faculty
from subjects.models import Subject, Assessment
from subjects.serializers import LOViewSerializer, AssessmentListSerializer

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

class StudentQuestionsSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    question = serializers.CharField()
    mark = serializers.IntegerField()
    learning_outcomes = LOViewSerializer(many=True)

class StudentAssessmentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    submitted_on = serializers.DateTimeField(allow_null=True)
    response = StudentQuestionsSerializer(many=True)

    class Meta:
        model = Assessment
        fields = ['id', 'title', 'description', 'created_on', 'submitted_on', 'response']

class StudentSubjectSerializer(serializers.ModelSerializer):
    learning_outcomes = LOViewSerializer(many=True)
    assessments = StudentAssessmentSerializer(many=True) 

    class Meta:
        model = Subject
        fields = fields = ['name', 'description', 'created_on', 'learning_outcomes', 'assessments']

class StudentDetailSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    username = serializers.CharField()
    profile = StudentProfileSerializer()
    subjects = StudentSubjectSerializer(many=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'date_joined', 'email', 'profile', 'subjects']
