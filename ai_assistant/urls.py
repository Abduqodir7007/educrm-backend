from django.urls import path
from .views import AiView

urlpatterns = [
    path("ai/assistant/", AiView.as_view()),
]
