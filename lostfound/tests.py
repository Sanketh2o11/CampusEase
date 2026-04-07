import json

from django.test import TestCase, Client
from django.urls import reverse

from accounts.models import User, Batch
from lostfound.models import LostFoundItem
from lostfound.forms import LostFoundItemForm


class LostFoundContactInfoMandatoryTest(TestCase):
    def test_contact_info_empty_fails_validation(self):
        """LostFoundItem contact_info is mandatory (empty fails validation)."""
        form = LostFoundItemForm(data={
            'title': 'Lost Wallet',
            'description': 'Black leather wallet',
            'status': 'lost',
            'contact_info': '',
            'last_seen_location': '',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('contact_info', form.errors)

    def test_contact_info_provided_passes(self):
        form = LostFoundItemForm(data={
            'title': 'Lost Wallet',
            'description': 'Black leather wallet',
            'status': 'lost',
            'contact_info': 'Room 204',
            'last_seen_location': 'Library',
        })
        self.assertTrue(form.is_valid())


class LostFoundClaimTest(TestCase):
    def setUp(self):
        self.batch = Batch.objects.create(name='CS2026', year=2026, department='CS')
        self.reporter = User.objects.create_user(
            email='reporter@test.com', password='pass123',
            full_name='Reporter', role='student', batch=self.batch
        )
        self.finder = User.objects.create_user(
            email='finder@test.com', password='pass123',
            full_name='Finder', role='student', batch=self.batch
        )
        self.item = LostFoundItem.objects.create(
            reporter=self.reporter,
            title='Found Keychain',
            description='Found near cafeteria',
            contact_info='9876543210',
            status='found',
        )

    def test_claim_sets_claimed_by_correctly(self):
        """Claim sets claimed_by correctly."""
        client = Client()
        client.login(email='finder@test.com', password='pass123')

        response = client.post(
            reverse('lostfound_claim', args=[self.item.pk]),
            data='{}',
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['claimed_by_name'], 'Finder')

        self.item.refresh_from_db()
        self.assertEqual(self.item.claimed_by, self.finder)


class LostFoundResolveTest(TestCase):
    def setUp(self):
        self.batch = Batch.objects.create(name='CS2026', year=2026, department='CS')
        self.reporter = User.objects.create_user(
            email='reporter@test.com', password='pass123',
            full_name='Reporter', role='student', batch=self.batch
        )
        self.cr = User.objects.create_user(
            email='cr@test.com', password='pass123',
            full_name='CR', role='cr', batch=self.batch
        )
        self.other = User.objects.create_user(
            email='other@test.com', password='pass123',
            full_name='Other', role='student', batch=self.batch
        )
        self.item = LostFoundItem.objects.create(
            reporter=self.reporter,
            title='Lost Bottle',
            description='Blue bottle',
            contact_info='Room 101',
            status='lost',
        )

    def test_cr_can_resolve(self):
        client = Client()
        client.login(email='cr@test.com', password='pass123')
        response = client.post(reverse('lostfound_resolve', args=[self.item.pk]))
        self.assertRedirects(response, reverse('lostfound_list'))
        self.item.refresh_from_db()
        self.assertTrue(self.item.is_resolved)

    def test_reporter_can_resolve(self):
        client = Client()
        client.login(email='reporter@test.com', password='pass123')
        response = client.post(reverse('lostfound_resolve', args=[self.item.pk]))
        self.assertRedirects(response, reverse('lostfound_list'))
        self.item.refresh_from_db()
        self.assertTrue(self.item.is_resolved)

    def test_other_student_cannot_resolve(self):
        client = Client()
        client.login(email='other@test.com', password='pass123')
        response = client.post(reverse('lostfound_resolve', args=[self.item.pk]))
        self.assertEqual(response.status_code, 403)
        self.item.refresh_from_db()
        self.assertFalse(self.item.is_resolved)
