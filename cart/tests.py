from django.test import TestCase
from django.contrib.auth.models import User
from products.models import Product
from .models import Cart, CartItem

class CartTests(TestCase):
    """ ✅ Tests for shopping cart functionality """

    def setUp(self):
        """ ✅ Set up test data for each test """
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.cart = Cart.objects.create(user=self.user)
        self.product = Product.objects.create(name="Test Product", price=100.00)

    def test_cart_creation(self):
        """ ✅ Test if a cart is created correctly """
        self.assertEqual(self.cart.user.username, "testuser")

    def test_add_item_to_cart(self):
        """ ✅ Test adding an item to the cart """
        cart_item = CartItem.objects.create(cart=self.cart, product=self.product, quantity=2)
        self.assertEqual(cart_item.product.name, "Test Product")
        self.assertEqual(cart_item.quantity, 2)

    def test_cart_total_price(self):
        """ ✅ Test calculating the total price of items in the cart """
        CartItem.objects.create(cart=self.cart, product=self.product, quantity=3)
        total_price = sum(item.total_price() for item in self.cart.items.all())
        self.assertEqual(total_price, 300.00)  # 3 * 100.00

    def test_remove_item_from_cart(self):
        """ ✅ Test removing an item from the cart """
        cart_item = CartItem.objects.create(cart=self.cart, product=self.product, quantity=1)
        cart_item.delete()
        self.assertEqual(self.cart.items.count(), 0)
