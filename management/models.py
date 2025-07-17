from django.db import models
from user.models import User



class Group(models.Model):
    name = models.CharField(max_length=255)
    level = models.CharField(max_length=255, blank=True, null=True)
    monthly_fee = models.PositiveSmallIntegerField()
    max_students = models.PositiveSmallIntegerField(
        default=15, help_text="Maximum number of students in a group"
    )
    teacher = models.ForeignKey(
        "user.User",
        on_delete=models.SET_NULL,
        related_name="teacher",
        null=True,
    )

    def __str__(self):
        return self.name


class Lesson(models.Model):
    name = models.CharField(max_length=55, blank=True)
    date = models.DateField()
    group = models.ForeignKey(
        Group, on_delete=models.SET_NULL, related_name="lesson", null=True
    )

    def __str__(self):
        return self.name


class Homework(models.Model):
    task = models.TextField(max_length=300)
    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, related_name="homeworks"
    )

    def __str__(self):
        return f"homework_of_{self.lesson.name}"


class Attendance(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, null=True, related_name='attendance')
    come_to_lesson = models.BooleanField()
    student = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="attendance", null=True
    )

    def __str__(self):
        return f"{self.lesson.name} lesson's attendance"
