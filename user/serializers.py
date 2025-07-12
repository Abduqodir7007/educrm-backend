from rest_framework import serializers

from user.utils import generate_token, validate_time
from .models import User, Group, Attendance, Homework, Lesson
from rest_framework.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate


class SignUpSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    phone_number = serializers.CharField()
    password = serializers.CharField()
    confirm_password = serializers.CharField(required=True)

    def validate(self, data):
        password = data.get("password", None)
        confirm_password = data.get("confirm_password", None)
        first_name = data.get("first_name", None)
        last_name = data.get("last_name", None)

        if password != confirm_password:
            raise ValidationError({"msg": "Password fields must be the same"})
        if password:
            validate_password(password)
            validate_password(confirm_password)

        if first_name.isdigit() or len(first_name) < 3:
            raise ValidationError({"msg": "Please Enter Valid First Name"})

        if last_name.isdigit() or len(last_name) < 3:
            raise ValidationError({"msg": "Please Enter Valid Last Name"})

        return data

    def validate_phone_number(self, value):
        if User.objects.filter(phone_number=value).exists():
            raise ValidationError(
                {"success": False, "msg": "This phone number already registered."}
            )
        return value

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField()

    def auth_validate(self, data):
        phone_number = data.get("phone_number")
        password = data.get("password")

        user = authenticate(phone_number=phone_number, password=password)
        if user is None:
            raise ValidationError({"msg": "Invalid credentials"})

        self.user = user

    def validate(self, data):
        self.auth_validate(data)
        token = generate_token(self.user)
        data["token"] = token
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "role"]


class GroupSerializer(serializers.ModelSerializer):
    teacher = UserSerializer(read_only=True)

    class Meta:
        model = Group
        fields = ["id", "name", "level", "teacher"]


class LessonSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    date = serializers.DateField()
    
    #group = GroupSerializer(read_only=True)

    # def validate_date(self, value):
    #     validate_time(value)

    def validate_name(self, value):
        if value.isdigit():
            raise ValidationError(
                {"msg": "Name of the lesson cannot be entirely numeric"}
            )
        return value

    def create(self, validated_data):
        return Lesson.objects.create(**validated_data)


class HomeworkSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    task = serializers.CharField()
    lesson = LessonSerializer(read_only=True)

    def create(self, validated_data):
        return Homework.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.task = validated_data.get("task", instance.task)
        instance.lesson = validated_data.get("group", instance.lesson)
        instance.save()
        return instance
    
