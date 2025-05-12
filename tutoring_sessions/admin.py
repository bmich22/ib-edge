from django.contrib import admin
from .models import TutoringSession

# Register your models here.

@admin.register(TutoringSession)
class TutoringSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'session_datetime', 'logged_by', 'logged_on')
    list_filter = ('session_datetime', 'logged_on')
    search_fields = ('purchase__user__username', 'notes')
