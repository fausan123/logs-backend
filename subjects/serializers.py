from rest_framework import serializers

from users.models import User
from .models import *

class SubjectCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['name', 'description']

class LOCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningOutcome
        fields = ['name']

class SubjectListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Subject
        fields = ['id', 'name', 'description', 'created_on']

class LOViewSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = LearningOutcome
        fields = ['id', 'name', 'created_on']

# more detailed on student detail api
class StudentViewSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    admission_number = serializers.IntegerField()
    username = serializers.CharField()

    class Meta:
        model = User
        fields = ['id', 'admission_number', 'username', 'first_name', 'last_name', 'email']

class StudentAddSerailizer(serializers.Serializer):
    admission_number = serializers.IntegerField()

# add assessment later
class SubjectDetailSerailizer(serializers.ModelSerializer):
    learning_outcomes = LOViewSerializer(many=True)
    students = StudentViewSerializer(many=True)

    class Meta:
        model = Subject
        fields = ['name', 'description', 'created_on', 'learning_outcomes', 'students']

