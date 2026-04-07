from django.db import models
from django.conf import settings


class Material(models.Model):
    MATERIAL_TYPES = [
        ('classroom', 'Google Classroom'),
        ('pdf', 'Drive PDF'),
        ('ppt', 'Drive PPT'),
        ('youtube', 'YouTube'),
        ('other', 'Other'),
    ]

    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='materials')
    title = models.CharField(max_length=255)
    subject = models.CharField(max_length=200)
    drive_link = models.URLField(max_length=500, help_text="Must be a valid Google Drive link")
    material_type = models.CharField(max_length=20, choices=MATERIAL_TYPES, default='other')
    is_pinned = models.BooleanField(default=False)
    thank_you_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.subject})"

    class Meta:
        ordering = ['-created_at']


class MaterialThankYou(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='thank_yous')
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='material_thanks')

    class Meta:
        unique_together = ('material', 'student')

    def __str__(self):
        return f"{self.student.email} thanked {self.material.title}"
