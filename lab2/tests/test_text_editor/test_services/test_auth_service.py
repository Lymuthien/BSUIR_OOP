import unittest

from text_editor.services.auth_service import AuthService


class TestAuthService(unittest.TestCase):
    def setUp(self):
        self.auth_service = AuthService(users=["user1", "user2"])

    def test_register_user_success(self):
        new_user = "user3"
        registered_user = self.auth_service.register_user(new_user)
        self.assertEqual(registered_user, new_user)

    def test_register_user_already_exists(self):
        with self.assertRaises(Exception) as context:
            self.auth_service.register_user("user1")
        self.assertEqual(str(context.exception), "User already exists")

    def test_login_success(self):
        logged_in_user = self.auth_service.login("user1")
        self.assertEqual(logged_in_user, "user1")

    def test_login_invalid_credentials(self):
        with self.assertRaises(Exception) as context:
            self.auth_service.login("non_existent_user")
        self.assertEqual(str(context.exception), "Invalid credentials")

    def test_register_and_login_new_user(self):
        new_user = "user4"
        self.auth_service.register_user(new_user)
        logged_in_user = self.auth_service.login(new_user)
        self.assertEqual(logged_in_user, new_user)


if __name__ == "__main__":
    unittest.main()
