from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import google.generativeai as genai

@csrf_exempt
def chatbot(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_message = data.get("message", "").strip()
            chat_history = data.get("chat_history", "").strip()  # Retrieve chat history from frontend

            if not user_message:
                return JsonResponse({"response": "⚠️ Please enter a message."})

            # Handle basic greetings directly
            greetings = ["hi", "hello", "hey", "good morning", "good afternoon", "good evening"]
            if user_message.lower() in greetings:
                return JsonResponse({"response": "👋 Hello! How can I assist you today?"})

            # Handle common fallback cases
            fallback_responses = [
                "I'm not sure I understand. Can you try rephrasing? 😊",
                "Hmm... I don't have an answer for that yet. Want me to connect you to support?",
                "That's a great question! Let me find that information for you. 🔍"
            ]

            # Format chat history for better AI context
            conversation = f"Previous conversation:\n{chat_history}\n\nUser: {user_message}\nBot:"

            # Generate AI response using Gemini
            model = genai.GenerativeModel("gemini-1.5-pro-latest")
            response = model.generate_content(conversation)

            if response and hasattr(response, "text"):
                bot_reply = response.text.strip()
            else:
                bot_reply = fallback_responses[0]  # Use a friendly fallback

            return JsonResponse({"response": bot_reply})

        except Exception as e:
            return JsonResponse({"response": f"❌ Oops! Something went wrong: {str(e)}"})

    return JsonResponse({"response": "⚠️ Invalid request method."})
