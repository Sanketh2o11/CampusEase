from django.db import models
from django.conf import settings


class LostFoundItem(models.Model):
    STATUS_CHOICES = [
        ('lost', 'Lost'),
        ('found', 'Found'),
    ]

    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reported_items')
    title = models.CharField(max_length=255)
    description = models.TextField()
    image_url = models.URLField(max_length=500, blank=True, null=True, help_text="Optional image link for the item")
    contact_info = models.CharField(max_length=200, help_text="Phone number or location like 'find me in Room 204'")
    last_seen_location = models.CharField(max_length=200, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    is_resolved = models.BooleanField(default=False, help_text="CR drops this to True once resolved")
    claimed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='claimed_items'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.get_status_display()}] {self.title}"

    class Meta:
        ordering = ['is_resolved', '-created_at']
