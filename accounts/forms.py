from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Batch

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'full_name', 'batch')
    
    # We do not include "role" in the registration form because CRs are manually set via the Django Admin
