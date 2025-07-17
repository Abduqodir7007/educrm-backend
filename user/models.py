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
        "management.Group",
        related_name="groups",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    objects = UserManager()

    USERNAME_FIELD = "phone_number"

    def __str__(self):
        return f"{self.last_name} {self.first_name}"
