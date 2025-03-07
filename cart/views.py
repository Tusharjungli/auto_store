from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product

def cart_view(request):
    """ Display the shopping cart """
    cart = request.session.get("cart", {})
    products = []

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        products.append({"product": product, "quantity": quantity})

    return render(request, "cart/cart.html", {"cart_items": products})

def add_to_cart(request, product_id):
    """ Add a product to the cart """
    cart = request.session.get("cart", {})

    if str(product_id) in cart:
        cart[str(product_id)] += 1
    else:
        cart[str(product_id)] = 1

    request.session["cart"] = cart
    return redirect("cart_view")

def remove_from_cart(request, product_id):
    """ Remove a product from the cart """
    cart = request.session.get("cart", {})

    if str(product_id) in cart:
        del cart[str(product_id)]

    request.session["cart"] = cart
    return redirect("cart_view")

def update_cart(request, product_id, action):
    """ Increase or decrease quantity of a product in the cart """
    cart = request.session.get("cart", {})

    if action == "increase":
        cart[str(product_id)] += 1
    elif action == "decrease":
        if cart[str(product_id)] > 1:
            cart[str(product_id)] -= 1
        else:
            del cart[str(product_id)]  # Remove if quantity becomes 0

    request.session["cart"] = cart
    return redirect("cart_view")

def clear_cart(request):
    """ Empty the cart """
    request.session["cart"] = {}
    return redirect("cart_view")

def increase_quantity(request, product_id):
    """ Increase the quantity of a product in the cart """
    cart = request.session.get("cart", {})

    if str(product_id) in cart:
        cart[str(product_id)] += 1  # Increase quantity

    request.session["cart"] = cart
    return redirect("cart_view")

def decrease_quantity(request, product_id):
    """ Decrease the quantity of a product in the cart """
    cart = request.session.get("cart", {})

    if str(product_id) in cart:
        if cart[str(product_id)] > 1:
            cart[str(product_id)] -= 1  # Decrease quantity
        else:
            del cart[str(product_id)]  # Remove item if quantity is 0

    request.session["cart"] = cart
    return redirect("cart_view")

