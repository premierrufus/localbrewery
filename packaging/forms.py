from django import forms

from .models import PackagingEvent


class PackForm(forms.ModelForm):
    
    class Meta:
        model = PackagingEvent
        fields = ('user', 'packaged_beer', 'packaging_date', 'packaged_beer_format', 'packaged_quantity')
