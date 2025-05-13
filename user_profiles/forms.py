from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, Subject 


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = fields = ['first_name', 'last_name', 'grade_year', 'parent_email', 'subjects']
        widgets = {
            'subjects': forms.CheckboxSelectMultiple()
        }