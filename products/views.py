from django.shortcuts import render, get_object_or_404
from .models import Product

def product_list(request):
    """ ✅ Displays a list of all available products with search & filter options """
    products = Product.objects.all()
    
    # ✅ Get search query
    search_query = request.GET.get("q", "").strip()
    if search_query:
        products = products.filter(name__icontains=search_query)

    # ✅ Get category filter
    category_filter = request.GET.get("category", "")
    if category_filter:
        products = products.filter(category__iexact=category_filter)

    # ✅ Get price range filter
    min_price = request.GET.get("min_price", "")
    max_price = request.GET.get("max_price", "")
    
    if min_price.isdigit():
        products = products.filter(price__gte=int(min_price))
    if max_price.isdigit():
        products = products.filter(price__lte=int(max_price))

    return render(request, "products/product_list.html", {
        "products": products,
        "search_query": search_query,
        "category_filter": category_filter,
        "min_price": min_price,
        "max_price": max_price,
    })

def product_detail(request, product_id):
    """ ✅ Displays details of a single product """
    product = get_object_or_404(Product, id=product_id)
    return render(request, "products/product_detail.html", {"product": product})
