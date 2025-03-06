from django.shortcuts import render
from products.models import Product

def homepage(request):
    """Render the homepage with featured products."""
    featured_products = Product.objects.all()[:6]  # Show 6 products
    return render(request, "index.html", {"products": featured_products})
