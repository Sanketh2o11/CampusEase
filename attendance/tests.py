import json
from datetime import date

from django.test import TestCase, Client
from django.urls import reverse
from django.db import IntegrityError

from accounts.models import User, Batch
from attendance.models import Attendance, AttendanceRecord
from attendance.views import compute_attendance_stats


class AttendanceRecordUniqueConstraintTest(TestCase):
    def setUp(self):
        self.batch = Batch.objects.create(name='CS2026', year=2026, department='CS')
        self.student = User.objects.create_user(
            email='student@test.com', password='pass123',
            full_name='Student', role='student', batch=self.batch
        )
        self.attendance = Attendance.objects.create(student=self.student, subject='DSA')

    def test_unique_constraint_same_student_subject_date(self):
        """AttendanceRecord unique constraint: same student, subject, date."""
        AttendanceRecord.objects.create(
            student=self.student, subject=self.attendance,
            date=date(2026, 3, 14), status='present'
        )
        with self.assertRaises(IntegrityError):
            AttendanceRecord.objects.create(
                student=self.student, subject=self.attendance,
                date=date(2026, 3, 14), status='absent'
            )

    def test_different_dates_allowed(self):
        AttendanceRecord.objects.create(
            student=self.student, subject=self.attendance,
            date=date(2026, 3, 14), status='present'
        )
        AttendanceRecord.objects.create(
            student=self.student, subject=self.attendance,
            date=date(2026, 3, 15), status='absent'
        )
        self.assertEqual(AttendanceRecord.objects.filter(student=self.student).count(), 2)


class AttendancePercentageAndClassesNeededTest(TestCase):
    def setUp(self):
        self.batch = Batch.objects.create(name='CS2026', year=2026, department='CS')
        self.student = User.objects.create_user(
            email='student@test.com', password='pass123',
            full_name='Student', role='student', batch=self.batch
        )
        self.attendance = Attendance.objects.create(student=self.student, subject='DSA')

    def _mark_days(self, present_count, absent_count):
        from datetime import timedelta
        current = date(2026, 1, 1)
        for i in range(present_count):
            AttendanceRecord.objects.create(
                student=self.student, subject=self.attendance,
                date=current, status='present'
            )
            current += timedelta(days=1)
        for i in range(absent_count):
            AttendanceRecord.objects.create(
                student=self.student, subject=self.attendance,
                date=current, status='absent'
            )
            current += timedelta(days=1)

    def test_percentage_above_75(self):
        """Attendance percentage and can_miss message when >= 75%."""
        self._mark_days(present_count=40, absent_count=5)
        stats = compute_attendance_stats(self.attendance)
        self.assertAlmostEqual(stats['percentage'], 88.9, places=1)
        self.assertIn('can miss', stats['message'])

    def test_percentage_below_75(self):
        """Attendance percentage and needed message when < 75%."""
        self._mark_days(present_count=30, absent_count=15)
        stats = compute_attendance_stats(self.attendance)
        self.assertAlmostEqual(stats['percentage'], 66.7, places=1)
        self.assertIn('Attend', stats['message'])
        self.assertIn('more', stats['message'])

    def test_no_classes_marked(self):
        """When no classes are marked, percentage is 0 and message is informational."""
        stats = compute_attendance_stats(self.attendance)
        self.assertEqual(stats['percentage'], 0.0)
        self.assertEqual(stats['message'], 'No classes marked yet')

    def test_mark_via_ajax(self):
        """POST /attendance/mark/ works and returns updated stats."""
        client = Client()
        client.login(email='student@test.com', password='pass123')
        response = client.post(
            reverse('attendance_mark'),
            data=json.dumps({
                'subject_id': self.attendance.id,
                'date': '2026-03-14',
                'status': 'present',
            }),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['attended'], 1)
        self.assertEqual(data['total'], 1)
        self.assertEqual(data['percentage'], 100.0)
