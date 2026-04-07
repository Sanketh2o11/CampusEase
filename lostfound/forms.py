from django import forms
from .models import LostFoundItem


class LostFoundItemForm(forms.ModelForm):
    class Meta:
        model = LostFoundItem
        fields = ['title', 'description', 'image_url', 'status', 'contact_info', 'last_seen_location']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'image_url': forms.URLInput(attrs={'placeholder': 'e.g., Imgur link (optional)'}),
        }

    def clean_contact_info(self):
        contact = self.cleaned_data.get('contact_info', '').strip()
        if not contact:
            raise forms.ValidationError("Contact info is required. Provide a phone number or room/location.")
        return contact
