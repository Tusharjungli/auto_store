from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from products.models import Product
from .models import Cart, CartItem

@login_required
def cart_view(request):
    """ ✅ Displays the user's shopping cart """
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()
    total_price = sum(item.total_price() if hasattr(item, "total_price") else item.product.price * item.quantity for item in cart_items)


    return render(request, "cart/cart.html", {"cart_items": cart_items, "total_price": total_price})

@login_required
def add_to_cart(request, product_id):
    """ ✅ Adds a product to the shopping cart """
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1  # ✅ If item already exists, increase quantity
    cart_item.save()

    return redirect("cart_view")

@login_required
def update_cart(request, product_id):
    """ ✅ Updates the quantity of an item in the cart """
    if request.method == "POST":
        cart = get_object_or_404(Cart, user=request.user)
        cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)

        new_quantity = int(request.POST.get("quantity", 1))
        if new_quantity > 0:
            cart_item.quantity = new_quantity
            cart_item.save()
        else:
            cart_item.delete()

    return redirect("cart_view")

@login_required
def remove_from_cart(request, product_id):
    """ ✅ Removes an item from the cart """
    cart = get_object_or_404(Cart, user=request.user)
    cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
    cart_item.delete()

    return redirect("cart_view")
