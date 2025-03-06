from django.shortcuts import render, redirect
from .models import CartItem
from products.models import Product
from django.contrib.auth.decorators import login_required

@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    
    if not created:
        cart_item.quantity += 1  # If already in cart, increase quantity
        cart_item.save()

    return redirect("cart_view")  # Redirect to cart page

@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = CartItem.objects.get(id=cart_item_id)
    
    if cart_item.user == request.user:  # Ensure user owns the cart item
        cart_item.delete()
    
    return redirect("cart_view")  # Redirect to cart page

@login_required
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.total_price() for item in cart_items)
    
    return render(request, "cart/cart.html", {"cart_items": cart_items, "total_price": total_price})
