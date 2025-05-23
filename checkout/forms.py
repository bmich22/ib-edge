from django import forms
from user_profiles.models import Subject


class ParentEmailForm(forms.Form):
    customer_email = forms.EmailField(label="Buyer's Email", required=True)
    subject_choice = forms.ModelChoiceField(
        queryset=Subject.objects.all(),
        label="Select Subject",
        empty_label="Choose a subject"
    )
