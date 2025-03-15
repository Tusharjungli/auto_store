from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse  # ✅ Import for AJAX response
from .forms import FeedbackForm
from .models import Feedback

def feedback_view(request):
    """Handles feedback form submission via AJAX or normal request."""
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":  # ✅ Check if AJAX request
                return JsonResponse({"success": True, "message": "Thank you for your feedback!"})
            messages.success(request, "Thank you for your feedback!")  # ✅ Normal success message
            return redirect("feedback_success")  # ✅ Redirect for normal request
        else:
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return JsonResponse({"success": False, "errors": form.errors}, status=400)

    else:
        form = FeedbackForm()

    return render(request, "feedback/feedback.html", {"form": form})

def feedback_success(request):
    """Displays a success message after feedback submission."""
    return render(request, "feedback/feedback_success.html")

def feedback_list(request):
    """Displays the list of submitted feedback (latest first)."""
    feedbacks = Feedback.objects.order_by('-submitted_at')
    return render(request, "feedback/feedback_list.html", {"feedbacks": feedbacks})
