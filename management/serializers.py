from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from management.models import Group, Homework, Lesson
from user.models import User
from rest_framework.exceptions import NotFound


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

    # group = GroupSerializer(read_only=True)

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


class AttendanceSerializer(serializers.Serializer):
    student_id = serializers.IntegerField()
    come_to_lesson = serializers.BooleanField()

    def validate(self, data):
        user = User.objects.get(id=data["student_id"])
        if user.role in ("Teacher", "Admin"):
            raise ValidationError({"msg": "User is teacher or admin"})
        return data
