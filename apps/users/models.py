from django.db import models
import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager

# Create your models here.

class UserManager(BaseUserManager):

    def _normalize_phone_number(self, phone_number):
        if not phone_number:
            raise ValueError("Phone number is required")

        if phone_number.startswith("09"):
            phone_number = "+98" + phone_number[1:]

        if not phone_number.startswith("+989"):
            raise ValueError("Phone number is not valid")

        if not phone_number.removeprefix("+98").isdigit():
            raise ValueError("Phone number is not valid")

        if len(phone_number) != 13:
            raise ValueError("Phone number is not valid")

        return phone_number

    def _create_user(self, phone_number, **extra_fields):
        user = self.model(
            phone_number=self._normalize_phone_number(phone_number),
            **extra_fields
        )

        # set_unusable_password():
        # check_password(something) --> always False
        # disables password-based authentication since users log in via OTP

        user.set_unusable_password()
        user.save(using=self._db)

        return user

    def create_user(self, phone_number, **extra_fields):

        if (
            extra_fields.get("is_staff") is True 
            or extra_fields.get("is_superuser") is True
        ):
                raise ValueError(
                    "Regular users cannot have staff or superuser permissions"
                )

        return self._create_user(phone_number, **extra_fields)

    def create_superuser(self, phone_number, **extra_fields):
        
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")

        return self._create_user(phone_number, **extra_fields)
    

class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    phone_number = models.CharField(max_length=13, unique=True)

    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    objects = UserManager()