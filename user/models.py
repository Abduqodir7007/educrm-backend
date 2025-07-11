from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

Student, Teacher, Admin, Accountant = "Student", "Teacher", "Admin", "Accountant"


class UserManager(BaseUserManager):

    def create_user(self, phone_number, password=None, **extra_fields):

        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(phone_number, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    ROLES = (
        (Student, Student),
        (Teacher, Teacher),
        (Admin, Admin),
        (Accountant, Accountant),
    )
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, unique=True)
    role = models.CharField(max_length=255, choices=ROLES, default=Student)
    is_staff = models.BooleanField(default=False)
    group = models.ForeignKey(
        "user.Group",
        related_name="students",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    objects = UserManager()

    USERNAME_FIELD = "phone_number"

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


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
    task = models.TextField(max_length=255)
    date = models.DateField()
    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, related_name="homeworks"
    )

    def __str__(self):
        return f"homework_of_{self.lesson.name}"


class Attendance(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, null=True)
    come_to_lesson = models.BooleanField()
    student = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="attendance", null=True
    )

    def __str__(self):
        return f"{self.lesson.name} lesson's attendance"
