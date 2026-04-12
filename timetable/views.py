import json

from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin

from core.mixins import CRRequiredMixin
from django.contrib import messages
from django.views import View
from django.utils import timezone
from .models import TimetableSlot
from attendance.models import Attendance
from accounts.models import User


DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
DAY_LABELS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
PERIODS = range(1, 9)


def _build_grid_data(slots):
    """Build grid and grid_data from a TimetableSlot queryset.

    Returns:
        grid: dict keyed by (day, period) → subject_name
        grid_data: JSON-serializable dict keyed by day → list of subject strings per period
    """
    grid = {}
    for slot in slots:
        grid[(slot.day, slot.period)] = slot.subject_name
    grid_data = {}
    for day in DAYS:
        grid_data[day] = [grid.get((day, p), '') for p in PERIODS]
    return grid, grid_data


class TimetableStudentView(LoginRequiredMixin, View):
    """Read-only timetable view for all users."""

    def get(self, request):
        batch = request.user.batch
        if not batch:
            return render(request, 'timetable/view.html', {
                'error': 'You are not assigned to a batch yet.',
                'days': DAYS,
                'day_labels': DAY_LABELS,
                'periods': list(PERIODS),
                'grid': {},
                'today_day': '',
                'today_subjects': [],
            })

        slots = TimetableSlot.objects.filter(batch=batch)
        grid, grid_data = _build_grid_data(slots)

        # Today info
        today_name = timezone.now().strftime('%A').lower()
        today_subjects = []
        if today_name in DAYS:
            for p in PERIODS:
                subj = grid.get((today_name, p), '')
                if subj:
                    today_subjects.append(subj)

        # Deduplicate today subjects for display
        today_unique = list(dict.fromkeys(today_subjects))

        return render(request, 'timetable/view.html', {
            'days': DAYS,
            'day_labels': DAY_LABELS,
            'periods': list(PERIODS),
            'grid': grid,
            'grid_data_json': json.dumps(grid_data),
            'days_json': json.dumps(DAYS),
            'periods_json': json.dumps(list(PERIODS)),
            'today_day': today_name,
            'today_subjects': today_unique,
            'today_label': timezone.now().strftime('%A'),
            'batch': batch,
            'is_cr': request.user.is_cr,
        })


class TimetableEditView(LoginRequiredMixin, CRRequiredMixin, View):
    """CR-only timetable edit view."""

    def get(self, request):
        batch = request.user.batch
        if not batch:
            return render(request, 'timetable/edit.html', {
                'error': 'You are not assigned to a batch.',
                'days': DAYS,
                'day_labels': DAY_LABELS,
                'periods': list(PERIODS),
                'grid': {},
            })

        slots = TimetableSlot.objects.filter(batch=batch)
        grid, grid_data = _build_grid_data(slots)

        return render(request, 'timetable/edit.html', {
            'days': DAYS,
            'day_labels': DAY_LABELS,
            'periods': list(PERIODS),
            'grid': grid,
            'grid_data_json': json.dumps(grid_data),
            'days_json': json.dumps(DAYS),
            'periods_json': json.dumps(list(PERIODS)),
            'batch': batch,
        })

    def post(self, request):
        batch = request.user.batch
        if not batch:
            return redirect('timetable_view')

        # Delete all existing slots for this batch and recreate
        TimetableSlot.objects.filter(batch=batch).delete()

        new_slots = []
        for day in DAYS:
            for period in PERIODS:
                field_name = f"slot_{day}_{period}"
                subject = request.POST.get(field_name, '').strip()
                new_slots.append(TimetableSlot(
                    batch=batch,
                    day=day,
                    period=period,
                    subject_name=subject,
                ))

        TimetableSlot.objects.bulk_create(new_slots)

        # Auto-populate attendance subjects for all students in this batch
        self._auto_populate_attendance(batch)

        messages.success(request, 'Timetable saved successfully!')
        return redirect('timetable_view')

    def _auto_populate_attendance(self, batch):
        """Create Attendance records for unique subjects for every student in the batch."""
        subjects = set(
            TimetableSlot.objects.filter(batch=batch)
            .exclude(subject_name='')
            .values_list('subject_name', flat=True)
            .distinct()
        )

        if not subjects:
            return

        students = User.objects.filter(batch=batch)

        records = []
        for student in students:
            for subject in subjects:
                records.append(Attendance(
                    student=student,
                    subject=subject,
                ))

        Attendance.objects.bulk_create(records, ignore_conflicts=True)
