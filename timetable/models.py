from django.db import models
from accounts.models import Batch


class TimetableSlot(models.Model):
    DAY_CHOICES = [
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
    ]

    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='timetable_slots')
    day = models.CharField(max_length=10, choices=DAY_CHOICES)
    period = models.IntegerField()  # 1 through 8
    subject_name = models.CharField(max_length=100, blank=True)
    # blank = free period or no class

    class Meta:
        ordering = ['day', 'period']
        unique_together = ['batch', 'day', 'period']

    def __str__(self):
        return f"{self.batch} — {self.get_day_display()} P{self.period}: {self.subject_name or 'Free'}"
