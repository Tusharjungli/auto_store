from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from products.models import Product
from .models import Cart, CartItem

@login_required
def cart_view(request):
    """ ✅ Displays the user's shopping cart """
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()
    total_price = sum(item.product.price * item.quantity for item in cart_items)

    return render(request, "cart/cart.html", {"cart_items": cart_items, "total_price": total_price})

@login_required
def add_to_cart(request, product_id):
    """ ✅ Adds a product to the shopping cart via AJAX or redirect """
    product = get_object_or_404(Product, id=product_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    # ✅ Fetch updated cart count
    cart_count = sum(item.quantity for item in cart.items.all())

    # ✅ Return JSON response for AJAX requests
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({"success": True, "cart_count": cart_count})

    return redirect("cart_view")

@login_required
def update_cart(request, product_id):
    """ ✅ Updates the quantity of an item in the cart via AJAX """
    if request.method == "POST" and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        cart = get_object_or_404(Cart, user=request.user)
        cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)

        try:
            new_quantity = int(request.POST.get("quantity", 1))
            if new_quantity > 0:
                cart_item.quantity = new_quantity
                cart_item.save()
            else:
                cart_item.delete()
        except ValueError:
            return JsonResponse({"success": False, "error": "Invalid quantity"}, status=400)

        # ✅ Fetch updated cart data
        cart_items = cart.items.all()
        total_price = sum(item.product.price * item.quantity for item in cart_items)
        item_total = cart_item.product.price * cart_item.quantity if new_quantity > 0 else 0
        cart_count = sum(item.quantity for item in cart_items)

        return JsonResponse({"success": True, "cart_total": total_price, "item_total": item_total, "cart_count": cart_count})

    return JsonResponse({"success": False}, status=400)

@login_required
def remove_from_cart(request, product_id):
    """ ✅ Removes an item from the cart via AJAX """
    if request.method == "POST" and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        cart = get_object_or_404(Cart, user=request.user)
        cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
        cart_item.delete()

        # ✅ Fetch updated cart data
        cart_items = cart.items.all()
        total_price = sum(item.product.price * item.quantity for item in cart_items)
        cart_count = sum(item.quantity for item in cart_items)

        return JsonResponse({"success": True, "cart_total": total_price, "cart_count": cart_count})

    return JsonResponse({"success": False}, status=400)

@login_required
def get_cart_count(request):
    """ ✅ Returns the total number of items in the cart for navbar """
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_count = sum(item.quantity for item in cart.items.all())
    return JsonResponse({"cart_count": cart_count})
