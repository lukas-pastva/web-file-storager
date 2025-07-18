from django import forms
from django.conf import settings
from pathlib import Path
from django.core.exceptions import ValidationError


class MediaUploadForm(forms.Form):
    file = forms.FileField(label="Vyber súbor")

    def clean_file(self):
        f = self.cleaned_data["file"]
        ext = Path(f.name).suffix.lower()
        if ext not in settings.ALLOWED_MEDIA_EXTS:
            raise ValidationError("Nepovolený typ súboru.")
        return f
