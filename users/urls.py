from django.urls import path
from .views import FacultyDetail, FacultyRegister, FacultyLogin, StudentDetail, StudentLogin, UserLogin

urlpatterns = [
    path('faculty/register/', FacultyRegister.as_view()),
    path('faculty/login/', FacultyLogin.as_view()),
    path('student/login/', StudentLogin.as_view()),
    path('login/', UserLogin.as_view()),
    path('student/detail/<int:id>/', StudentDetail.as_view()),
    path('faculty/detail/<int:id>/', FacultyDetail.as_view()),
]