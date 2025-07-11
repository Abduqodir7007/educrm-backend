from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from user.utils import generate_token
from .models import User, Lesson, Attendance, Homework, Group
from rest_framework.views import APIView
from .serializers import (
    GroupSerializer,
    LessonSerializer,
    SignUpSerializer,
    LoginSerializer,
)


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


class GroupView(APIView):

    def get(self, request):
        groups = Group.objects.all()
        serializer = GroupSerializer(groups, many=True).data
        return Response({"data": serializer}, status=status.HTTP_200_OK)


class LessonView(APIView):

    def get(self, request, pk):
        group = Group.objects.get(id=pk)
        lessons = group.lesson.all()
        serializer = LessonSerializer(lessons, many=True).data

        return Response(serializer)

    def post(self, request, pk):
        group = Group.objects.get(id=pk)
        serializer = LessonSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save(group=group)

        return Response({"msg": "Lesson created successfully"})
