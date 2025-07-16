from django.contrib import admin
from .models import User, Group, Attendance, Lesson, Homework, Teacher
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    add_fieldsets = (
        (
            None,
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "phone_number",
                    "role",
                    "group",
                    "is_staff",
                    "is_superuser",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
    fieldsets = (
        (None, {"fields": ("phone_number", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name", "group")}),
        ("Permissions", {"fields": ("role", "is_staff", "is_superuser")}),
    )
    list_display = ("id", "full_name", "group", "phone_number", "role")
    list_filter = ("role",)
    search_fields = ("phone_number", "first_name", "last_name")
    ordering = ("first_name",)

    def full_name(self, obj):
        first_name = obj.first_name.title()
        last_name = obj.last_name.title()

        return f"{first_name} {last_name}"


admin.site.register(User, CustomUserAdmin)


class GroupAdmin(admin.ModelAdmin):
    list_filter = ("id", "name", "teacher")
    list_filter = ("teacher",)
    search_fields = ("teacher", "name")

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "teacher":
            kwargs["queryset"] = User.objects.filter(role=Teacher)
        return super(GroupAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs
        )


admin.site.register(Group, GroupAdmin)


class LessonAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_filter = ("group",)


admin.site.register(Lesson, LessonAdmin)


class HomeworkAdmin(admin.ModelAdmin):
    list_display = ("id",)


admin.site.register(Homework, HomeworkAdmin)


class AttendanceAdmin(admin.ModelAdmin):
    list_display = ("id", "student", "come_to_lesson")


admin.site.register(Attendance, AttendanceAdmin)
