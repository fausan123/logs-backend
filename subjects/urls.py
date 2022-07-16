from django.urls import path
from .views import LOCreate, SubjectCreate, SubjectDetail, SubjectList, SubjectStudentAdd

urlpatterns = [
    path('create/', SubjectCreate.as_view()),
    path('<int:id>/lo/add/', LOCreate.as_view()),
    path('list/', SubjectList.as_view()),
    path('detail/<int:id>/', SubjectDetail.as_view()),
    path('<int:id>/students/add/', SubjectStudentAdd.as_view()),
]