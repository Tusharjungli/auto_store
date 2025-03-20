from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from store.models import Product, Review
from store.forms import ReviewForm
import google.generativeai as genai
import os
from pinecone import Pinecone

# ✅ Load API keys from environment
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME = "auto-store-ai"

# ✅ Set up Google Gemini AI
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    print("⚠️ Warning: GEMINI_API_KEY is missing. AI search may not work.")

# ✅ Initialize Pinecone safely
if PINECONE_API_KEY:
    pc = Pinecone(api_key=PINECONE_API_KEY)
    try:
        index_names = [index_info["name"] for index_info in pc.list_indexes()]
        if INDEX_NAME in index_names:
            index = pc.Index(INDEX_NAME)
        else:
            print(f"⚠️ Warning: Pinecone index '{INDEX_NAME}' not found.")
            index = None
    except Exception as e:
        print(f"❌ Pinecone Error: {e}")
        index = None
else:
    print("⚠️ Warning: PINECONE_API_KEY is missing.")
    index = None


def ai_search(request):
    """ ✅ AI-powered search """
    query = request.GET.get("q", "").strip()
    results = []

    if not query:
        return render(request, "store/search_results.html", {"results": [], "query": query})

    if index is None:
        print("⚠️ Pinecone is not available.")
        return render(request, "store/search_results.html", {"results": [], "query": query})

    try:
        response = genai.embed_content(
            model="models/embedding-001",
            content=query,
            task_type="retrieval_query"
        )

        query_embedding = response.get("embedding")
        if not query_embedding:
            raise ValueError("❌ No embedding received from Gemini.")

        pinecone_response = index.query(
            vector=query_embedding, top_k=10, include_metadata=True
        )
        matched_products = [int(match['id']) for match in pinecone_response.get('matches', [])]
        results = Product.objects.filter(id__in=matched_products)

    except Exception as e:
        print(f"❌ AI Search Error: {e}")
        results = []

    return render(request, "store/search_results.html", {"results": results, "query": query})


def product_detail(request, id):
    """ ✅ View for product details """
    product = get_object_or_404(Product, id=id)
    return render(request, "store/product_detail.html", {"product": product})

def submit_review(request, id):
    """ ✅ Handle product reviews """
    product = get_object_or_404(Product, id=id)

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.save()
            messages.success(request, "Review submitted successfully!")
            return redirect("product_detail", product_id=product.id)
        else:
            messages.error(request, "Error submitting review. Please check the form.")
    
    return redirect("product_detail", product_id=product.id)

def product_list(request):
    """ ✅ View all products """
    products = Product.objects.all()
    return render(request, "store/product_list.html", {"products": products})

