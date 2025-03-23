from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import google.generativeai as genai

@csrf_exempt
def chatbot(request):
    if request.method != "POST":
        return JsonResponse({"response": "⚠️ Invalid request method."}, status=405)

    try:
        # Load request data
        data = json.loads(request.body)
        user_message = data.get("message", "").strip()
        chat_history = data.get("chat_history", "").strip() if data.get("chat_history") else ""

        if not user_message:
            return JsonResponse({"response": "⚠️ Please enter a message."}, status=400)

        # Handle basic greetings
        greetings = ["hi", "hello", "hey", "good morning", "good afternoon", "good evening"]
        if user_message.lower() in greetings:
            return JsonResponse({"response": "👋 Hello! How can I assist you today?"})

        # Fallback responses
        fallback_responses = [
            "I'm not sure I understand. Can you try rephrasing? 😊",
            "Hmm... I don't have an answer for that yet. Want me to connect you to support?",
            "That's a great question! Let me find that information for you. 🔍"
        ]

        # Prepare conversation history
        conversation = f"Previous conversation:\n{chat_history}\n\nUser: {user_message}\nBot:"

        # Generate AI response using Gemini
        model = genai.GenerativeModel("gemini-1.5-pro-latest")
        response = model.generate_content(conversation)

        bot_reply = response.text.strip() if response and hasattr(response, "text") else fallback_responses[0]

        return JsonResponse({"response": bot_reply})

    except json.JSONDecodeError:
        return JsonResponse({"response": "⚠️ Invalid JSON format. Please check your request."}, status=400)

    except Exception as e:
        return JsonResponse({"response": f"❌ Oops! Something went wrong: {str(e)}"}, status=500)
