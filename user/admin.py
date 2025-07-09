from django.contrib import admin
from .models import User, Group, Attendance, Lesson, Homework, Teacher


class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name")

    def full_name(self, obj):
        first_name = obj.first_name.title()
        last_name = obj.last_name.title()
        return f"{last_name} {first_name}"
    
    full_name.short_description  = 'full_name'

admin.site.register(User, UserAdmin)


class GroupAdmin(admin.ModelAdmin):
    list_filter = ("id", "name", "teacher")
    list_filter = ("teacher",)
    search_fields = ("teacher", "name")

    def formfiel_for_foreignkey(self, db_field, request, **kwargs):
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
    list_display = ("id",)


admin.site.register(Attendance, AttendanceAdmin)
