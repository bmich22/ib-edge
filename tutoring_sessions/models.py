from django.db import models
from django.contrib.auth.models import User


class TutoringSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tutoring_sessions')
    session_datetime = models.DateTimeField()
    notes = models.TextField(blank=True)
    logged_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='logged_sessions')
    logged_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} — {self.session_datetime.strftime('%b %d, %Y %I:%M %p')}"