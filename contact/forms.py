from django import forms
from .models import ContactMessage


class ContactForm(forms.ModelForm):
    # Honeypot field (form spam protection)
    bot_field = forms.CharField(
        required=False,
        widget=forms.HiddenInput,
        label="Leave empty"
    )

    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your name',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your email',
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Your message',
                'rows': 5,
            }),
        }
