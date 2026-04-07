from django.contrib import admin
from .models import TimetableSlot


@admin.register(TimetableSlot)
class TimetableSlotAdmin(admin.ModelAdmin):
    list_display = ('batch', 'day', 'period', 'subject_name')
    list_filter = ('batch', 'day')
    ordering = ('batch', 'day', 'period')
