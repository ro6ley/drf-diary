from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from .models import Entry


class ModelTestCase(TestCase):
    """
    This class defines the test suite for the Entry model
    """

    def setUp(self):
        """
        Define the test client and other test variables
        """
        self.entry_content = "Dear Diary, I wrote tests today"
        self.entry = Entry(content=self.entry_content)

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
        self.client = APIClient()
        self.entry_data = {"content": "Dear Diary, it's been so long"}
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
