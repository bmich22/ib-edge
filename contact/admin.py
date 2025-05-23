from django.contrib import admin
from .models import ContactMessage

# Register your models here.


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'timestamp', 'is_read')
    list_filter = ('is_read',)
    search_fields = ('name', 'email', 'message')
    ordering = ('-timestamp',)
    readonly_fields = ('name', 'email', 'message', 'timestamp')
    actions = ['mark_as_read']

    @admin.action(description='Mark selected messages as read')
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
