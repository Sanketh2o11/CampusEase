import json

from django.test import TestCase, Client
from django.urls import reverse

from accounts.models import User, Batch
from exams.models import BatchExam, PersonalExamResult


class BatchExamVisibilityTest(TestCase):
    def setUp(self):
        self.batch = Batch.objects.create(name='CS2026', year=2026, department='CS')
        self.other_batch = Batch.objects.create(name='EC2026', year=2026, department='EC')
        self.cr = User.objects.create_user(
            email='cr@test.com', password='pass123',
            full_name='CR', role='cr', batch=self.batch
        )
        self.student1 = User.objects.create_user(
            email='s1@test.com', password='pass123',
            full_name='Student 1', role='student', batch=self.batch
        )
        self.student2 = User.objects.create_user(
            email='s2@test.com', password='pass123',
            full_name='Student 2', role='student', batch=self.other_batch
        )
        self.exam = BatchExam.objects.create(
            batch=self.batch, created_by=self.cr,
            subject='DSA', exam_name='DSA Midterm',
            exam_type='internal', exam_date='2026-04-15',
        )

    def test_batch_exam_visible_to_all_students_in_batch(self):
        """BatchExam visible to all students in batch."""
        client = Client()
        client.login(email='s1@test.com', password='pass123')
        response = client.get(reverse('exam_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'DSA Midterm')

    def test_batch_exam_not_visible_to_other_batch(self):
        client = Client()
        client.login(email='s2@test.com', password='pass123')
        response = client.get(reverse('exam_list'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'DSA Midterm')


class PersonalExamResultPrivacyTest(TestCase):
    def setUp(self):
        self.batch = Batch.objects.create(name='CS2026', year=2026, department='CS')
        self.cr = User.objects.create_user(
            email='cr@test.com', password='pass123',
            full_name='CR', role='cr', batch=self.batch
        )
        self.student1 = User.objects.create_user(
            email='s1@test.com', password='pass123',
            full_name='Student 1', role='student', batch=self.batch
        )
        self.student2 = User.objects.create_user(
            email='s2@test.com', password='pass123',
            full_name='Student 2', role='student', batch=self.batch
        )
        self.exam = BatchExam.objects.create(
            batch=self.batch, created_by=self.cr,
            subject='DSA', exam_name='DSA Midterm',
            exam_type='internal', exam_date='2026-03-15',
        )

    def test_personal_result_filtered_by_request_user(self):
        """PersonalExamResult filtered strictly by request.user."""
        # Student 1 adds result
        PersonalExamResult.objects.create(
            student=self.student1, batch_exam=self.exam,
            score='42/50', notes='Good'
        )

        # Student 2 should not see student 1's result
        client = Client()
        client.login(email='s2@test.com', password='pass123')
        response = client.get(reverse('exam_list'))
        self.assertNotContains(response, '42/50')

    def test_add_result_via_ajax(self):
        client = Client()
        client.login(email='s1@test.com', password='pass123')
        response = client.post(
            reverse('personal_result_create', args=[self.exam.pk]),
            data=json.dumps({'score': '38/50', 'notes': 'Could be better'}),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['score'], '38/50')
        self.assertEqual(PersonalExamResult.objects.filter(student=self.student1).count(), 1)
