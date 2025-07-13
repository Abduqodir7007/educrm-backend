from django.urls import path
from .views import (
    HomeworkView,
    SignupView,
    LoginView,
    GroupView,
    LessonView,
    HomeworkUpdateView,
    ProfileView,
)

urlpatterns = [
    path("register/", SignupView.as_view()),
    path("login/", LoginView.as_view()),
    path("groups/", GroupView.as_view()),
    path("group/<str:pk>/lesson/", LessonView.as_view()),
    path("lesson/<str:pk>/homework/", HomeworkView.as_view()),
    path("homework/<str:pk>/", HomeworkUpdateView.as_view()),
    path("me/", ProfileView.as_view()),
]
