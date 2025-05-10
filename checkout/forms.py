from django import forms


class ParentEmailForm(forms.Form):
    parent_email = forms.EmailField(label="Parent's Email", required=True)