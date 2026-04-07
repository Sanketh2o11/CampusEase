import json

from django.test import TestCase, Client
from django.urls import reverse
from django.db import IntegrityError

from accounts.models import User, Batch
from notices.models import Notice, NoticePoll, PollVote


class PollVoteUniquenessTest(TestCase):
    def setUp(self):
        self.batch = Batch.objects.create(name='CS2026', year=2026, department='CS')
        self.cr = User.objects.create_user(
            email='cr@test.com', password='pass123',
            full_name='CR', role='cr', batch=self.batch
        )
        self.student = User.objects.create_user(
            email='student@test.com', password='pass123',
            full_name='Student', role='student', batch=self.batch
        )
        self.notice = Notice.objects.create(
            author=self.cr, title='Event', description='Test event',
            notice_type='event'
        )
        self.poll = NoticePoll.objects.create(
            notice=self.notice, question='Coming?',
            option_yes='Yes', option_no='No', option_maybe='Maybe'
        )

    def test_poll_vote_uniqueness_per_student(self):
        """Poll vote uniqueness per student per poll."""
        PollVote.objects.create(poll=self.poll, student=self.student, choice='yes')
        with self.assertRaises(IntegrityError):
            PollVote.objects.create(poll=self.poll, student=self.student, choice='no')

    def test_changing_vote_updates_not_duplicates(self):
        """Changing a poll vote updates existing record, not duplicates."""
        client = Client()
        client.login(email='student@test.com', password='pass123')

        # Vote yes
        response = client.post(
            reverse('poll_vote', args=[self.notice.pk]),
            data=json.dumps({'choice': 'yes'}),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(PollVote.objects.filter(poll=self.poll, student=self.student).count(), 1)
        self.assertEqual(PollVote.objects.get(poll=self.poll, student=self.student).choice, 'yes')

        # Change to no
        response = client.post(
            reverse('poll_vote', args=[self.notice.pk]),
            data=json.dumps({'choice': 'no'}),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(PollVote.objects.filter(poll=self.poll, student=self.student).count(), 1)
        self.assertEqual(PollVote.objects.get(poll=self.poll, student=self.student).choice, 'no')

        data = response.json()
        self.assertEqual(data['yes_count'], 0)
        self.assertEqual(data['no_count'], 1)
