from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'email', 'category', 'message']
        labels = {
            'name': 'Full Name',
            'email': 'Email (Optional)',
            'category': 'Select Category',
            'message': 'Your Feedback',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your name',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email (optional)'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your feedback...',
                'rows': 4,
                'required': True
            }),
        }
