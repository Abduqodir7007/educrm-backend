from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .services import ai_student_assistant


class AiView(APIView):
    def post(self, request):
        prompt = request.data.get("prompt")
        new_prompt = (
            "You are a helpful and friendly school teacher assistant, Your job is to answer students' academic questions clearly and simply. Please make your answer shorter and clear"
            + prompt
        )
        response = ai_student_assistant(prompt)
        return Response({"answer": response})
