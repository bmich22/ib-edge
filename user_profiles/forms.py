from django import forms
from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['parent_email', 'subjects']
        widgets = {
            'subjects': forms.CheckboxSelectMultiple()
        }