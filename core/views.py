import json
from datetime import timedelta
from math import ceil, floor

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.utils import timezone
from django.db.models import Q

from attendance.models import Attendance, AttendanceRecord
from notices.models import Notice, NoticeRead
from materials.models import Material
from lostfound.models import LostFoundItem
from exams.models import BatchExam


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'core/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        now = timezone.now()
        today = now.date()

        # 1. Top 4 recent notices
        context['recent_notices'] = Notice.objects.all().order_by('-created_at')[:4]

        # Upcoming Deadline
        upcoming_notice = Notice.objects.filter(deadline__gte=now).order_by('deadline').first()
        if upcoming_notice:
            delta = upcoming_notice.deadline - now
            context['upcoming_notice'] = upcoming_notice
            context['notice_deadline_days'] = delta.days

        # Quick Stats for User
        context['uploaded_materials_count'] = Material.objects.filter(uploader=user).count()
        context['open_lostfound_count'] = LostFoundItem.objects.filter(reporter=user, is_resolved=False).count()

        # Unread notices count — count notices the user hasn't read yet
        context['unread_notices_count'] = Notice.objects.exclude(
            reads__student=user
        ).count()

        # Attendance summary & alerts (for ALL users, not just students)
        attendances = list(Attendance.objects.filter(student=user).prefetch_related('records'))
        attendance_stats = []
        for att in attendances:
            records = att.records.all()
            total_r = records.filter(~Q(status='not_marked')).count()
            attended_r = records.filter(status='present').count()
            pct = round((attended_r / total_r) * 100, 1) if total_r > 0 else 0.0
            attendance_stats.append({
                'subject': att.subject,
                'percentage': pct,
                'attended': attended_r,
                'total': total_r,
            })

        # Sort low → high so at-risk subjects are shown first
        attendance_stats_sorted = sorted(attendance_stats, key=lambda s: s['percentage'])

        context['attendance_records'] = attendance_stats_sorted[:6]
        context['tracked_subjects_count'] = len(attendance_stats)
        context['attendance_all_json'] = json.dumps([
            {'subject': s['subject'], 'percentage': s['percentage'],
             'attended': s['attended'], 'total': s['total']}
            for s in attendance_stats_sorted
        ])

        # Attendance warnings — subjects below 65%
        context['attendance_warnings'] = [s for s in attendance_stats if s['total'] > 0 and s['percentage'] < 65]

        if attendance_stats:
            alert_status = 'green'
            alert_subject = ''
            for s in attendance_stats:
                if s['total'] > 0 and s['percentage'] < 65:
                    alert_status = 'red'
                    alert_subject = s['subject']
                    break
                elif s['total'] > 0 and s['percentage'] < 75 and alert_status != 'red':
                    alert_status = 'yellow'
                    alert_subject = s['subject']

            if alert_status == 'green':
                alert_subject = 'All subjects'

            context['attendance_alert'] = {
                'status': alert_status,
                'subject': alert_subject,
            }

        # Upcoming batch exams (next 3)
        if user.batch:
            upcoming_exams = BatchExam.objects.filter(
                batch=user.batch, exam_date__gte=today
            ).order_by('exam_date')[:3]
            context['upcoming_exams'] = upcoming_exams

            # Next exam countdown
            next_exam = upcoming_exams.first() if upcoming_exams.exists() else None
            if next_exam:
                context['days_until_next_exam'] = (next_exam.exam_date - today).days
            else:
                context['days_until_next_exam'] = None

            # Build all batch exams for timeline
            all_exams = BatchExam.objects.filter(batch=user.batch).order_by('exam_date')
            exam_timeline = []
            for exam in all_exams:
                exam_timeline.append({
                    'id': exam.id,
                    'name': exam.exam_name,
                    'subject': exam.subject,
                    'date': exam.exam_date.isoformat(),
                    'date_display': exam.exam_date.strftime('%b %d'),
                    'type': exam.exam_type,
                    'is_past': exam.exam_date < today,
                })
            context['exam_timeline'] = exam_timeline
            context['exam_timeline_json'] = json.dumps(exam_timeline)
        else:
            context['upcoming_exams'] = []
            context['days_until_next_exam'] = None
            context['exam_timeline'] = []
            context['exam_timeline_json'] = json.dumps([])

        # 7-day ambient strip (Section G3) — batch queries to avoid N+1
        monday = today - timedelta(days=today.weekday())
        week_end = monday + timedelta(days=6)

        # Fetch all exam dates and deadline dates in the week in ONE query each
        exam_dates_this_week = set()
        if user.batch:
            exam_dates_this_week = set(
                BatchExam.objects.filter(
                    batch=user.batch,
                    exam_date__gte=monday,
                    exam_date__lte=week_end,
                ).values_list('exam_date', flat=True)
            )

        deadline_dates_this_week = set(
            Notice.objects.filter(
                deadline__date__gte=monday,
                deadline__date__lte=week_end,
            ).values_list('deadline__date', flat=True)
        )

        week_events = []
        for i in range(7):
            d = monday + timedelta(days=i)
            week_events.append({
                'date': d.isoformat(),
                'day_short': d.strftime('%a')[:2],
                'day_num': d.day,
                'is_today': d == today,
                'has_exam': d in exam_dates_this_week,
                'has_deadline': d in deadline_dates_this_week,
            })

        context['week_events'] = week_events
        context['week_events_json'] = json.dumps(week_events)

        return context
