import unittest
import os
import json

from app import create_app, db


class EntryTestCase(unittest.TestCase):
    """
    This class represents the Entry test cases
    """

    def setUp(self):
        """
        Define test variables and initialize app
        """
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.entry = {"content": "Dear Diary, I built an API today."}

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_entry_creation(self):
        """
        Test that a diary entry can be created
        """
        res = self.client().post("/entries/", data=self.entry)
        self.assertEqual(res.status_code, 201)
        res = self.client().get("/entries/")
        self.assertEqual(res.status_code, 200)
        self.assertIn("Dear Diary", str(res.data))

    def tearDown(self):
        """
        Tear down all initialized variables.
        """
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()


# Make the tests conviniently executable
if __name__ == "__main__":
    unittest.main()
