from django import forms
from urllib.parse import urlparse

from .models import Application


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = [
            "company",
            "role",
            "status",
            "applied_date",
            "logo_style",
            "logo_url",
            "logo_image",
        ]
        widgets = {"logo_url": forms.HiddenInput()}

    def clean_logo_url(self):
        logo_url = self.cleaned_data.get("logo_url", "").strip()
        if not logo_url:
            return ""

        parsed = urlparse(logo_url)
        if (
            parsed.scheme != "https"
            or parsed.hostname != "www.google.com"
            or parsed.path != "/s2/favicons"
            or "domain=" not in parsed.query
        ):
            raise forms.ValidationError("Logo URL must come from the approved logo service.")
        return logo_url

    def clean_logo_image(self):
        logo_image = self.cleaned_data.get("logo_image")
        if logo_image and logo_image.size > 5 * 1024 * 1024:
            raise forms.ValidationError("Logo files must be 5 MB or smaller.")
        if logo_image and logo_image.content_type not in {
            "image/gif",
            "image/jpeg",
            "image/png",
            "image/webp",
        }:
            raise forms.ValidationError("Upload a GIF, JPEG, PNG, or WebP image.")
        return logo_image
