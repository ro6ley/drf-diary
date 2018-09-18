from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from django.contrib.auth.models import User

from api.models import Category


class CategoryModelTestCase(TestCase):
    """
    This class defines the test cases for the Category model
    """

    def setUp(self):
        """
        Set up the test suite and some initial variables
        """
        self.category_content = {"name": "Test", "description": "This is a test category"}
        self.category = Category(name="Test", description="This is a test category")

    def test_category_can_be_created(self):
        """
        Test that a category can be created by providing the required 
        information.
        """
        old_count = Category.objects.count()
        self.category.save()
        new_count = Category.objects.count()
        self.assertEqual(new_count, old_count + 1)
        
        created_category = Category.objects.get()
        self.assertTrue(isinstance(created_category, Category))


class CategoryViewsTestCases(TestCase):
    """
    This class defines the test cases for the category endpoint
    """

    def setUp(self):
        """
        Set up the Test Suite and define initial variables
        """
        self.user = User.objects.create(username="categories_user")

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.category = Category(name="Test", description="This is a test category")

    def test_view_categories(self):
        """
        Test that an authenticated user can view categories
        """
        response = self.client.get('/api/v1/categories/')
        self.assertEqual(response.status_code, 200)

    def test_unauthenticated_view_categories(self):
        """
        Test that an unauthenticated user cannot view categories
        """
        client = APIClient()
        response = client.get('/api/v1/categories/')
        self.assertEqual(response.status_code, 401)
