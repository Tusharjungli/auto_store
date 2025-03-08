from django.db import models

class Product(models.Model):
    """ ✅ Represents a product in the store """
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="product_images/")
    is_featured = models.BooleanField(default=False)  # ✅ Flag for featured products

    def __str__(self):
        return self.name
