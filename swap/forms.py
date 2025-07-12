# swap/forms.py
from django import forms
from .models import Swap

class SwapForm(forms.ModelForm):
    class Meta:
        model = Swap
        fields = ['message']  # ✅ only valid field to take from user
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Optional message for the receiver...'})
        }
