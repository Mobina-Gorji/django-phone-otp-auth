from django.contrib import admin
from .models import OTP

# Register your models here.

@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    model = OTP

    ordering = ("phone_number",)
    list_display = ("phone_number", "attempts", "is_used", "created_at", "expires_at",)

    search_fields = ("phone_number",)

    exclude = ("code_hash",)