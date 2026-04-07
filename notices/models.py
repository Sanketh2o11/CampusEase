from django.db import models
from django.conf import settings


class Notice(models.Model):
    NOTICE_TYPES = [
        ('announcement', 'Announcement'),
        ('event', 'Event'),
        ('exam', 'Exam'),
        ('urgent', 'Urgent'),
        ('general', 'General'),
    ]

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notices')
    title = models.CharField(max_length=255)
    description = models.TextField()
    notice_type = models.CharField(max_length=20, choices=NOTICE_TYPES, default='general')
    is_pinned = models.BooleanField(default=False)
    image_url = models.URLField(blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    deadline = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']


class NoticePoll(models.Model):
    notice = models.OneToOneField(Notice, on_delete=models.CASCADE, related_name='poll')
    question = models.CharField(max_length=200)
    option_yes = models.CharField(max_length=100, default="Yes, I'm in")
    option_no = models.CharField(max_length=100, default="No, I'll skip")
    option_maybe = models.CharField(max_length=100, default="Maybe")

    def __str__(self):
        return f"Poll: {self.question}"


class PollVote(models.Model):
    CHOICE_OPTIONS = [
        ('yes', 'Yes'),
        ('no', 'No'),
        ('maybe', 'Maybe'),
    ]

    poll = models.ForeignKey(NoticePoll, on_delete=models.CASCADE, related_name='votes')
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='poll_votes')
    choice = models.CharField(max_length=10, choices=CHOICE_OPTIONS)

    class Meta:
        unique_together = ('poll', 'student')

    def __str__(self):
        return f"{self.student.email} voted {self.choice} on {self.poll}"


class NoticeRead(models.Model):
    notice = models.ForeignKey(Notice, on_delete=models.CASCADE, related_name='reads')
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notice_reads')
    read_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('notice', 'student')

    def __str__(self):
        return f"{self.student.email} read {self.notice.title}"
