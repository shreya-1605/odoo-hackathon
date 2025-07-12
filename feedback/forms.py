from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['comment', 'rating']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Leave a comment...'}),
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
        }
