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

class AssessmentListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Assessment
        fields = ['id', 'title', 'description', 'created_on']


class SubjectDetailSerailizer(serializers.ModelSerializer):
    learning_outcomes = LOViewSerializer(many=True)
    students = StudentViewSerializer(many=True)
    assessments = AssessmentListSerializer(many=True)

    class Meta:
        model = Subject
        fields = ['name', 'description', 'created_on', 'learning_outcomes', 'students', 'assessments']

class QuestionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssessmentQuestion
        fields = ['question', 'learningoutcomes']

class AssessmentCreateSerializer(serializers.ModelSerializer):
    questions = QuestionCreateSerializer(many=True)

    class Meta:
        model = Assessment
        fields = ['title', 'description', 'questions']

class QuestionDetailSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    learningoutcomes = LOViewSerializer(many=True)

    class Meta:
        model = AssessmentQuestion
        fields = ['id', 'question', 'learningoutcomes']

class AssessmentResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    user_id = serializers.IntegerField()
    admission_number = serializers.IntegerField()
    marks = serializers.IntegerField()
    submitted_on = serializers.DateTimeField()

class AssessmentDetailSerializer(serializers.ModelSerializer):
    questions = QuestionDetailSerializer(many=True)
    responses = AssessmentResponseSerializer(many=True)

    class Meta:
        model = Assessment
        fields = ['title', 'description', 'created_on', 'questions', 'responses']

class QASerializer(serializers.ModelSerializer):
    class Meta:
        model = QAGrade
        fields = ['question', 'mark']

class AssessmentSubmitSerializer(serializers.Serializer):
    admission_number = serializers.IntegerField()
    questions = QASerializer(many=True)



