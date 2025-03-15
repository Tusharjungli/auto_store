from django.db import models

class Feedback(models.Model):
    CATEGORY_CHOICES = [
        ('suggestion', 'Suggestion'),
        ('bug', 'Bug Report'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=100, verbose_name="Full Name")
    email = models.EmailField(blank=True, default="", verbose_name="Email (Optional)")
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='suggestion',
        verbose_name="Feedback Category"
    )
    message = models.TextField(verbose_name="Your Message")
    submitted_at = models.DateTimeField(auto_now_add=True, verbose_name="Submitted At")

    class Meta:
        ordering = ['-submitted_at']  # Show newest feedback first
        verbose_name = "Feedback"
        verbose_name_plural = "Feedback Entries"

    def __str__(self):
        return f"{self.name} - {self.category} ({self.submitted_at.strftime('%Y-%m-%d %H:%M')})"
