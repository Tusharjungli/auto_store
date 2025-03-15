from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from products.models import Product
from .models import Cart, CartItem, Order

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

@login_required
def checkout(request):
    """ ✅ Handles order placement and sends confirmation email """
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()

    if not cart_items:
        messages.error(request, "Your cart is empty!")
        return redirect("cart_view")

    total_price = sum(item.product.price * item.quantity for item in cart_items)

    # ✅ Create an order
    order = Order.objects.create(user=request.user, total_price=total_price)

    # ✅ Move items from cart to order
    for item in cart_items:
        order.items.add(item)

    # ✅ Clear the cart after checkout
    cart.items.all().delete()

    # ✅ Send order confirmation email
    user_email = request.user.email
    subject = "Order Confirmation - AutoSpare Parts"
    message = f"""
    Dear {request.user.username},

    Thank you for your order! 🎉

    Your order ID: {order.id}
    Total Amount: ₹{total_price}

    Our team is now processing your order. We will notify you once it is shipped. 
    You can track your order status on your profile.

    Have a great day! 🚗💨
    
    Best regards,
    AutoSpare Parts Team
    """

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user_email],
        fail_silently=False,
    )

    messages.success(request, "Order placed successfully! A confirmation email has been sent.")
    return redirect("order_success")  # Redirect to success page

@login_required
def order_success(request):
    """ ✅ Displays order success page after checkout """
    return render(request, "cart/order_success.html")

@login_required
def order_history(request):
    """ ✅ Displays the user's order history """
    orders = Order.objects.filter(user=request.user).order_by("-created_at")  # Newest first
    return render(request, "cart/order_history.html", {"orders": orders})
