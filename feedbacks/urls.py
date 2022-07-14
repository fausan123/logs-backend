from django.urls import path
from .views import FeedbackCreate

urlpatterns = [
    path('create/', FeedbackCreate.as_view())
]