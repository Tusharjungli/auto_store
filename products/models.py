from django.db import models
from django.contrib.postgres.search import SearchVectorField

class Product(models.Model):
    """ ✅ Represents a product in the store """
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="product_images/")
    is_featured = models.BooleanField(default=False)  # ✅ Flag for featured products
    search_vector = SearchVectorField(null=True, blank=True)  # ✅ Search Index Field

    def __str__(self):
        return self.name

class Review(models.Model):
    """ ✅ Stores product reviews """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    name = models.CharField(max_length=100, default="Anonymous")
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])  # 1-5 stars
    comment = models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.rating}⭐ for {self.product.name}"

class Subscriber(models.Model):
    """ ✅ Stores email subscribers """
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
