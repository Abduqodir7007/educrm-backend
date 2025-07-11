from django.urls import path
from .views import SignupView, LoginView, GroupView, LessonView

urlpatterns = [
    path('register/', SignupView.as_view()),
    path('login/', LoginView.as_view()),
    path('groups/', GroupView.as_view()),
    path('group/<str:pk>/lesson/', LessonView.as_view()),
]
