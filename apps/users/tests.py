from django.test import TestCase
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User
from django.contrib.admin.sites import AdminSite
from .admin import CustomUserAdmin
from django.urls import reverse
from django.db import IntegrityError, transaction

# Create your tests here.

class CustomUserManagerTest(TestCase):

    def test_create_user_without_phone_number(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(
                phone_number=""
            )

    def test_create_user_with_none_phone_number(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(
                phone_number=None
            )

    def test_create_user_with_short_phone_number(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(
                phone_number="+98"
            )

    def test_create_user_with_long_phone_number(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(
                phone_number="+981234567899"
            )

    def test_create_user_with_non_numeric_phone_number(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(
                phone_number="+98912345678a"
            )

    def test_create_superuser_with_non_numeric_phone_number(self):
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                phone_number="+98912345678a"
            )

    def test_create_user_with_invalid_iranian_mobile_prefix(self):

        with self.assertRaises(ValueError):
            User.objects.create_user(
                phone_number="+981234567890"
            )

    def test_create_user_without_country_code(self):

        user = User.objects.create_user(
            phone_number="09123456789",
            first_name="Ali",
            last_name="Ahmadi",
        )

        self.assertEqual(user.phone_number, "+989123456789")
        self.assertTrue(User.objects.filter(phone_number="+989123456789").exists())

    def test_create_superuser_without_country_code(self):

        user = User.objects.create_superuser(
            phone_number="09123456789",
            first_name="Ali",
            last_name="Ahmadi",
        )

        self.assertEqual(user.phone_number, "+989123456789")
        self.assertTrue(User.objects.filter(phone_number="+989123456789").exists())

    def test_create_user_with_valid_phone_number(self):

        user = User.objects.create_user(
            phone_number="+989123456789",
            first_name="Ali",
            last_name="Ahmadi",
        )

        self.assertEqual(user.phone_number, "+989123456789")

    def test_create_user_with_duplicate_standard_phone_number(self):

        _ = User.objects.create_user(
            phone_number="+989123456789",
            first_name="Ali",
            last_name="Ahmadi",
        )
            
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                User.objects.create_user(
                    phone_number="+989123456789"
                )

    def test_create_user_with_duplicate_normalized_phone_number(self):

        _ = User.objects.create_user(
            phone_number="+989123456789",
            first_name="Ali",
            last_name="Ahmadi",
        )
            
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                User.objects.create_user(
                    phone_number="09123456789"
                )

    def test_create_user_has_default_permissions(self):
        
        user = User.objects.create_user(
            phone_number="+989123456789",
            first_name="Ali",
            last_name="Ahmadi",
        )

        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.has_usable_password())

    def test_create_user_is_active_by_default(self):
        
        user = User.objects.create_user(
            phone_number="+989123456789",
            first_name="Ali",
            last_name="Ahmadi",
        )

        self.assertTrue(user.is_active)

    def test_create_user_with_is_active_false(self):
        
        user = User.objects.create_user(
            phone_number="+989123456789",
            is_active=False,
        )

        self.assertFalse(user.is_active)

    def test_create_superuser_is_active_by_default(self):
        
        user = User.objects.create_superuser(
            phone_number="+989123456789",
            first_name="Ali",
            last_name="Ahmadi",
        )

        self.assertTrue(user.is_active)

    def test_create_superuser_with_is_active_false(self):
        
        user = User.objects.create_superuser(
            phone_number="+989123456789",
            is_active=False,
        )

        self.assertFalse(user.is_active)

    def test_create_superuser_with_valid_phone_number(self):
    
        user = User.objects.create_superuser(
            phone_number="+989123456789",
            first_name="Ali",
            last_name="Ahmadi",
        )

        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertFalse(user.has_usable_password())

    def test_create_superuser_with_invalid_is_staff(self):

        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                phone_number="+989123456789",
                is_staff=False,
            )

    def test_create_superuser_with_invalid_is_superuser(self):
        
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                phone_number="+989123456789",
                is_superuser=False,
            )

    def test_create_user_with_invalid_is_staff(self):
        
        with self.assertRaises(ValueError):
            User.objects.create_user(
                phone_number="+989123456789",
                is_staff=True,
            )

    def test_create_user_with_invalid_is_superuser(self):
        
        with self.assertRaises(ValueError):
            User.objects.create_user(
                phone_number="+989123456789",
                is_superuser=True,
            )

class CustomUserCreationFormTest(TestCase):

    def test_create_user_without_usable_password(self):
        form_data = {
            "phone_number": "+989123456789",
            "first_name": "Ali",
            "last_name": "Ahmadi",
            "is_active": True,
            "is_staff": False,
        }

        form = CustomUserCreationForm(data=form_data)

        self.assertTrue(form.is_valid())

        user = form.save()

        self.assertFalse(user.has_usable_password())
        self.assertTrue(user.pk)

class CustomUserChangeFormTest(TestCase):

    def test_update_user_without_changing_password(self):
        user = User.objects.create_user(
            phone_number="+989123456789",
            first_name="Ali",
            last_name="Ahmadi",
        )

        form_data = {
            "phone_number": "+989123456789",
            "first_name": "Reza",
            "last_name": "Ahmadi",
            "is_active": True,
            "is_staff": False,
            "is_superuser": False,
            "groups": [],
            "user_permissions": [],
        }

        form = CustomUserChangeForm(data=form_data, instance=user)

        self.assertTrue(form.is_valid())

        updated_user = form.save()

        self.assertEqual(updated_user.first_name, "Reza")
        self.assertFalse(updated_user.has_usable_password())

class CustomUserAdminTest(TestCase):

    def test_admin_uses_custom_forms(self):
        admin_instance = CustomUserAdmin(User, AdminSite())

        self.assertEqual(
            admin_instance.add_form,
            CustomUserCreationForm
        )

        self.assertEqual(
            admin_instance.form,
            CustomUserChangeForm
        )

class CustomUserAdminPageTest(TestCase):

    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            phone_number="+989123456789"
        )

        self.client.force_login(self.admin_user)

    def test_user_changelist_page_loads(self):
        url = reverse("admin:users_user_changelist")

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_user_add_page_loads(self):
        url = reverse("admin:users_user_add")

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

