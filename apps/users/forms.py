from django import forms
from .models import User

class CustomUserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            "phone_number",
            "first_name",
            "last_name",
            "is_active",
            "is_staff",
        )

    def save(self, commit=True):
        user = super().save(commit=False)

        user.set_unusable_password()

        if commit:
            user.save()

        return user


class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            "phone_number",
            "first_name",
            "last_name",
            "is_active",
            "is_staff",
            "is_superuser",
            "groups",
            "user_permissions",
        )