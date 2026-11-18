from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from .forms import CustomUserCreationForm, CustomUserChangeForm

# Register your models here.

@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    model = User

    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    ordering = ("phone_number",)
    list_display = ("phone_number", "first_name", "last_name", "is_staff", "is_active",)

    search_fields = ("phone_number", "first_name", "last_name")

    fieldsets = (
        (None, {"fields": ("phone_number",)}),

        ("Personal Information", {
            "fields": ("first_name", "last_name")
        }),

        ("Permissions", {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            )
        }),

        ("Important Dates", {
            "fields": ("last_login", "date_joined")
        }),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "phone_number",
                "first_name",
                "last_name",
                "is_active",
                "is_staff",
            ),
        }),
    )