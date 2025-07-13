from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from user.utils import generate_token, IsTeacher
from .models import Admin, Student, Teacher, User, Lesson, Attendance, Homework, Group
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .serializers import (
    GroupSerializer,
    HomeworkSerializer,
    LessonSerializer,
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


class GroupView(APIView):
    def get(self, request):
        groups = Group.objects.all()
        serializer = GroupSerializer(groups, many=True).data
        return Response({"data": serializer}, status=status.HTTP_200_OK)


class LessonView(APIView):
    permission_classes = [
        IsTeacher,
    ]

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
    permission_classes = [
        IsTeacher,
    ]

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


class ProfileView(APIView):

    def get(self, request):
        user = request.user
        if user.role == Student:
            group = user.group
            serializer = GroupSerializer(group, many=True)
            return Response({"data": serializer.data})

        elif user.role == Teacher:
            group = user.teacher.all()
            serializer = GroupSerializer(group, many=True)
            return Response({"data": serializer.data})

        elif user.role in ("Admin", "Teacher") and user.is_superuser:

            total_users = User.objects.all().count()
            total_teachers = User.objects.filter(role=Teacher).count()
            total_students = User.objects.filter(role=Student).count()
            total_groups = Group.objects.all().count()
            total_profit = 0

            for group in Group.objects.all():
                fee = group.monthly_fee
                student_count = User.objects.filter(group=group).count()
                total_profit += fee * student_count

            return Response(
                {
                    "total_users": total_users,
                    "total_teacher": total_teachers,
                    "total_students": total_students,
                    "total_groups": total_groups,
                    "total_profit": total_profit,
                }
            )
