from django.db import models

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('engine', 'Engine Parts'),
        ('brake', 'Brake System'),
        ('lights', 'Lights & Indicators'),
        ('battery', 'Battery & Electrical'),
        ('accessory', 'Accessories'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_images/')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='accessory')

    def __str__(self):
        return self.name
