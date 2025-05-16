from django import forms
from user_profiles.models import Subject


class ParentEmailForm(forms.Form):
    parent_email = forms.EmailField(label="Parent's Email", required=True)
    subject = forms.ModelChoiceField(
        queryset=Subject.objects.all(),
        label="Select Subject",
        empty_label="Choose a subject"
    )