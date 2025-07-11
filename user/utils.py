from django.core.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from datetime import datetime

def generate_token(user):

    refresh = RefreshToken.for_user(user)

    return {"refresh": str(refresh), "access": str(refresh.access_token)}


def validate_time(value):
    if value < datetime.now():
        raise ValidationError('Invalid time')