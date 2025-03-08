from django.test import TestCase
from django.contrib.auth import get_user_model

class AuthSystemTests(TestCase):
    """ Tests for user authentication system """

    def test_create_user(self):
        """ ✅ Test creating a new user """
        User = get_user_model()
        user = User.objects.create_user(username="testuser", password="testpassword")
        self.assertEqual(user.username, "testuser")
        self.assertTrue(user.check_password("testpassword"))

    def test_create_superuser(self):
        """ ✅ Test creating a new superuser """
        User = get_user_model()
        admin_user = User.objects.create_superuser(username="admin", password="adminpassword")
        self.assertTrue(admin_user.is_superuser)
        self.assertTrue(admin_user.is_staff)

    def test_user_login(self):
        """ ✅ Test user login """
        User = get_user_model()
        user = User.objects.create_user(username="testuser", password="testpassword")
        login_successful = self.client.login(username="testuser", password="testpassword")
        self.assertTrue(login_successful)

    def test_invalid_login(self):
        """ ✅ Test invalid login attempt """
        login_successful = self.client.login(username="wronguser", password="wrongpassword")
        self.assertFalse(login_successful)
