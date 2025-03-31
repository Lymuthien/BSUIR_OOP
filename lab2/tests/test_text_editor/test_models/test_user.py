import unittest

from text_editor.models import User


class TestUser(unittest.TestCase):
    def setUp(self):
        self.user = User(name="test_user")

    def test_initial_name(self):
        self.assertEqual(self.user.name, "test_user")

    def test_initial_message(self):
        self.assertEqual(self.user.message, "")

    def test_update_message(self):
        self.user.update("New message")
        self.assertEqual(self.user.message, "New message")

    def test_to_dict(self):
        self.user.update("Test message")
        user_dict = self.user.to_dict()
        expected_dict = {
            "type": "User",
            "message": "Test message",
            "name": "test_user"
        }
        self.assertEqual(user_dict, expected_dict)

    def test_from_dict(self):
        user_dict = {
            "type": "User",
            "message": "Loaded message",
            "name": "loaded_user"
        }
        self.user.from_dict(user_dict)
        self.assertEqual(self.user.name, "loaded_user")
        self.assertEqual(self.user.message, "Loaded message")


if __name__ == "__main__":
    unittest.main()
