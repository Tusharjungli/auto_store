from django.db import models
import os
import google.generativeai as genai
from pinecone import Pinecone
from django.contrib.auth.models import User
import uuid

# ✅ Configure Google Gemini AI for embeddings
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("❌ GEMINI_API_KEY is missing. Set it in your environment.")

genai.configure(api_key=GEMINI_API_KEY)

# ✅ Pinecone Setup
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")

if not PINECONE_API_KEY or not PINECONE_INDEX_NAME:
    raise ValueError("❌ Pinecone API key or index name is missing. Check your environment variables.")

# ✅ Initialize Pinecone when needed
pc = Pinecone(api_key=PINECONE_API_KEY)


def generate_embedding(text):
    """Generates AI embeddings using Google Gemini AI."""
    try:
        response = genai.embed_content(
            model="models/embedding-001",
            content=text,
            task_type="retrieval_document"
        )
        return response.get("embedding")
    except Exception as e:
        print(f"❌ Embedding Generation Failed: {e}")
        return None


# ✅ Product Model (Merged)
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)  # ✅ Added stock field
    image = models.ImageField(upload_to="product_images/", blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Generate AI embedding and save to Pinecone before saving product."""
        super().save(*args, **kwargs)  # Save product first

        # Generate AI embedding
        embedding = generate_embedding(f"{self.name} {self.description}")

        # ✅ Save embedding in Pinecone only if successful
        if embedding:
            try:
                index = pc.Index(PINECONE_INDEX_NAME)
                index.upsert(vectors=[
                    (str(self.id), embedding, {"name": self.name, "price": str(self.price)})
                ])
                print(f"✅ Product {self.id} indexed in Pinecone")
            except Exception as e:
                print(f"❌ Pinecone Upsert Failed: {e}")

    def delete(self, *args, **kwargs):
        """Remove product from Pinecone when deleted."""
        try:
            index = pc.Index(PINECONE_INDEX_NAME)
            index.delete(ids=[str(self.id)])
            print(f"🗑️ Product {self.id} removed from Pinecone")
        except Exception as e:
            print(f"❌ Pinecone Deletion Failed: {e}")
        super().delete(*args, **kwargs)


# ✅ Review Model (Moved from `products`)
class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    name = models.CharField(max_length=100, default="Anonymous")
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])  # 1-5 stars
    comment = models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.rating}⭐ for {self.product.name}"


# ✅ Subscriber Model (Moved from `products`)
class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
    

class Order(models.Model):
    STATUS_CHOICES = [
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tracking_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Processing')
    expected_delivery = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.status}"
