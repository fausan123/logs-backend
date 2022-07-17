from django.urls import path
from .views import AssessmentCreate, AssessmentDetail, AssessmentSubmit, LOCreate, LOImprove, LOSuggest, ProgressGraph, SubjectCreate, SubjectDetail, SubjectList, SubjectStudentAdd

urlpatterns = [
    path('create/', SubjectCreate.as_view()),
    path('<int:id>/lo/add/', LOCreate.as_view()),
    path('list/', SubjectList.as_view()),
    path('detail/<int:id>/', SubjectDetail.as_view()),
    path('<int:id>/students/add/', SubjectStudentAdd.as_view()),
    path('<int:id>/assessment/create/', AssessmentCreate.as_view()),
    path('assessment/detail/<int:id>/', AssessmentDetail.as_view()),
    path('assessment/submit/<int:id>/', AssessmentSubmit.as_view()),
    path('<int:id>/assessment/progressgraph/<int:adm_num>/', ProgressGraph.as_view()),
    path('<int:id>/lo/improve/<int:adm_num>/', LOImprove.as_view()),
    path('<int:id>/lo/suggest/', LOSuggest.as_view()),
]