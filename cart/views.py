from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from store.models import Product
from .models import Cart, CartItem, Order, OrderItem

@login_required(login_url='/auth/login/')  # ✅ Ensures users are redirected properly if logged out
def cart_view(request):
    """ ✅ Displays the user's shopping cart """
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.select_related("product").all()  # ✅ Optimized query
    total_price = sum(item.product.price * item.quantity for item in cart_items)

    return render(request, "cart/cart.html", {"cart_items": cart_items, "total_price": total_price})

@login_required(login_url='/auth/login/')
def add_to_cart(request, product_id):
    """ ✅ Adds a product to the shopping cart via AJAX or redirect """
    product = get_object_or_404(Product, id=product_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    cart_count = sum(item.quantity for item in cart.items.all())

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({"success": True, "cart_count": cart_count})

    return redirect("cart_view")

@login_required(login_url='/auth/login/')
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

        cart_items = cart.items.select_related("product").all()
        total_price = sum(item.product.price * item.quantity for item in cart_items)
        item_total = cart_item.product.price * cart_item.quantity if new_quantity > 0 else 0
        cart_count = sum(item.quantity for item in cart_items)

        return JsonResponse({"success": True, "cart_total": total_price, "item_total": item_total, "cart_count": cart_count})

    return JsonResponse({"success": False}, status=400)

@login_required(login_url='/auth/login/')
def remove_from_cart(request, product_id):
    """ ✅ Removes an item from the cart via AJAX """
    if request.method == "POST" and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        cart = get_object_or_404(Cart, user=request.user)
        cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
        cart_item.delete()

        cart_items = cart.items.select_related("product").all()
        total_price = sum(item.product.price * item.quantity for item in cart_items)
        cart_count = sum(item.quantity for item in cart_items)

        return JsonResponse({"success": True, "cart_total": total_price, "cart_count": cart_count})

    return JsonResponse({"success": False}, status=400)

@login_required(login_url='/auth/login/')
def get_cart_count(request):
    """ ✅ Returns the total number of items in the cart for navbar """
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_count = sum(item.quantity for item in cart.items.all())
    return JsonResponse({"cart_count": cart_count})

@login_required(login_url='/auth/login/')
def checkout(request):
    """ ✅ Handles order placement and sends a confirmation email """
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.select_related("product").all()

    if not cart_items:
        messages.error(request, "Your cart is empty!")
        return redirect("cart_view")

    total_price = sum(item.product.price * item.quantity for item in cart_items)

    # ✅ Create an order
    order = Order.objects.create(user=request.user, total_price=total_price)

    # ✅ Move items from cart to order
    order_items = [
        OrderItem(
            order=order,
            product_name=item.product.name,
            price=item.product.price,
            quantity=item.quantity,
        ) for item in cart_items
    ]
    OrderItem.objects.bulk_create(order_items)  # ✅ Optimized bulk insert

    # ✅ Clear the cart
    cart.items.all().delete()

    # ✅ Send order confirmation email
    user_email = request.user.email
    if user_email:
        subject = "Order Confirmation - AutoSpare Parts"
        message = f"""
        Dear {request.user.username},

        🎉 Thank you for your order! 🎉

        Order ID: {order.id}
        Total Amount: ₹{total_price}

        We are processing your order and will notify you when it's shipped.
        You can track your order in your profile.

        🚗 Happy Shopping!
        
        Regards,
        AutoSpare Parts Team
        """

        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user_email], fail_silently=False)

    messages.success(request, "Order placed successfully! A confirmation email has been sent.")
    return redirect(reverse("order_success"))  # ✅ Fix: Redirects correctly

@login_required(login_url='/auth/login/')
def order_history(request):
    """ ✅ Displays the user's order history """
    orders = Order.objects.filter(user=request.user).prefetch_related("items")
    return render(request, "cart/order_history.html", {"orders": orders})

@login_required(login_url='/auth/login/')
def order_success(request):
    """ ✅ Displays the order success page """
    return render(request, "cart/order_success.html")
