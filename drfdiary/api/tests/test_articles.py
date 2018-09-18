import json

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User

from api.models import Category, Article


class ArticleModelTestCase(TestCase):
    """
    This class defines the tests for the article model
    """

    def setUp(self):
        """
        Define the initial variables for the test suite
        """
        self.user = User.objects.create(username="artisan")
        self.category = Category.objects.create(name="Test12", owner=self.user)

    def test_article_creation(self):
        """
        Test creation  of an article in a category
        """
        old_count = Article.objects.count()
        new_article = Article(url="http://www.dummy.com",
                              title="Dummy title",
                              category=self.category,
                              owner=self.user)
        new_article.save()
        new_count = Article.objects.count()
        self.assertEqual(new_count, old_count + 1)
        self.assertTrue(isinstance(new_article, Article))


class ArticleViewTestCase(TestCase):
    """
    This class defines the tests for the article view
    """

    def setUp(self):
        """
        Define the test client and initial variables for the test suite
        """
        self.user = User.objects.create(username="categories_user")

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.category = Category(
            name="Test", description="This is a test category",
            owner=self.user)
        self.category.save()
        self.article = Article(url="http://www.dummy.com",
                               title="Dummy title",
                               category=self.category,
                               owner=self.user)
        self.article_data = {
            "url": "http://www.dummy.com",
            "title": "Dummy Title",
            "description": "A sample description",
            "read_status": False,
            "owner": self.user.id
        }
        article_url = '/api/v1/categories/{}/articles/'.format(
            self.category.id)
        self.response = self.client.post(
            article_url, self.article_data, format="json")

    def test_successful_article_creation(self):
        """
        Test that an authenticated user can create an article in a category
        """
        category = Category.objects.get()
        category_url = '/api/v1/categories/{}/articles/'.format(category.id)
        article_data = {
            "url": "http://www.dummy.com",
            "title": "New One",
            "description": "A sample description",
            "read_status": False,
            "owner": self.user.id
        }
        response = self.client.post(
            category_url, article_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)       

    def test_article_access_without_auth(self):
        """
        Test that authentication is required to create an article
        """
        client = APIClient()
        category = Category.objects.get()
        category_url = '/api/v1/categories/{}/articles/'.format(category.id)
        response = client.get(category_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_fetching_of_articles(self):
        """
        Test that an authenticated user can view their articles
        """
        category = Category.objects.get()
        category_url = '/api/v1/categories/{}/articles/'.format(category.id)
        response = self.client.get(category_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_updating_an_article(self):
        """
        Test that an article can be marked as read as well as updated
        """
        category = Category.objects.get()

        # get the entry we created with the user in the setup method
        response_content = json.loads(self.response.content.decode("utf-8"))

        article_url = '/api/v1/categories/{}/articles/{}/'.format(
            response_content["category"], response_content["id"])

        # Update title
        response = self.client.patch(
            article_url, {"title": "New title"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Mark as read
        status_response = self.client.patch(
            article_url, {"read_status": True}, format="json")

        self.assertEqual(status_response.status_code, status.HTTP_200_OK)

    def test_article_deletion(self):
        """
        Test that an authenticated user can delete an article
        """
        category = Category.objects.get()
        article_data = {
            "url": "http://www.dummy.com",
            "title": "To Be Deleted",
            "description": "A sample description",
            "read_status": False,
            "owner": self.user.id
        }
        # Create an article
        creation_response = self.client.post(
            '/api/v1/categories/{}/articles/'.format(category.id),
            article_data, format="json")
        article = Article.objects.filter(category=category.id)
        article_url = '/api/v1/categories/{}/articles/{}/'.format(
            category.id, article[0].id)
        response = self.client.delete(article_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def cannot_update_another_user_entry(self):
        """
        Test that an unauthenticated user cannot delete another user's articles
        """
        client = APIClient()
        # create a new user
        new_user = User.objects.create(username="another_nerd")
        # log them is
        client.force_authenticate(user=new_user)
        # get the entry we created with the user in the setup method
        response_content = json.loads(self.response.content.decode("utf-8"))
        article_url = '/api/v1/categories/{}/articles/{}/'.format(
            self.category.id, response_content["id"])
        response = client.patch(
            article_url, {"title": "I will not be updated"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
