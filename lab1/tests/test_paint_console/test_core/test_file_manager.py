import os
import unittest
from tempfile import NamedTemporaryFile

from paint_console.core import FileManager


class TestFileManager(unittest.TestCase):
    def test_save_and_load_valid_data(self):
        test_data = {"key": "value", "numbers": [1, 2, 3]}

        with NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.close()

            FileManager.save(test_data, tmp_file.name)
            loaded_data = FileManager.load(tmp_file.name)
            self.assertEqual(test_data, loaded_data)

        os.remove(tmp_file.name)

    def test_load_nonexistent_file(self):
        with self.assertRaises(FileNotFoundError):
            FileManager.load("non_existent_file.pkl")

    def test_load_corrupted_file(self):
        with NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(b"corrupted_data")
            tmp_file.flush()
            tmp_file.close()

            with self.assertRaisesRegex(Exception, "Load failed:"):
                FileManager.load(tmp_file.name)

        os.remove(tmp_file.name)


if __name__ == "__main__":
    unittest.main()
