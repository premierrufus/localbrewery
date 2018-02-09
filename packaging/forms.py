from django import forms
from .models import PackagingEvent


class PackForm(forms.ModelForm):

    class Meta:
        model = PackagingEvent
        fields = ('packager', 'brewing_event', 'packaging_date', 'formats')
   