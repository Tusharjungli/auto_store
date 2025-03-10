from .models import Cart

def cart_context(request):
    """ ✅ Adds cart-related data to all templates """
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_count = sum(item.quantity for item in cart.items.all())
    else:
        cart_count = 0  # No cart for anonymous users

    return {"cart_count": cart_count}
