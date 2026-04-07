from django.contrib import admin
from .models import Attendance, AttendanceRecord


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'updated_at')
    list_filter = ('subject',)
    search_fields = ('student__email', 'subject')


@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'date', 'status')
    list_filter = ('status', 'date')
    search_fields = ('student__email',)
