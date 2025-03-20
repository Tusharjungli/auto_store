from django import forms
from store.models import Subscriber, Review
from django.core.validators import MinValueValidator, MaxValueValidator

class SubscriptionForm(forms.ModelForm):
    """ ✅ Form for users to subscribe via email """
    class Meta:
        model = Subscriber
        fields = ["email"]

class ReviewForm(forms.ModelForm):
    """ ✅ Form for users to submit product reviews """
    name = forms.CharField(
        required=False,  # ✅ Make name optional
        widget=forms.TextInput(attrs={"placeholder": "Your Name (Optional)", "class": "review-name-input"})
    )
    rating = forms.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],  # ✅ Enforce rating validation (1-5)
        widget=forms.NumberInput(attrs={"min": 1, "max": 5, "class": "rating-input"})
    )
    
    class Meta:
        model = Review
        fields = ["name", "rating", "comment"]
        widgets = {
            "comment": forms.Textarea(attrs={"placeholder": "Write your review...", "rows": 4, "class": "comment-input"}),
        }
