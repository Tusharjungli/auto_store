from django.db import models
from django.contrib.auth.models import User
from products.models import Product

class Cart(models.Model):
    """ ✅ Shopping cart model """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="carts")  
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
    """ ✅ Items in the shopping cart """
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")  
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
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
        cart.delete_if_empty()  

    def __str__(self):
        return f"{self.quantity} x {self.product.name} (Cart {self.cart.id})"

class Order(models.Model):
    """ ✅ Order model to store placed orders """
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Shipped", "Shipped"),
        ("Delivered", "Delivered"),
        ("Cancelled", "Cancelled"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(CartItem)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.username} - {self.status}"
