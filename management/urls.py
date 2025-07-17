from django.urls import path
from .views import (
    AttendanceGetView,
    GroupStudentsView,
    GroupView,
    LessonView,
    HomeworkUpdateView,
    HomeworkView,
    ProfileView,
    AttendanceView,
)


urlpatterns = [
    path("groups/", GroupView.as_view()),
    path("group/<str:pk>/lesson/", LessonView.as_view()),
    path("lesson/<str:pk>/homework/", HomeworkView.as_view()),
    path("homework/<str:pk>/", HomeworkUpdateView.as_view()),
    path("me/", ProfileView.as_view()),
    path("lesson/<str:pk>/attendance/", AttendanceView.as_view()),
    path("group/<str:pk>/attendance/", AttendanceGetView.as_view()),
    path("group/<str:pk>/students/", GroupStudentsView.as_view()),
]
