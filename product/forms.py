# forms.py
from django import forms
from .models import PriceAdjustment

class PriceAdjustmentForm(forms.ModelForm):
    class Meta:
        model = PriceAdjustment
        fields = ['product', 'new_price', 'reason']
