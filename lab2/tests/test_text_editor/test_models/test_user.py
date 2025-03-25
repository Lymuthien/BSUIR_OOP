import unittest

from text_editor.models import User


class TestUser(unittest.TestCase):
    def setUp(self):
        self.user = User()

    def test_message(self):
        self.assertEqual(self.user.message, '')

    def test_update(self):
        self.user.update('new')
        self.assertNotEqual(self.user.message, '')


if __name__ == '__main__':
    unittest.main()
