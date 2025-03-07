from django.shortcuts import render, get_object_or_404
from .models import Product

def product_list(request):
    query = request.GET.get('q')
    category = request.GET.get('category')
    sort_by = request.GET.get('sort')

    products = Product.objects.all()

    if query:
        products = products.filter(name__icontains=query)

    if category:
        products = products.filter(category=category)

    if sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')

    return render(request, 'products/product_list.html', {
        'products': products,
        'selected_category': category,
        'selected_sort': sort_by,
    })

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, "products/product_detail.html", {"product": product})
