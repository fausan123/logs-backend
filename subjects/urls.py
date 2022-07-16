from django.urls import path
from .views import AssessmentCreate, AssessmentDetail, AssessmentSubmit, LOCreate, SubjectCreate, SubjectDetail, SubjectList, SubjectStudentAdd

urlpatterns = [
    path('create/', SubjectCreate.as_view()),
    path('<int:id>/lo/add/', LOCreate.as_view()),
    path('list/', SubjectList.as_view()),
    path('detail/<int:id>/', SubjectDetail.as_view()),
    path('<int:id>/students/add/', SubjectStudentAdd.as_view()),
    path('<int:id>/assessment/create/', AssessmentCreate.as_view()),
    path('assessment/detail/<int:id>/', AssessmentDetail.as_view()),
    path('assessment/submit/<int:id>/', AssessmentSubmit.as_view()),
]