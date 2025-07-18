from django.contrib import admin
from .models import User, Teacher
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
