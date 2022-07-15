from django.urls import path
from .views import FeedbackCreate, FeedbackList, FeedbackResponseList, FeedbackSubmit

urlpatterns = [
    path('create/', FeedbackCreate.as_view()),
    path('submit/<int:id>/', FeedbackSubmit.as_view()),
    path('<int:id>/view/all/', FeedbackList.as_view()),
    path('<int:id>/responses/all', FeedbackResponseList.as_view()),
]