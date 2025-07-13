from django.core.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Teacher, User
from datetime import datetime
from rest_framework import permissions

class IsTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.role == Teacher
    
def generate_token(user):

    refresh = RefreshToken.for_user(user)

    return {"refresh": str(refresh), "access": str(refresh.access_token)}


def validate_time(value):
    if value < datetime.now():
        raise ValidationError('Invalid time')