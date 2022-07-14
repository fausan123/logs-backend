from django.urls import path
from .views import FacultyRegister, FacultyLogin, StudentLogin

urlpatterns = [
    path('faculty/register/', FacultyRegister.as_view()),
    path('faculty/login/', FacultyLogin.as_view()),
    path('student/login/', StudentLogin.as_view())
]