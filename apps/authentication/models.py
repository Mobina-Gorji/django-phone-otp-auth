from django.db import models

# Create your models here.

class OTP(models.Model):

    phone_number = models.CharField(max_length=13)

    code_hash = models.CharField(max_length=128)

    attempts = models.PositiveSmallIntegerField(default=0)

    is_used = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def __str__(self):
        return self.phone_number