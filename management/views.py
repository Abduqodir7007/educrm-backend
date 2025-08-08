from rest_framework.views import APIView
from rest_framework.response import Response
from management.models import Attendance, Lesson, Homework, Group
from rest_framework import status
from user.utils import IsTeacher
from django.db.models import Count, F, Sum, ExpressionWrapper, IntegerField
from rest_framework.exceptions import NotFound
from user.models import User, Teacher, Student
from datetime import date
from management.serializers import (
    AttendanceSerializer,
    GroupSerializer,
    HomeworkSerializer,
    LessonSerializer,
    UserSerializer,
)


# get all groups
class GroupView(APIView):
    def get(self, request):
        groups = Group.objects.all()
        serializer = GroupSerializer(groups, many=True).data
        return Response({"data": serializer}, status=status.HTTP_200_OK)

    # TO DO
    # def post(self, request):
    #     data = request.data

    #     name = request.get('name')
    #     level = request.get('level')
    #     monthly_fee = request.get('monthly')


# get the list of students in a group
class GroupStudentsView(APIView):
    def get(self, request, pk):
        group = Group.objects.get(id=pk)
        students = group.students.all()
        serializer = UserSerializer(students, many=True).data

        return Response(serializer, status=status.HTTP_200_OK)


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


# update homework
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

            # for group in Group.objects.all():
            #     fee = group.monthly_fee
            #     student_count = User.objects.filter(group=group).count()
            #     total_profit += fee * student_count
            
            total_profit = Group.objects.annotate(
                profit=ExpressionWrapper(
                    F("monthly_fee") * Count("students"), output_field=IntegerField()
                )
            ).aggregate(total=Sum("profit"))["total"]

            return Response(
                {
                    "total_users": total_users,
                    "total_teacher": total_teachers,
                    "total_students": total_students,
                    "total_groups": total_groups,
                    "total_profit": total_profit,
                }
            )


# create attendance
class AttendanceView(APIView):
    permission_classes = [IsTeacher]

    def post(self, request, pk):
        try:
            lesson = Lesson.objects.get(id=pk)
        except NotFound:
            return Response({"msg": "Not found"})

        data = request.data
        serializer = AttendanceSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        for item in data:
            student = User.objects.get(id=item["student_id"])
            come_to_lesson = item["come_to_lesson"]

            Attendance.objects.create(
                student=student, come_to_lesson=come_to_lesson, lesson=lesson
            )
        return Response({"msg": "attandance created"})

    # update attendance
    def put(self, request, pk):
        lesson = Lesson.objects.get(id=pk)
        serializer = AttendanceSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        print(serializer.validated_data)
        for item in serializer.validated_data:

            student = User.objects.get(id=item["student_id"])
            come_to_lesson = item["come_to_lesson"]

            Attendance.objects.update_or_create(
                lesson=lesson,
                student=student,
                defaults={"come_to_lesson": come_to_lesson},
            )

        return Response({"msg": "Attendance changed!"})


# get attendance data
class AttendanceGetView(APIView):
    permission_classes = [
        IsTeacher,
    ]

    def get(self, request, pk):
        group = Group.objects.get(id=pk)
        date_from = request.query_params.get("date_from")
        date_to = request.query_params.get("date_to")
        
        if date_from and date_to:
            attendances = Attendance.objects.filter(
                lesson__date__range=[date_from, date_to]
            )
        else:

            start_of_month = date.today().replace(day=1)
            attendances = Attendance.objects.filter(
                lesson__group=group, lesson__date__gte=start_of_month
            ).select_related("lesson", "student")

        result = []
        for att in attendances:
            result.append(
                {
                    "date": att.lesson.date,
                    "lesson_id": att.lesson.id,
                    "attendances": [
                        {
                            "student_id": att.student.id,
                            "come_to_lesson": att.come_to_lesson,
                        }
                    ],
                }
            )

        return Response(result)
