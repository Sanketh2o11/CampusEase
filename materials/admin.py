from django.contrib import admin
from .models import Material, MaterialThankYou


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'material_type', 'uploader', 'is_pinned', 'thank_you_count', 'created_at')
    list_filter = ('subject', 'material_type', 'is_pinned')
    search_fields = ('title', 'subject', 'uploader__email')


@admin.register(MaterialThankYou)
class MaterialThankYouAdmin(admin.ModelAdmin):
    list_display = ('material', 'student')
