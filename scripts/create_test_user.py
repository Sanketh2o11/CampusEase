import os
import sys

import django


# Make the script runnable via `python scripts/create_test_user.py`
# (i.e., without needing `PYTHONPATH=.`).
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campusease.settings')
django.setup()

from accounts.models import User, Batch

# Create batch if it doesn't exist
batch, _ = Batch.objects.get_or_create(
    name='CS2024',
    defaults={'year': 2024, 'department': 'CS'}
)

# Create CR user
if not User.objects.filter(email='cr@test.com').exists():
    cr = User.objects.create_user(
        email='cr@test.com',
        password='campusease123',
        full_name='Test CR',
        batch=batch,
        role='cr'
    )
    print(f'Created CR user: {cr.email}')
else:
    print('CR user already exists: cr@test.com')

# Create student user
if not User.objects.filter(email='student@test.com').exists():
    student = User.objects.create_user(
        email='student@test.com',
        password='campusease123',
        full_name='Test Student',
        batch=batch,
        role='student'
    )
    print(f'Created Student user: {student.email}')
else:
    print('Student user already exists: student@test.com')

print('\n--- LOGIN CREDENTIALS ---')
print('CR Login:      cr@test.com      / campusease123')
print('Student Login: student@test.com / campusease123')
