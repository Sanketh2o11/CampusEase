import json

from django.http import JsonResponse


def parse_json_body(request):
    """
    Parse a JSON request body.
    Returns (data, None) on success, or (None, JsonResponse(400)) on failure.

    Usage:
        data, err = parse_json_body(request)
        if err:
            return err
    """
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, AttributeError):
        return None, JsonResponse({'error': 'Invalid JSON'}, status=400)
    return data, None


def compute_attendance_pct(attendance_obj):
    """
    Return (attended, total, pct) for an Attendance instance.
    Excludes 'not_marked' records from the total. pct is 0.0 when total is 0.
    """
    from django.db.models import Q
    records = attendance_obj.records.all()
    total = records.filter(~Q(status='not_marked')).count()
    attended = records.filter(status='present').count()
    pct = round((attended / total) * 100, 1) if total > 0 else 0.0
    return attended, total, pct


def get_poll_counts(poll):
    """Return yes/no/maybe vote counts for a NoticePoll."""
    return {
        'yes_count': poll.votes.filter(choice='yes').count(),
        'no_count': poll.votes.filter(choice='no').count(),
        'maybe_count': poll.votes.filter(choice='maybe').count(),
    }
