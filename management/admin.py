from django.contrib import admin
from user.models import Teacher, User
from .models import Attendance, Group, Homework, Lesson


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
