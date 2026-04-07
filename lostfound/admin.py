from django.contrib import admin
from .models import LostFoundItem


@admin.register(LostFoundItem)
class LostFoundItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'reporter', 'is_resolved', 'claimed_by', 'created_at')
    list_filter = ('status', 'is_resolved')
    search_fields = ('title', 'description', 'reporter__email')
