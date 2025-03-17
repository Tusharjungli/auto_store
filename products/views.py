from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from .models import Product, Review
from .forms import ReviewForm
from django.contrib import messages
from django.http import JsonResponse

def product_list(request):
    """ ✅ AI-Powered Search & Filtering for Products """
    query = request.GET.get("q", "").strip()  # ✅ Get search query
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")
    is_featured = request.GET.get("is_featured")

    products = Product.objects.all()

    # ✅ AI-Powered Search (Typo Correction & Relevance)
    if query:
        search_query = SearchQuery(query)
        products = products.annotate(
            search=SearchVector("name", "description")
        ).filter(search=search_query).order_by("-id")

    # ✅ Apply price range filter
    if min_price and min_price.isdigit():
        products = products.filter(price__gte=float(min_price))
    if max_price and max_price.isdigit():
        products = products.filter(price__lte=float(max_price))

    # ✅ Apply featured filter
    if is_featured == "true":
        products = products.filter(is_featured=True)

    return render(request, "products/product_list.html", {
        "products": products,
        "query": query,
        "min_price": min_price,
        "max_price": max_price,
        "is_featured": is_featured,
    })

def product_detail(request, product_id):
    """ ✅ Displays details of a single product with reviews """
    product = get_object_or_404(Product, id=product_id)
    reviews = Review.objects.filter(product=product).order_by("-created_at")
    form = ReviewForm()

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.save()
            messages.success(request, "✅ Review submitted successfully!")
            return redirect("product_detail", product_id=product.id)

    return render(request, "products/product_detail.html", {
        "product": product,
        "reviews": reviews,
        "form": form,
    })

def submit_review(request, product_id):
    """ ✅ Handles AJAX review submission """
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.save()
            return JsonResponse({"success": True, "message": "✅ Review submitted successfully!"})

        return JsonResponse({"success": False, "message": "❌ Invalid form submission."})

    return JsonResponse({"success": False, "message": "❌ Invalid request method."})
