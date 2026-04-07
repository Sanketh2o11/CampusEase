from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Batch

class CustomUserAdmin(UserAdmin):
    model = User
    ordering = ('email',)
    list_display = ('email', 'full_name', 'role', 'batch', 'is_staff')
    list_filter = ('role', 'batch', 'is_staff', 'is_superuser', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('full_name', 'batch', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'role', 'batch'),
        }),
    )
    search_fields = ('email', 'full_name')

admin.site.register(User, CustomUserAdmin)
admin.site.register(Batch)
