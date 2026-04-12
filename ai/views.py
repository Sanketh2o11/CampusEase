from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Q

from attendance.models import Attendance
from exams.models import BatchExam
from notices.models import Notice, NoticeRead
from timetable.models import TimetableSlot
from core.utils import parse_json_body, compute_attendance_pct


SYSTEM_PROMPT = (
    "You are a Campus AI Assistant helping engineering students inside a campus management app.\n\n"
    "Context: {context}\n\n"
    "{injected_data}\n\n"
    "Instructions based on context:\n"
    "- If context is exams: Focus on exam preparation. Suggest what to study, not just explain. "
    "Be practical and priority-driven.\n"
    "- If context is materials: Focus on summarizing and explaining concepts clearly and concisely.\n"
    "- If context is dashboard: Help the user decide what to focus on today. "
    "Use this format strictly:\n"
    "  Focus Today:\n"
    "  • [Top priority]\n\n"
    "  Next:\n"
    "  • [Second priority]\n\n"
    "  If time:\n"
    "  • [Optional]\n\n"
    "STRICT RULES:\n"
    "- Maximum 5 lines. No extra explanation. No greetings.\n"
    "- Jump straight to actionable advice.\n"
    "- Use bullet points.\n"
    "- No markdown formatting (no bold, no headers, no asterisks).\n\n"
    "Student's question: {question}"
)


def _get_attendance_pct(user, subject):
    """Return attendance percentage for a subject, or None if no data."""
    att = Attendance.objects.filter(student=user, subject=subject).first()
    if not att:
        return None
    _, total, pct = compute_attendance_pct(att)
    return pct if total > 0 else None


def _get_all_attendance_stats(user):
    """Return list of {subject, pct} sorted low→high, only subjects with data."""
    stats = []
    for att in Attendance.objects.filter(student=user):
        pct = _get_attendance_pct(user, att.subject)
        if pct is not None:
            stats.append({'subject': att.subject, 'pct': pct})
    stats.sort(key=lambda s: s['pct'])
    return stats


def _build_dashboard_data(user):
    """Build selective, priority-sorted data for dashboard context."""
    now = timezone.now()
    today = now.date()

    # Today's classes
    day_name = today.strftime('%A').lower()
    today_classes = list(
        TimetableSlot.objects.filter(batch=user.batch, day=day_name)
        .exclude(subject_name='')
        .order_by('period')
        .values_list('subject_name', flat=True)
    ) if user.batch else []

    # Attendance — weak subjects (< 75%)
    all_stats = _get_all_attendance_stats(user)
    weak_subjects = [s for s in all_stats if s['pct'] < 75]

    # Next exam
    next_exam = None
    days_until_exam = None
    if user.batch:
        next_exam = BatchExam.objects.filter(
            batch=user.batch, exam_date__gte=today
        ).order_by('exam_date').first()
        if next_exam:
            days_until_exam = (next_exam.exam_date - today).days

    # Nearest deadline notice
    nearest_deadline = Notice.objects.filter(deadline__gte=now).order_by('deadline').first()
    deadline_days = None
    if nearest_deadline:
        deadline_days = (nearest_deadline.deadline - now).days

    # Unread notices count
    unread_count = Notice.objects.exclude(reads__student=user).count()

    # Fallback — no priorities at all
    if not next_exam and not weak_subjects and not nearest_deadline and unread_count == 0:
        return None  # signal to skip API call

    # Build priority-sorted data string
    lines = []

    # Priority 1: Exam within 3 days
    if next_exam and days_until_exam is not None and days_until_exam <= 3:
        lines.append(
            f"URGENT: {next_exam.subject} exam ({next_exam.exam_name}) in {days_until_exam} day(s)."
        )
    elif next_exam and days_until_exam is not None:
        lines.append(
            f"Next exam: {next_exam.subject} ({next_exam.exam_name}) in {days_until_exam} days."
        )

    # Priority 2: Weak attendance
    for s in weak_subjects[:2]:  # max 2 to keep it concise
        lines.append(f"Low attendance: {s['subject']} at {s['pct']}%.")

    # Priority 3: Deadline
    if nearest_deadline and deadline_days is not None:
        lines.append(
            f"Nearest deadline: \"{nearest_deadline.title}\" in {deadline_days} day(s)."
        )

    # Context info
    if today_classes:
        lines.append(f"Today's classes: {', '.join(today_classes)}.")

    if unread_count > 0:
        lines.append(f"{unread_count} unread notice(s).")

    return '\n'.join(lines)


def _build_exam_data(user, exam, days_left):
    """Build data for exam context."""
    lines = []
    lines.append(f"Subject: {exam.subject}")
    lines.append(f"Exam: {exam.exam_name} ({exam.exam_type})")

    if days_left is not None:
        lines.append(f"Days left: {days_left}")

    if exam.syllabus:
        # Truncate syllabus to avoid prompt overload
        syllabus_text = exam.syllabus[:500]
        lines.append(f"Syllabus: {syllabus_text}")

    att_pct = _get_attendance_pct(user, exam.subject)
    if att_pct is not None:
        lines.append(f"Student's attendance in {exam.subject}: {att_pct}%")
    else:
        lines.append(f"No attendance data available for {exam.subject}.")

    return '\n'.join(lines)


def _build_materials_data(user, subject):
    """Build data for materials context."""
    lines = []
    lines.append(f"Subject: {subject}")

    if user.batch:
        today = timezone.now().date()
        upcoming_exam = BatchExam.objects.filter(
            batch=user.batch, subject__iexact=subject, exam_date__gte=today
        ).order_by('exam_date').first()

        if upcoming_exam:
            days = (upcoming_exam.exam_date - today).days
            lines.append(
                f"Upcoming exam for this subject: {upcoming_exam.exam_name} in {days} day(s). "
                "Focus on key exam-relevant concepts."
            )
        else:
            lines.append("No upcoming exam for this subject.")

    return '\n'.join(lines)


class AIAssistView(LoginRequiredMixin, View):
    """Single AI endpoint — context + priority aware."""

    def post(self, request):
        data, err = parse_json_body(request)
        if err:
            return err

        context = (data.get('context') or '').strip()
        if context not in ('dashboard', 'exams', 'materials'):
            return JsonResponse({'error': 'Invalid context'}, status=400)

        question = (data.get('question') or '').strip()
        if not question:
            return JsonResponse({'error': 'Question is required'}, status=400)

        api_key = getattr(settings, 'GEMINI_API_KEY', '')
        if not api_key:
            return JsonResponse({'error': 'AI service is not configured.'}, status=503)

        user = request.user

        # --- Build injected data based on context ---
        if context == 'dashboard':
            injected_data = _build_dashboard_data(user)
            if injected_data is None:
                return JsonResponse({
                    'answer': 'No urgent priorities today. Good time to review or get ahead.'
                })

        elif context == 'exams':
            exam_id = data.get('exam_id')
            if not exam_id:
                return JsonResponse({'error': 'exam_id is required for exam context'}, status=400)
            exam = get_object_or_404(BatchExam, pk=exam_id, batch=user.batch)
            days_left = data.get('days_left')
            injected_data = _build_exam_data(user, exam, days_left)

        elif context == 'materials':
            subject = (data.get('subject') or '').strip()
            if not subject:
                return JsonResponse({'error': 'Subject is required for materials context'}, status=400)
            injected_data = _build_materials_data(user, subject)

        # --- Build prompt ---
        prompt = SYSTEM_PROMPT.format(
            context=context,
            injected_data=injected_data,
            question=question,
        )

        # --- Call Gemini ---
        try:
            from google import genai
        except ImportError:
            return JsonResponse({'error': 'AI SDK is missing on server.'}, status=503)

        try:
            client = genai.Client(api_key=api_key)
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
            )
            raw = (response.text or '').strip()
            if not raw:
                return JsonResponse({'error': 'AI returned an empty response.'}, status=502)

            # Post-process: enforce line limit
            lines = raw.split('\n')[:7]
            cleaned = '\n'.join(line for line in lines if line.strip())

        except Exception:
            return JsonResponse(
                {'error': 'Could not get a response from AI. Try again.'},
                status=502,
            )

        return JsonResponse({'answer': cleaned})
