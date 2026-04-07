from django import forms
from urllib.parse import urlparse
from .models import Material


class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['title', 'subject', 'drive_link', 'material_type']

    def clean_drive_link(self):
        url = self.cleaned_data.get('drive_link', '')
        if not url:
            raise forms.ValidationError("A URL is required.")
        material_type = self.cleaned_data.get('material_type', 'other')
        drive_types = ('pdf', 'ppt', 'classroom')
        if material_type in drive_types:
            # Use urlparse to check actual hostname, not substring match
            try:
                hostname = urlparse(url).hostname or ''
            except Exception:
                hostname = ''
            if 'drive.google.com' not in hostname and 'classroom.google.com' not in hostname:
                raise forms.ValidationError(
                    "Must be a valid Google Drive or Google Classroom link for this type."
                )
        return url
