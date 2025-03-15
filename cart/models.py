from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from django.utils import timezone

class Cart(models.Model):
    """ ✅ Represents a user's shopping cart """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="carts")  # ✅ Allow multiple carts per user
    created_at = models.DateTimeField(auto_now_add=True)

    def get_total_price(self):
        """ ✅ Returns the total cost of all items in the cart """
        return sum(item.total_price() for item in self.items.all())

    def has_items(self):
        """ ✅ Check if the cart has any items """
        return self.items.exists()

    def delete_if_empty(self):
        """ ✅ Delete cart if it has no items """
        if not self.has_items():
            self.delete()

    def __str__(self):
        return f"Cart {self.id} for {self.user.username}"

class CartItem(models.Model):
    """ ✅ Represents an item inside a cart """
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")  
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        """ ✅ Returns the total price of this cart item """
        return self.product.price * self.quantity  

    def save(self, *args, **kwargs):
        """ ✅ Auto-delete cart if last item is removed """
        if self.quantity < 1:
            self.delete()
        else:
            super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """ ✅ Ensure cart is deleted if it's empty after removing this item """
        cart = self.cart
        super().delete(*args, **kwargs)
        cart.delete_if_empty()  # ✅ Check if cart should be deleted

    def __str__(self):
        return f"{self.quantity} x {self.product.name} (Cart {self.cart.id})"

# ✅ Order Model
class Order(models.Model):
    """ ✅ Represents a completed order """
    STATUS_CHOICES = [
        ("Processing", "Processing"),
        ("Shipped", "Shipped"),
        ("Delivered", "Delivered"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Processing")
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Order {self.id} - {self.user.username} ({self.status})"

# ✅ OrderItem Model
class OrderItem(models.Model):
    """ ✅ Represents an item inside an order """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product_name = models.CharField(max_length=255)  # ✅ Store product name separately
    price = models.DecimalField(max_digits=10, decimal_places=2)  # ✅ Store price separately
    quantity = models.PositiveIntegerField()

    def total_price(self):
        """ ✅ Returns the total price of this order item """
        return self.price * self.quantity  

    def __str__(self):
        return f"{self.quantity} x {self.product_name} (Order {self.order.id})"
