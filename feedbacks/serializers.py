from dataclasses import fields
from rest_framework import serializers
from .models import Feedback, FeedbackResponse

class FeedbackCreateSerializer(serializers.ModelSerializer):
    subject = serializers.IntegerField()

    class Meta:
        model = Feedback
        fields = ["title", "subject"]

class FeedbackSubmitSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedbackResponse
        fields = ["response"]

class FeedbackViewSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Feedback
        fields = ["id", "title", "created_on"]

class FeedbackResponseViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedbackResponse
        fields = ["response", "submitted_on", "student"] #maybe sentiment later