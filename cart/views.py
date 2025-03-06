from django.shortcuts import render, redirect, get_object_or_404
from .models import CartItem
from products.models import Product
from django.contrib.auth.decorators import login_required

@login_required
def add_to_cart(request, product_id):
    """ Adds a product to the cart or increases its quantity if already added. """
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    
    if not created:
        cart_item.quantity += 1  # Increase quantity if already in cart
        cart_item.save()

    return redirect("cart_view")

@login_required
def remove_from_cart(request, cart_item_id):
    """ Removes a product from the cart. """
    cart_item = get_object_or_404(CartItem, id=cart_item_id, user=request.user)
    cart_item.delete()
    return redirect("cart_view")

@login_required
def increase_quantity(request, cart_item_id):
    """ Increases the quantity of a product in the cart. """
    cart_item = get_object_or_404(CartItem, id=cart_item_id, user=request.user)
    cart_item.quantity += 1
    cart_item.save()
    return redirect("cart_view")

@login_required
def decrease_quantity(request, cart_item_id):
    """ Decreases the quantity of a product in the cart. If quantity is 1, removes the item. """
    cart_item = get_object_or_404(CartItem, id=cart_item_id, user=request.user)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()  # Remove item if quantity reaches 0

    return redirect("cart_view")

@login_required
def cart_view(request):
    """ Displays the cart with all items and total price. """
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.total_price() for item in cart_items)
    
    return render(request, "cart/cart.html", {"cart_items": cart_items, "total_price": total_price})
