from django.contrib import admin
from .models import Notice, NoticePoll, PollVote, NoticeRead


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'notice_type', 'is_pinned', 'deadline', 'created_at')
    list_filter = ('notice_type', 'is_pinned', 'author', 'deadline')
    search_fields = ('title', 'description', 'author__email')


@admin.register(NoticePoll)
class NoticePollAdmin(admin.ModelAdmin):
    list_display = ('question', 'notice')


@admin.register(PollVote)
class PollVoteAdmin(admin.ModelAdmin):
    list_display = ('poll', 'student', 'choice')
    list_filter = ('choice',)


@admin.register(NoticeRead)
class NoticeReadAdmin(admin.ModelAdmin):
    list_display = ('notice', 'student', 'read_at')
