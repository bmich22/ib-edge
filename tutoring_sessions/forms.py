from django import forms
from user_profiles.models import UserProfile


class LogSessionForm(forms.Form):
    student = forms.ModelChoiceField(
        queryset=UserProfile.objects.filter(user__purchases__isnull=False).distinct().order_by('last_name', 'first_name'),
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['student'].label_from_instance = lambda profile: f"{profile.last_name}, {profile.first_name} ({profile.user.email})"