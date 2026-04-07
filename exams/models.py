from django.db import models
from django.conf import settings
from accounts.models import Batch


class BatchExam(models.Model):
    """Batch-wide exam schedule created by CR. Visible to all students in the batch."""
    EXAM_TYPES = [
        ('internal', 'Internal'),
        ('external', 'External'),
    ]

    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='batch_exams')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_exams')
    subject = models.CharField(max_length=100)
    exam_name = models.CharField(max_length=200)
    exam_type = models.CharField(max_length=20, choices=EXAM_TYPES)
    exam_date = models.DateField()
    syllabus = models.TextField(blank=True)

    class Meta:
        ordering = ['-exam_date']

    def __str__(self):
        return f"{self.exam_name} — {self.subject} ({self.exam_date})"


class PersonalExamResult(models.Model):
    """Private per-student result linked to a batch exam."""
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='exam_results')
    batch_exam = models.ForeignKey(BatchExam, on_delete=models.CASCADE, null=True, blank=True, related_name='results')
    score = models.CharField(max_length=20, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ('student', 'batch_exam')

    def __str__(self):
        exam_label = self.batch_exam.exam_name if self.batch_exam else 'Unlinked'
        return f"{self.student.email} — {exam_label}: {self.score}"
