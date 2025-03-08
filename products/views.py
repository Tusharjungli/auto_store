from django.shortcuts import render, get_object_or_404
from .models import Product

def product_list(request):
    """ ✅ Displays a list of all available products """
    products = Product.objects.all()
    return render(request, "products/product_list.html", {"products": products})

def product_detail(request, product_id):
    """ ✅ Displays details of a single product """
    product = get_object_or_404(Product, id=product_id)
    return render(request, "products/product_detail.html", {"product": product})
