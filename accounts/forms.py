from django import forms
from django.forms import ModelForm

from .models import Account


class AccountForm(forms.ModelForm):
    
    class Meta:
        model = Account
        fields = ('user', 'name', 'contact', 'status', 'notes')