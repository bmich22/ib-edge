from django.contrib import admin
from .models import TutoringSession


@admin.register(TutoringSession)
class TutoringSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'session_datetime', 'logged_by', 'logged_on')
    list_filter = ('session_datetime', 'logged_on')
    search_fields = ('user__username', 'notes')
