from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import User, Batch
from timetable.models import TimetableSlot
from attendance.models import Attendance


class TimetableAutoPopulateTest(TestCase):
    def setUp(self):
        self.batch = Batch.objects.create(name='Class of 2026', year=2026, department='CS')
        self.cr = User.objects.create_user(
            email='cr@test.com', password='testpass123',
            full_name='CR User', role='cr', batch=self.batch
        )
        self.student = User.objects.create_user(
            email='student@test.com', password='testpass123',
            full_name='Student User', role='student', batch=self.batch
        )
        self.client = Client()

    def test_cr_saves_timetable_triggers_attendance_subjects(self):
        """TimetableSlot creation by CR triggers subject auto-population."""
        self.client.login(email='cr@test.com', password='testpass123')

        post_data = {}
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
        for day in days:
            for period in range(1, 9):
                post_data[f'slot_{day}_{period}'] = ''

        # Set some subjects
        post_data['slot_monday_1'] = 'DSA'
        post_data['slot_monday_2'] = 'DBMS'
        post_data['slot_tuesday_1'] = 'DSA'
        post_data['slot_wednesday_3'] = 'CN'

        response = self.client.post(reverse('timetable_edit'), post_data)
        self.assertEqual(response.status_code, 302)

        # Check that 48 timetable slots were created
        self.assertEqual(TimetableSlot.objects.filter(batch=self.batch).count(), 48)

        # Check unique subjects: DSA, DBMS, CN = 3
        unique_subjects = set(
            TimetableSlot.objects.filter(batch=self.batch)
            .exclude(subject_name='')
            .values_list('subject_name', flat=True)
        )
        self.assertEqual(unique_subjects, {'DSA', 'DBMS', 'CN'})

        # Check attendance records created for the student
        student_attendances = Attendance.objects.filter(student=self.student)
        self.assertEqual(student_attendances.count(), 3)
        subjects = set(student_attendances.values_list('subject', flat=True))
        self.assertEqual(subjects, {'DSA', 'DBMS', 'CN'})

    def test_student_cannot_access_edit(self):
        self.client.login(email='student@test.com', password='testpass123')
        response = self.client.get(reverse('timetable_edit'))
        self.assertEqual(response.status_code, 403)
