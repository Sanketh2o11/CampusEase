from django.db import models
from django.conf import settings


class Attendance(models.Model):
    """Subject metadata per student. No longer stores counts — computed from AttendanceRecord."""
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='attendances')
    subject = models.CharField(max_length=200)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['student', 'subject']

    def __str__(self):
        return f"{self.subject} - {self.student.email}"


class AttendanceRecord(models.Model):
    """Daily attendance marking per subject per student."""
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('not_marked', 'Not Marked'),
    ]

    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='attendance_records')
    subject = models.ForeignKey(Attendance, on_delete=models.CASCADE, related_name='records')
    date = models.DateField()
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default='not_marked')

    class Meta:
        unique_together = ('student', 'subject', 'date')
        ordering = ['-date']

    def __str__(self):
        return f"{self.student.email} — {self.subject.subject} — {self.date} — {self.status}"
