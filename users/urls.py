from django.urls import path
from .views import FacultyDetailID, FacultyDetail, FacultyRegister, FacultyLogin, StudentDetail, StudentDetailID, StudentLogin, UserLogin

urlpatterns = [
    path('faculty/register/', FacultyRegister.as_view()),
    path('faculty/login/', FacultyLogin.as_view()),
    path('student/login/', StudentLogin.as_view()),
    path('login/', UserLogin.as_view()),
    path('student/detail/', StudentDetail.as_view()),
    path('student/detail/<int:id>/', StudentDetailID.as_view()),
    path('faculty/detail/', FacultyDetail.as_view()),
    path('faculty/detail/<int:id>/', FacultyDetailID.as_view()),
]