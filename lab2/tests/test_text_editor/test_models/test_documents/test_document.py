import unittest
from unittest.mock import MagicMock

from text_editor.interfaces import IObserver
from text_editor.models import DocumentSettings
from text_editor.models.documents.document import Document


class TestDocument(unittest.TestCase):
    def setUp(self):
        self.document = Document()

    def test_set_password_first_time(self):
        self.document.set_password('<PASSWORD>')

    def test_set_password_twice_raise_exception(self):
        self.document.set_password('<PASSWORD>')
        with self.assertRaises(Exception):
            self.document.set_password('<PASSWORD>')

    def test_validate_password(self):
        self.document.set_password('<PASSWORD>')
        self.assertTrue(self.document.validate_password('<PASSWORD>'))

    def test_validate_password_with_incorrect_password_returns_false(self):
        self.document.set_password('<PASSWORD>')
        self.assertFalse(self.document.validate_password('other'))

    def test_settings_returns_document_settings(self):
        self.assertTrue(isinstance(self.document.settings, DocumentSettings))

    def test_insert_text(self):
        self.document.insert_text('text', 0)
        self.assertEqual(self.document.get_text(), 'text')

    def test_insert_text_to_end(self):
        self.document.insert_text('text', 0)
        self.document.insert_text('end', 4)
        self.assertEqual(self.document.get_text(), 'textend')

    def test_replace_text(self):
        self.document.insert_text('text', 0)
        self.document.replace_text('new', 0, 1)
        self.assertEqual(self.document.get_text(), 'newxt')

    def test_delete_text(self):
        self.document.insert_text('text', 0)
        self.document.delete_text(2, 3)
        self.assertEqual(self.document.get_text(), 'te')

    def test_get_text(self):
        self.assertEqual(self.document.get_text(), '')

    def test_attach(self):
        mock_observer = MagicMock(spec=IObserver)
        self.document.attach(mock_observer)
        self.document.notify()
        mock_observer.update.assert_called_once()

    def test_attach_add_twice_called_once(self):
        mock_observer = MagicMock(spec=IObserver)
        self.document.attach(mock_observer)
        self.document.attach(mock_observer)
        self.document.notify()
        mock_observer.update.assert_called_once()

    def test_from_dict_raise_exception(self):
        with self.assertRaises(NotImplementedError):
            self.document.from_dict({})



if __name__ == '__main__':
    unittest.main()
