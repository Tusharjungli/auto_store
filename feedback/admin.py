from django.contrib import admin
from .models import Feedback

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'category', 'submitted_at')
    list_filter = ('category', 'submitted_at')
    search_fields = ('name', 'email', 'message')
