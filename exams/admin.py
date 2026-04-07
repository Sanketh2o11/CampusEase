from django.contrib import admin
from .models import BatchExam, PersonalExamResult


@admin.register(BatchExam)
class BatchExamAdmin(admin.ModelAdmin):
    list_display = ('exam_name', 'subject', 'exam_type', 'batch', 'exam_date', 'created_by')
    list_filter = ('exam_type', 'exam_date', 'batch')
    search_fields = ('exam_name', 'subject')


@admin.register(PersonalExamResult)
class PersonalExamResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'batch_exam', 'score')
    list_filter = ('batch_exam',)
    search_fields = ('student__email',)
