import json

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User

from api.models import Entry


class ModelTestCase(TestCase):
    """
    This class defines the test suite for the Entry model
    """

    def setUp(self):
        """
        Define the test client and other test variables
        """
        user = User.objects.create(username="nerd")
        self.entry_content = "Dear Diary, I wrote tests today"
        self.entry = Entry(content=self.entry_content, owner=user)

    def test_model_can_create_an_entry(self):
        """
        Test that the Entry model can create a diary entry
        """
        old_count = Entry.objects.count()
        self.entry.save()
        new_count = Entry.objects.count()
        self.assertNotEqual(old_count, new_count)


class ViewTestCase(TestCase):
    """
    The test suite for the views
    """

    def setUp(self):
        """
        Define the test client and other test variables
        """
        self.user = User.objects.create(username="nerd", password="password")

        # Initialize the client and force it to use auth
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.entry_data = {
            "content": "Dear Diary, it's been so long", "owner": self.user.id}
        self.response = self.client.post(
            '/api/v2/entries/', self.entry_data, format="json")

    def test_can_create_a_user(self):
        """
        Test user registration via the API
        """
        response = self.client.post('/api/v2/accounts/registration/',
                                    {
                                        "username": "robley",
                                        "password1": "0@qwer687",
                                        "password2": "0@qwer687",
                                        "email": "random@guy.com"
                                    },
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_api_can_create_an_entry(self):
        """
        Test the API can create an entry
        """
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_api_cannot_create_without_auth(self):
        """
        Test that creation of an entry requires authentication
        """
        client = APIClient()
        response = client.post(
            '/api/v2/entries/', {"content": "I cannot be created"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_api_can_list_all_users(self):
        """
        Test that the API can return a list of all users
        """
        response = self.client.get('/api/v2/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_cannot_list_all_users_without_auth(self):
        """
        Test that authentication is required to list all users
        """
        client = APIClient()
        response = client.get('/api/v2/users/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_api_can_get_an_entry(self):
        """
        Test the can get a given diary entry
        """
        entry = Entry.objects.get()
        url = "/api/v2/entries/{}/".format(entry.id)
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_cannot_get_entry_without_auth(self):
        """
        Test that authentication is required to fetch an entry
        """
        response_content = json.loads(self.response.content.decode("utf-8"))
        client = APIClient()
        response = client.get(
            '/api/v2/entries/{}/'.format(response_content["id"]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_api_can_update_an_entry(self):
        """
        Test that we can update an entry
        """
        entry = Entry.objects.get()
        url = "/api/v2/entries/{}/".format(entry.id)
        response = self.client.put(
            url, {"content": "I am going to be updated"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_cannot_update_entry_without_auth(self):
        """
        Test that auth is needed to update an entry
        """
        client = APIClient()
        entry = Entry.objects.get()
        url = "/api/v2/entries/{}/".format(entry.id)
        response = client.put(
            url, {"content": "I am going to be updated"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_cannot_view_another_user_entry(self):
        """
        Test that a user cannot view another user's entries
        """
        client = APIClient()
        # create a new user
        new_user = User.objects.create(username="another_nerd")
        # log them is
        self.client.force_authenticate(user=new_user)
        # get the entry we created with the user in the setup method
        response_content = json.loads(self.response.content.decode("utf-8"))
        response = client.get(
            '/api/v2/entries/{}/'.format(response_content["id"]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_cannot_update_another_user_entry(self):
        """
        Test that no other user can update a user's entry
        """
        client = APIClient()
        # create a new user
        new_user = User.objects.create(username="another_nerd")
        # log them is
        self.client.force_authenticate(user=new_user)
        # get the entry we created with the user in the setup method
        response_content = json.loads(self.response.content.decode("utf-8"))
        response = client.put(
            '/api/v2/entries/{}/'.format(response_content["id"]),
            {"content": "I will not be updated"},
            format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_api_can_delete_an_entry(self):
        """
        Test the deletion of a given diary entry
        """
        entry = Entry.objects.get()
        url = "/api/v2/entries/{}/".format(entry.id)
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
