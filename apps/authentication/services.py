import secrets
from django.contrib.auth.hashers import make_password, check_password
from datetime import timedelta
from django.utils import timezone
from .models import OTP
from django.db import transaction

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

def verify_otp(phone_number, otp_code):

    with transaction.atomic():

        otp = OTP.objects.select_for_update().filter(
            phone_number=phone_number
        ).order_by("-created_at", "-id").first()

        if otp is None:
            return False

        if otp.is_used:
            return False

        if otp.expires_at <= timezone.now():
            return False

        if otp.attempts >= 4:
            return False

        if not check_password(otp_code, otp.code_hash):
            otp.attempts += 1
            otp.save(update_fields=["attempts"])
            return False

        otp.is_used = True
        otp.save(update_fields=["is_used"])

        return True