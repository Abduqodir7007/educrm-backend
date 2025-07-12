from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from user.utils import generate_token
from .models import User, Lesson, Attendance, Homework, Group
from rest_framework.views import APIView
from .serializers import (
    GroupSerializer,
    HomeworkSerializer,
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


4


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
        try:
            group = Group.objects.get(id=pk)
        except Group.DoesNotExist:
            return Response({"msg": "Group does not exists!"})

        serializer = LessonSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save(group=group)

        return Response({"msg": "Lesson created successfully"})


class HomeworkView(APIView):

    def get(self, request, pk):
        lesson = Lesson.objects.get(id=pk)
        homeworks = lesson.homeworks.all()

        serializer = HomeworkSerializer(homeworks, many=True).data
        # serializer.is_valid(raise_exception=True)
        return Response(serializer)

    def post(self, request, pk):
        try:
            lesson = Lesson.objects.get(id=pk)
        except Lesson.DoesNotExist:
            return Response({"msg": "Lesson does not exists!"})

        serializer = HomeworkSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(lesson=lesson)

        return Response({"msg": "Homework created"})


class HomeworkUpdateView(APIView):

    def put(self, request, pk):
        try:
            homework = Homework.objects.get(id=pk)
        except Homework.DoesNotExist:
            return Response({"msg": "Does not exists"})
        
        serializer = HomeworkSerializer(homework, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"msg": "Updated successfully"})

    def delete(self, request, pk):
        try:
            homework = Homework.objects.get(id=pk)
        except Homework.DoesNotExist:
            return Response({"msg": "Does not exists"})
        
        homework.delete()

        return Response({"msg": "Deleted"})
    

