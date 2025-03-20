from django.core.management.base import BaseCommand
from store.models import Product
import google.generativeai as genai
import os

# Set up Google Gemini AI
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")  # Store API key in environment variables
genai.configure(api_key=GEMINI_API_KEY)

# Pinecone setup
from pinecone import Pinecone
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")  # Your Pinecone API Key
INDEX_NAME = "auto-store-ai"  # Your new Pinecone Index
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(INDEX_NAME)

class Command(BaseCommand):
    help = "Update all products in Pinecone using Google Gemini AI for embeddings"

    def handle(self, *args, **kwargs):
        products = Product.objects.all()
        if not products:
            self.stdout.write(self.style.WARNING("No products found in the database."))
            return

        vectors = []
        for product in products:
            text = f"{product.name} {product.description}"
            
            # Generate embedding using Google Gemini
            response = genai.embed_content(
                model="models/embedding-001", 
                content=text, 
                task_type="retrieval_document"
            )

            if response and "embedding" in response:
                embedding = response["embedding"]

                vectors.append({
                    "id": str(product.id),
                    "values": embedding,  # Now correctly 768-dimension
                    "metadata": {
                        "name": product.name,
                        "description": product.description,
                        "price": str(product.price),
                    }
                })
        
        if vectors:
            index.upsert(vectors=vectors)
            self.stdout.write(self.style.SUCCESS(f"✅ Updated {len(vectors)} products in Pinecone using Gemini AI."))

