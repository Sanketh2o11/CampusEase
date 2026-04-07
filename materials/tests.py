import json

from django.test import TestCase, Client
from django.urls import reverse

from accounts.models import User, Batch
from materials.models import Material, MaterialThankYou


class MaterialThankYouUniquenessTest(TestCase):
    def setUp(self):
        self.batch = Batch.objects.create(name='CS2026', year=2026, department='CS')
        self.student = User.objects.create_user(
            email='student@test.com', password='pass123',
            full_name='Student', role='student', batch=self.batch
        )
        self.material = Material.objects.create(
            uploader=self.student,
            title='DSA Notes',
            subject='DSA',
            drive_link='https://drive.google.com/file/d/test/view',
        )
        self.client = Client()

    def test_thankyou_uniqueness_pressing_twice_no_double_count(self):
        """MaterialThankYou uniqueness — pressing twice does not add count."""
        self.client.login(email='student@test.com', password='pass123')

        # First press
        response = self.client.post(
            reverse('material_thankyou', args=[self.material.pk]),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['count'], 1)
        self.assertFalse(data['already_thanked'])

        # Second press
        response = self.client.post(
            reverse('material_thankyou', args=[self.material.pk]),
            content_type='application/json',
        )
        data = response.json()
        self.assertEqual(data['count'], 1)
        self.assertTrue(data['already_thanked'])

        # DB check
        self.assertEqual(MaterialThankYou.objects.filter(material=self.material).count(), 1)
        self.material.refresh_from_db()
        self.assertEqual(self.material.thank_you_count, 1)


class MaterialCRDeleteTest(TestCase):
    def setUp(self):
        self.batch = Batch.objects.create(name='CS2026', year=2026, department='CS')
        self.student = User.objects.create_user(
            email='student@test.com', password='pass123',
            full_name='Student', role='student', batch=self.batch
        )
        self.cr = User.objects.create_user(
            email='cr@test.com', password='pass123',
            full_name='CR', role='cr', batch=self.batch
        )
        self.material = Material.objects.create(
            uploader=self.student, title='Notes', subject='DSA',
            drive_link='https://drive.google.com/file/d/test/view',
        )

    def test_student_cannot_delete(self):
        client = Client()
        client.login(email='student@test.com', password='pass123')
        response = client.post(reverse('material_delete', args=[self.material.pk]))
        self.assertEqual(response.status_code, 403)

    def test_cr_can_delete(self):
        client = Client()
        client.login(email='cr@test.com', password='pass123')
        response = client.post(reverse('material_delete', args=[self.material.pk]))
        self.assertRedirects(response, reverse('material_list'))
        self.assertEqual(Material.objects.count(), 0)
