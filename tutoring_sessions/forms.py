# tutoring_sessions/forms.py
from django import forms
from django.contrib.auth.models import User


class LogSessionForm(forms.Form):
    student = forms.ModelChoiceField(
        queryset=User.objects.filter(purchases__isnull=False).distinct(),
        label="Select Student",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    session_datetime = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        label="Session Date and Time"
    )
    notes = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        required=False
    )