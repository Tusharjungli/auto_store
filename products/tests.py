from django.test import TestCase
from .models import Product

class ProductTests(TestCase):
    """ ✅ Tests for the Product model """

    def setUp(self):
        """ ✅ Set up test data for each test """
        self.product = Product.objects.create(
            name="Test Product",
            description="This is a test product.",
            price=999.99
        )

    def test_product_creation(self):
        """ ✅ Test if a product is created correctly """
        self.assertEqual(self.product.name, "Test Product")
        self.assertEqual(self.product.description, "This is a test product.")
        self.assertEqual(self.product.price, 999.99)

    def test_product_string_representation(self):
        """ ✅ Test the string representation of the product """
        self.assertEqual(str(self.product), "Test Product")
