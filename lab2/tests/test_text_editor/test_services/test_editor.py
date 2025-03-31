import unittest
from unittest.mock import Mock

from text_editor.models import EditorSettings
from text_editor.services import Editor


class TestEditor(unittest.TestCase):
    def setUp(self):
        self.mock_serializer = Mock()
        self.editor = Editor(serializers={"json": self.mock_serializer})
        self.mock_file_manager = Mock()
        self.editor.set_file_manager(self.mock_file_manager)

    def test_initial_settings(self):
        self.assertIsInstance(self.editor.settings, EditorSettings)

    def test_create_document_without_login(self):
        with self.assertRaises(Exception) as context:
            self.editor.create_document()
        self.assertEqual(str(context.exception), 'Login please.')

    def test_create_document_with_login(self):
        self.editor.register("test_user")
        self.editor.create_document()
        self.assertTrue(self.editor.is_opened())

    def test_open_document_unknown_extension(self):
        self.editor.register("test_user")
        with self.assertRaises(Exception) as context:
            self.editor.open_document("file.unknown")
        self.assertEqual(str(context.exception), "Unknown format")

    def test_close_document(self):
        self.editor.register("test_user")
        self.editor.create_document()
        self.editor.close_document()
        self.assertFalse(self.editor.is_opened())

    def test_login_user(self):
        self.editor.register("test_user")
        self.editor.login("test_user")
        self.assertEqual(self.editor.get_text(), None)  # No document created yet

    def test_save_document_unknown_format(self):
        self.editor.register("test_user")
        self.editor.create_document()
        with self.assertRaises(Exception) as context:
            self.editor.save_document("file_path", format_="unknown")
        self.assertEqual(str(context.exception), "Unknown format")

    def test_set_theme(self):
        self.editor.register("test_user")
        self.editor.create_document()
        self.editor.set_theme(2)
        self.assertTrue(self.editor.is_opened())

    def test_give_role_without_login(self):
        with self.assertRaises(Exception) as context:
            self.editor.give_role("test_user", "admin")
        self.assertEqual(str(context.exception), "Login please")


    def test_undo_with_no_commands(self):
        try:
            self.editor.undo()
        except Exception:
            self.fail("Undo raised exception unexpectedly!")

    def test_redo_with_no_commands(self):
        try:
            self.editor.redo()
        except Exception:
            self.fail("Redo raised exception unexpectedly!")


if __name__ == "__main__":
    unittest.main()
