import secrets
from django.contrib.auth.hashers import make_password
from datetime import timedelta
from django.utils import timezone
from .models import OTP

def generate_otp():

    otp = secrets.randbelow(900000) + 100000
    return str(otp)

def hash_otp(otp):
    return make_password(otp)

def create_otp_for_phone(phone_number):
    expires_at = timezone.now() + timedelta(minutes=2)

    otp_code = generate_otp()
    otp_hash = hash_otp(otp_code)

    otp = OTP.objects.create(
        phone_number=phone_number,
        code_hash=otp_hash,
        expires_at=expires_at
    )

    return otp_code, otp