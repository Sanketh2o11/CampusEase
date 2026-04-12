from math import ceil, floor
from datetime import timedelta

from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.utils import timezone
from django.db.models import Count, Q

from .models import Attendance, AttendanceRecord
from timetable.models import TimetableSlot
from core.utils import parse_json_body


def compute_attendance_stats(attendance_obj):
    """Compute attended, total, percentage, and classes-needed message for an Attendance subject."""
    records = attendance_obj.records.all()
    total = records.filter(~Q(status='not_marked')).count()
    attended = records.filter(status='present').count()

    if total > 0:
        percentage = round((attended / total) * 100, 1)
    else:
        percentage = 0.0

    # Classes needed / can miss calculation
    message = ''
    if total == 0:
        message = 'No classes marked yet'
    elif percentage < 75:
        needed = ceil((0.75 * total - attended) / 0.25)
        message = f'Attend {needed} more classes to reach 75%'
    else:
        can_miss = floor((attended - 0.75 * total) / 0.75)
        message = f'You can miss {can_miss} more classes safely'

    return {
        'id': attendance_obj.id,
        'subject': attendance_obj.subject,
        'attended': attended,
        'total': total,
        'percentage': percentage,
        'message': message,
    }


class AttendanceListView(LoginRequiredMixin, ListView):
    model = Attendance
    template_name = 'attendance/list.html'
    context_object_name = 'attendances'

    def get_queryset(self):
        return Attendance.objects.filter(student=self.request.user).prefetch_related('records')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        attendances = context['attendances']

        # Compute stats for each subject
        stats_list = [compute_attendance_stats(att) for att in attendances]
        context['stats_list'] = stats_list

        # Overall average
        total_all = sum(s['total'] for s in stats_list)
        attended_all = sum(s['attended'] for s in stats_list)
        if total_all > 0:
            context['overall_percentage'] = round((attended_all / total_all) * 100, 1)
        else:
            context['overall_percentage'] = 0.0

        context['total_subjects'] = len(stats_list)
        context['subjects_safe'] = sum(1 for s in stats_list if s['percentage'] >= 75)
        context['subjects_at_risk'] = sum(1 for s in stats_list if 0 < s['total'] and s['percentage'] < 75)

        # Current week dates for the week strip
        today = timezone.now().date()
        context['today'] = today

        # Day → subjects map from timetable (lowercase day keys e.g. 'tuesday')
        user = self.request.user
        day_subjects = {}
        if user.batch:
            slots = (
                TimetableSlot.objects
                .filter(batch=user.batch)
                .exclude(subject_name='')
                .values_list('day', 'subject_name')
                .distinct()
            )
            for day, subject in slots:
                day_subjects.setdefault(day, [])
                if subject not in day_subjects[day]:
                    day_subjects[day].append(subject)

        context['day_subjects'] = day_subjects

        return context


@login_required
@require_POST
def attendance_mark(request):
    """AJAX endpoint: POST /attendance/mark/ — mark attendance for a subject on a date."""
    data, err = parse_json_body(request)
    if err:
        return err
    subject_id = data.get('subject_id')
    date_str = data.get('date')
    status = data.get('status')

    if status not in ('present', 'absent', 'not_marked'):
        return JsonResponse({'error': 'Invalid status'}, status=400)

    try:
        attendance = Attendance.objects.get(id=subject_id, student=request.user)
    except Attendance.DoesNotExist:
        return JsonResponse({'error': 'Subject not found'}, status=404)

    from datetime import date as date_cls
    try:
        mark_date = date_cls.fromisoformat(date_str)
    except (ValueError, TypeError):
        return JsonResponse({'error': 'Invalid date format'}, status=400)

    # Update or create the record
    record, created = AttendanceRecord.objects.update_or_create(
        student=request.user,
        subject=attendance,
        date=mark_date,
        defaults={'status': status},
    )

    # Recompute stats
    stats = compute_attendance_stats(attendance)

    return JsonResponse({
        'percentage': stats['percentage'],
        'attended': stats['attended'],
        'total': stats['total'],
        'message': stats['message'],
    })


@login_required
def attendance_week(request):
    """AJAX endpoint: GET /attendance/week/?date=2026-03-14 — get week data."""
    from datetime import date as date_cls

    date_str = request.GET.get('date')
    if date_str:
        try:
            ref_date = date_cls.fromisoformat(date_str)
        except ValueError:
            ref_date = timezone.now().date()
    else:
        ref_date = timezone.now().date()

    # Get Monday of the week containing ref_date
    monday = ref_date - timedelta(days=ref_date.weekday())
    days = []
    for i in range(7):
        d = monday + timedelta(days=i)
        has_records = AttendanceRecord.objects.filter(
            student=request.user,
            date=d,
        ).exclude(status='not_marked').exists()
        days.append({
            'date': d.isoformat(),
            'day_name': d.strftime('%a'),
            'day_num': d.day,
            'has_records': has_records,
        })

    return JsonResponse({'days': days, 'monday': monday.isoformat()})
