from django.test import TestCase
from .models import OTP
from django.utils import timezone
from datetime import timedelta
from .services import hash_otp, create_otp_for_phone
from django.contrib.auth.hashers import check_password

# Create your tests here.


class OTPTest(TestCase):

    def test_create_otp(self):

        otp = OTP.objects.create(
            phone_number="+989123456789",
            code_hash="hashed_test_code",
            expires_at=timezone.now() + timedelta(minutes=2)
        )

        self.assertTrue(
            OTP.objects.filter(phone_number="+989123456789").exists()
        )
        self.assertEqual(otp.phone_number, "+989123456789")

    def test_create_otp_default_values(self):

        otp = OTP.objects.create(
            phone_number="+989123456789",
            code_hash="hashed_test_code",
            expires_at=timezone.now() + timedelta(minutes=2)
        )

        self.assertFalse(otp.is_used)
        self.assertEqual(otp.attempts, 0)

    def test_create_otp_created_at(self):

        otp = OTP.objects.create(
            phone_number="+989123456789",
            code_hash="hashed_test_code",
            expires_at=timezone.now() + timedelta(minutes=2)
        )

        self.assertIsNotNone(otp.created_at)

    def test_create_otp_expires_at(self):

        expected_expiration = timezone.now() + timedelta(minutes=2)

        otp = OTP.objects.create(
            phone_number="+989123456789",
            code_hash="hashed_test_code",
            expires_at=expected_expiration
        )

        self.assertEqual(otp.expires_at, expected_expiration)

    def test_create_otp_str(self):

        otp = OTP.objects.create(
            phone_number="+989123456789",
            code_hash="hashed_test_code",
            expires_at=timezone.now() + timedelta(minutes=2)
        )

        self.assertEqual(str(otp), "+989123456789")

class HashOTPTest(TestCase):

    def test_hash_otp_is_not_plain_text(self):

        otp = "123456"
        otp_hash = hash_otp(otp)

        self.assertNotEqual(otp_hash, otp)

    def test_otp_is_correct(self):

        otp = "123456"
        otp_hash = hash_otp(otp)

        self.assertTrue(check_password(otp, otp_hash))

    def test_otp_not_correct(self):

        otp = "123456"
        otp_hash = hash_otp(otp)

        self.assertFalse(check_password("123457", otp_hash))

class CreateOTPForPhoneTest(TestCase):

    def test_create_otp_for_phone(self):

        phone_number = "+989123456789"
        create_otp_for_phone(phone_number)

        self.assertEqual(
            OTP.objects.filter(
                phone_number=phone_number
            ).count(),
            1
        )

    def test_otp_code_is_six_digits(self):

        phone_number = "+989123456789"
        otp_code, _ = create_otp_for_phone(phone_number)

        self.assertEqual(len(otp_code), 6)
        self.assertTrue(otp_code.isdigit())

    def test_otp_hash_is_correct(self):

        phone_number = "+989123456789"
        otp_code, otp = create_otp_for_phone(phone_number)

        self.assertTrue(check_password(otp_code, otp.code_hash))

    def test_otp_plain_code_is_not_stored(self):

        phone_number = "+989123456789"
        otp_code, otp = create_otp_for_phone(phone_number)

        self.assertNotEqual(otp.code_hash, otp_code)

    def test_otp_phone_number_is_correct(self):

        phone_number = "+989123456789"
        _, otp = create_otp_for_phone(phone_number)

        self.assertEqual(otp.phone_number, phone_number)

    def test_otp_expires_after_two_minutes(self):

        phone_number = "+989123456789"
        _, otp = create_otp_for_phone(phone_number)

        expected_expiration = otp.created_at + timedelta(minutes=2)

        self.assertAlmostEqual(
            (otp.expires_at - otp.created_at).total_seconds(),
            120,
            delta=2
        )