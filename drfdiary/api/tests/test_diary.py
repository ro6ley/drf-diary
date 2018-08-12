import json

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse

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
        user = User.objects.create(username="nerd")

        # Initialize the client and force it to use auth
        self.client = APIClient()
        self.client.force_authenticate(user=user)
        self.entry_data = {"content": "Dear Diary, it's been so long", "owner": user.id}
        self.response = self.client.post(
            reverse('create'),
            self.entry_data,
            format="json"
        )

    def test_api_can_create_an_entry(self):
        """
        Test the API can create an entry
        """
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_authorization_is_enforced(self):
        """
        Test that the api has user authorization
        """
        new_client = APIClient()
        res = new_client.get('/api/entries/', kwargs={'pk': 3}, format="json")
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_api_can_get_an_entry(self):
        """
        Test the can get a given diary entry
        """
        entry = Entry.objects.get()
        response = self.client.get(
            reverse('details',
                    kwargs={'pk': entry.id}), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
