from django import forms
from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = fields = ['first_name', 'last_name', 'grade_year', 'parent_email', 'subjects']
        widgets = {
            'subjects': forms.CheckboxSelectMultiple()
        }