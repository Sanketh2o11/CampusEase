from django.test import TestCase
from django.contrib.auth.models import User

class UserAuthTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='student',
            password='test123'
        )

    def test_user_login_success(self):
        login = self.client.login(username='student', password='test123')
        self.assertTrue(login)

    def test_user_login_fail(self):
        login = self.client.login(username='student', password='wrong')
        self.assertFalse(login)


class RoleAccessTest(TestCase):

    def setUp(self):
        self.student = User.objects.create_user(username='student', password='123')
        self.cr = User.objects.create_user(username='cr', password='123', is_staff=True)

    def test_student_blocked(self):
        self.client.login(username='student', password='123')
        response = self.client.get('/cr-dashboard/')
        self.assertEqual(response.status_code, 403)

    def test_cr_access(self):
        self.client.login(username='cr', password='123')
        response = self.client.get('/cr-dashboard/')
        self.assertEqual(response.status_code, 200)
