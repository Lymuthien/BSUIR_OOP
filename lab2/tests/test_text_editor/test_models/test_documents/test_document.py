import unittest

from text_editor.interfaces import IUser
from text_editor.models import Theme, Document


class MockUser(IUser):
    def __init__(self, name):
        self._name = name
        self._message = ""

    @property
    def name(self) -> str:
        return self._name

    def can_edit_text(self) -> bool:
        return True

    def can_change_document_settings(self) -> bool:
        return True

    @property
    def message(self) -> str:
        return self._message

    def update(self, data) -> None:
        self._message = data

    def to_dict(self) -> dict:
        return {"type": "MockUser", "name": self._name}

    @staticmethod
    def from_dict(data: dict):
        return MockUser(data["name"])


class TestDocument(unittest.TestCase):
    def setUp(self):
        self.document = Document()

    def test_insert_text(self):
        self.document.insert_text("Hello", 0)
        self.assertEqual(self.document.get_text(), "Hello")

    def test_replace_text(self):
        self.document.insert_text("Hello World", 0)
        self.document.replace_text("Universe", 6, 10)
        self.assertEqual(self.document.get_text(), "Hello Universe")

    def test_delete_text(self):
        self.document.insert_text("Hello World", 0)
        self.document.delete_text(5, 11)
        self.assertEqual(self.document.get_text(), "Hello")

    def test_set_theme(self):
        theme = Theme(font_size=12, italic=True)
        self.document.set_theme(theme)
        # Assuming the `set_theme` triggers a notification, mock observers could verify this
        # Here we just ensure no exceptions occur

    def test_attach_user(self):
        user = MockUser("test_user")
        self.document.attach(user)
        self.assertIn("test_user", self.document.users())

    def test_detach_user(self):
        user = MockUser("test_user")
        self.document.attach(user)
        self.document.detach(user)
        self.assertNotIn("test_user", self.document.users())

    def test_notify_users(self):
        user = MockUser("test_user")
        self.document.attach(user)
        self.document.notify("Test notification")
        self.assertEqual(user.message, "Test notification")

    def test_to_dict(self):
        self.document.insert_text("Sample text", 0)
        result = self.document.to_dict()
        self.assertEqual(result["type"], "Document")
        self.assertEqual(len(result["components"]), 1)
        self.assertEqual(result["components"][0]["text"], "Sample text")



if __name__ == "__main__":
    unittest.main()
