import os
import google.generativeai as genai
from pinecone import Pinecone

# ✅ Load API Key securely
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("⚠️ ERROR: GEMINI_API_KEY is missing! Please set it in your environment variables.")

# ✅ Initialize AI Model
genai.configure(api_key=GEMINI_API_KEY)

# ✅ Pinecone Setup
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
if not PINECONE_API_KEY:
    raise ValueError("⚠️ ERROR: PINECONE_API_KEY is missing! Please set it in your environment variables.")

pinecone = Pinecone(api_key=PINECONE_API_KEY)
