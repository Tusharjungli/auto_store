from django import forms
from .models import Subscriber

class SubscriptionForm(forms.ModelForm):
    """ ✅ Form for users to subscribe via email """
    class Meta:
        model = Subscriber
        fields = ["email"]
