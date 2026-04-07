from django.test import TestCase
from .models import User, Batch

class AccountsModelTests(TestCase):
    def setUp(self):
        self.batch = Batch.objects.create(name="CS2024", year=2024, department="Computer Science")
        self.user = User.objects.create_user(
            email="test@campusease.com",
            password="testpassword123",
            full_name="Test Student",
            batch=self.batch
        )

    def test_batch_creation(self):
        self.assertEqual(self.batch.name, "CS2024")
        self.assertEqual(str(self.batch), "CS2024 - Computer Science")

    def test_user_creation(self):
        self.assertEqual(self.user.email, "test@campusease.com")
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_staff)
        self.assertEqual(self.user.role, 'student')

    def test_user_is_student_property(self):
        self.assertTrue(self.user.is_student)
        self.assertFalse(self.user.is_cr)
        
    def test_cr_creation(self):
        cr_user = User.objects.create_user(
            email="cr@campusease.com",
            password="testpassword123",
            full_name="Test CR",
            batch=self.batch,
            role='cr'
        )
        self.assertTrue(cr_user.is_cr)
        self.assertFalse(cr_user.is_student)
