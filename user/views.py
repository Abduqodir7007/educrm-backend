from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from user.utils import generate_token
from .models import User, Lesson, Attendance, Homework, Group
from rest_framework.views import APIView
from .serializers import SignUpSerializer, LoginSerializer


class SignupView(APIView):

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = generate_token(user)
        return Response({"token": token}, status=status.HTTP_201_CREATED)


class LoginView(APIView):

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            serializer.validated_data["token"], status=status.HTTP_201_CREATED
        )
