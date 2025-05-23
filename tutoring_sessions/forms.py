from django import forms
from user_profiles.models import UserProfile
import datetime


class LogSessionForm(forms.Form):
    student = forms.ModelChoiceField(
        queryset=UserProfile.objects.filter(
            user__purchases__isnull=False).distinct().order_by(
                'last_name', 'first_name'),
        label="Select Student",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    session_date = forms.DateField(
        widget=forms.DateInput(
            attrs={'type': 'date', 'class': 'form-control'}),
        label="Session Date"
    )

    # Top of the hour options from 7am to 11pm
    HOUR_CHOICES = [(datetime.time(h, 0), f"{h:02}:00") for h in range(7, 23)]

    session_time = forms.ChoiceField(
        choices=HOUR_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Session Time"
    )
    notes = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['student'].label_from_instance = lambda profile:f"{profile.last_name}, {profile.first_name} ({profile.user.email})"
