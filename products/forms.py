from django import forms
from .models import Subscriber, Review

class SubscriptionForm(forms.ModelForm):
    """ ✅ Form for users to subscribe via email """
    class Meta:
        model = Subscriber
        fields = ["email"]

class ReviewForm(forms.ModelForm):
    """ ✅ Form for users to submit product reviews """
    class Meta:
        model = Review
        fields = ["name", "rating", "comment"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Your Name (Optional)", "class": "review-name-input"}),
            "rating": forms.NumberInput(attrs={"min": 1, "max": 5, "class": "rating-input"}),
            "comment": forms.Textarea(attrs={"placeholder": "Write your review...", "rows": 4, "class": "comment-input"}),
        }
