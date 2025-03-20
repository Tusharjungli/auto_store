from django.shortcuts import render
from store.models import Product

def homepage(request):
    """ ✅ Renders the homepage with featured products """
    featured_products = Product.objects.filter(is_featured=True)  # ✅ Fetch featured products
    return render(request, "index.html", {"featured_products": featured_products})

def index(request):
    return render(request, 'auto_store/index.html')
