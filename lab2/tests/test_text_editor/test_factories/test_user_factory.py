import unittest

from text_editor.factories.user_factory import EditorUserFactory, AdminUserFactory, ReaderUserFactory
from text_editor.models import EditorUser, Admin, ReaderUser


class TestEditorUserFactory(unittest.TestCase):
    def setUp(self):
        self.factory = EditorUserFactory()

    def test_create_user_default_name(self):
        user = self.factory.create_user()
        self.assertIsInstance(user, EditorUser)
        self.assertEqual(user.name, 'base')

    def test_create_user_with_name(self):
        user_name = "TestUser"
        user = self.factory.create_user(user_name)
        self.assertIsInstance(user, EditorUser)
        self.assertEqual(user.name, user_name)

    def test_user_can_edit_text(self):
        user = self.factory.create_user()
        self.assertTrue(user.can_edit_text())

    def test_user_cannot_change_document_settings(self):
        user = self.factory.create_user()
        self.assertFalse(user.can_change_document_settings())


class TestAdminUserFactory(unittest.TestCase):
    def setUp(self):
        self.factory = AdminUserFactory()

    def test_create_user_default_name(self):
        user = self.factory.create_user()
        self.assertIsInstance(user, Admin)
        self.assertEqual(user.name, 'base')

    def test_create_user_with_name(self):
        user_name = "AdminTestUser"
        user = self.factory.create_user(user_name)
        self.assertIsInstance(user, Admin)
        self.assertEqual(user.name, user_name)

    def test_admin_can_edit_text(self):
        user = self.factory.create_user()
        self.assertTrue(user.can_edit_text())

    def test_admin_can_change_document_settings(self):
        user = self.factory.create_user()
        self.assertTrue(user.can_change_document_settings())


class TestReaderUserFactory(unittest.TestCase):
    def setUp(self):
        self.factory = ReaderUserFactory()

    def test_create_user_default_name(self):
        user = self.factory.create_user()
        self.assertIsInstance(user, ReaderUser)
        self.assertEqual(user.name, 'base')

    def test_create_user_with_name(self):
        user_name = "ReaderTestUser"
        user = self.factory.create_user(user_name)
        self.assertIsInstance(user, ReaderUser)
        self.assertEqual(user.name, user_name)

    def test_reader_cannot_edit_text(self):
        user = self.factory.create_user()
        self.assertFalse(user.can_edit_text())

    def test_reader_cannot_change_document_settings(self):
        user = self.factory.create_user()
        self.assertFalse(user.can_change_document_settings())


if __name__ == "__main__":
    unittest.main()
