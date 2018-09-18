import json

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
        self.user = User.objects.create(username="anerd")
        self.category_content = {"name": "Test",
                                 "description": "This is a test category"}
        self.category = Category(name="Test",
                                 description="This is a test category",
                                 owner=self.user)

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
        self.category = Category(name="Test",
                                 description="This is a test category",
                                 owner=self.user)

    def test_view_categories(self):
        """
        Test that an authenticated user can view categories
        """
        response = self.client.get('/api/v1/categories/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthenticated_view_categories(self):
        """
        Test that an unauthenticated user cannot view categories
        """
        client = APIClient()
        response = client.get('/api/v1/categories/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_successful_category_creation(self):
        """
        Test that an authenticated user can create categories
        """
        category_data = {"name": "Sampuli", "description": "Ditto"}
        response = self.client.post(
            '/api/v1/categories/', category_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_successful_category_updating(self):
        """
        Test that an authenticated user can update categories
        """
        category_data = {"name": "Sampuli", "description": "Ditto"}
        create_response = self.client.post(
            '/api/v1/categories/', category_data, format="json")

        response_content = json.loads(create_response.content.decode("utf-8"))

        new_category_data = {"name": "Sampuli B"}
        update_url = '/api/v1/categories/{}/'.format(response_content["id"])

        update_response = self.client.patch(
            update_url, new_category_data, format="json")
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)

    def test_successful_category_deletion(self):
        """
        Test that an authenticated user can delete categories
        """
        category_data = {"name": "Sampuli", "description": "Ditto"}
        create_response = self.client.post(
            '/api/v1/categories/', category_data, format="json")

        response_content = json.loads(create_response.content.decode("utf-8"))

        update_response = self.client.delete(
            '/api/v1/categories/{}/'.format(response_content["id"]))
        self.assertEqual(update_response.status_code,
                         status.HTTP_204_NO_CONTENT)

    def test_cannot_access_another_user_category(self):
        """
        Test that an authenticated user cannot view another user's categories
        """
        # Create a category as initial user
        category_data = {"name": "Ditto", "description": "Ditto"}
        create_response = self.client.post(
            '/api/v1/categories/', category_data, format="json")

        response_content = json.loads(create_response.content.decode("utf-8"))

        client = APIClient()
        # create a new user
        new_user = User.objects.create(username="another_nerd")
        # log them in
        client.force_authenticate(user=new_user)

        category_url = '/api/v1/categories/{}/'.format(response_content["id"])

        response = client.get(category_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cannot_update_another_user_category(self):
        """
        Test that an authenticated user cannot update another user's categories
        """
        # Create a category as initial user
        category_data = {"name": "Ditto", "description": "Ditto"}
        create_response = self.client.post(
            '/api/v1/categories/', category_data, format="json")

        response_content = json.loads(create_response.content.decode("utf-8"))

        client = APIClient()
        # create a new user
        new_user = User.objects.create(username="another_nerd")
        # log them in
        client.force_authenticate(user=new_user)

        category_url = '/api/v1/categories/{}/'.format(response_content["id"])

        response = client.put(category_url, {"name": "new name"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
