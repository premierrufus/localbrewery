from django import forms
from django.forms import ModelForm

from .models import BrewingEvent


class BatchForm(forms.ModelForm):
    
    class Meta:
        model = BrewingEvent
        fields = ('brewer', 'brew_date', 'batch_number')

