from django.shortcuts import render, get_object_or_404
from .models import Product

def product_list(request):
    """ ✅ Displays a list of products with search and filtering """
    query = request.GET.get("q", "")  # ✅ Get search query
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")
    is_featured = request.GET.get("is_featured")

    products = Product.objects.all()

    # ✅ Apply search filter
    if query:
        products = products.filter(name__icontains=query)

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
    """ ✅ Displays details of a single product """
    product = get_object_or_404(Product, id=product_id)
    return render(request, "products/product_detail.html", {"product": product})
