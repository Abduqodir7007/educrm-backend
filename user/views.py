from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from user.utils import generate_token
from .models import Admin, Student, Teacher
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .serializers import (
    SignUpSerializer,
    LoginSerializer,
)


class SignupView(APIView):
    permission_classes = [
        AllowAny,
    ]

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = generate_token(user)
        return Response({"token": token}, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = [
        AllowAny,
    ]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            serializer.validated_data["token"], status=status.HTTP_201_CREATED
        )
        