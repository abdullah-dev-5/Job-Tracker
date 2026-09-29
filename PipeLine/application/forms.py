from django import forms

from .models import Application


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ["company", "role", "status", "applied_date", "logo_style"]
