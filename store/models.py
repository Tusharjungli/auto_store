from django.db import models
import os
import openai
from pinecone import Pinecone

# ✅ Initialize Pinecone Correctly
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index_name = os.getenv("PINECONE_INDEX_NAME")

# ✅ Function to generate AI embeddings using OpenAI
def generate_embedding(text):
    openai.api_key = os.getenv("OPENAI_API_KEY")  # 🔴 Ensure OpenAI API key is set
    response = openai.Embedding.create(
        input=text,
        model="text-embedding-ada-002"
    )
    return response['data'][0]['embedding']

# ✅ Product Model
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Generate AI embedding and save to Pinecone before saving product."""
        super().save(*args, **kwargs)  # Save product first

        # Generate AI embedding
        embedding = generate_embedding(f"{self.name} {self.description}")

        # ✅ Save embedding in Pinecone
        index = pc.Index(index_name)
        index.upsert(vectors=[
            (str(self.id), embedding, {"name": self.name, "price": str(self.price)})
        ])

    def delete(self, *args, **kwargs):
        """Remove product from Pinecone when deleted."""
        index = pc.Index(index_name)
        index.delete(ids=[str(self.id)])
        super().delete(*args, **kwargs)
