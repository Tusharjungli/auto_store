from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import google.generativeai as genai

@csrf_exempt
def chatbot(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_message = data.get("message", "")

            if not user_message:
                return JsonResponse({"response": "⚠️ Please enter a message."})

            # Generate AI response using Gemini
            model = genai.GenerativeModel("gemini-1.5-pro-latest")
            response = model.generate_content(user_message)
            bot_reply = response.text if response and hasattr(response, "text") else "⚠️ Error: No response from AI."

            return JsonResponse({"response": bot_reply})

        except Exception as e:
            return JsonResponse({"response": f"❌ Error: {str(e)}"})

    return JsonResponse({"response": "⚠️ Invalid request method."})
