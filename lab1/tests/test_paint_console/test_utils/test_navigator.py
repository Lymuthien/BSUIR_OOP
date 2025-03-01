import unittest
from src.paint_console.utils import Navigator


class TestNavigator(unittest.TestCase):
    def test_initialization_with_single_item_sets_current(self):
        navigator = Navigator(4)
        self.assertEqual(navigator.current(), 4)

    def test_initialization_with_multiple_items_sets_current_to_last(self):
        navigator = Navigator(5, 8, 'sad', 9.8, True, 1)
        self.assertEqual(navigator.current(), 1)

    def test_append_sets_current_item_to_last_added_item(self):
        navigator = Navigator()
        navigator.append(5)
        navigator.append(6)
        self.assertEqual(navigator.current(), 6)

    def test_remove_existing_item_before_current_changed_current_index_to_valid(self):
        navigator = Navigator(5, 10, 78, 44)
        navigator.remove(5)
        self.assertEqual(navigator.current(), 44)

    def test_remove_existing_item_after_current_changed_current_index_to_valid(self):
        navigator = Navigator(5, 10, 78, 44)
        navigator.prev()
        navigator.remove(44)
        self.assertEqual(navigator.current(), 78)

    def test_remove_nonexistent_item_raises_index_error(self):
        navigator = Navigator(9, 10)
        with self.assertRaisesRegex(IndexError, "No such object"):
            navigator.remove(6)

    def test_remove_nonexistent_item_after_deletion_raises_index_error(self):
        navigator = Navigator(5)
        navigator.remove(5)
        with self.assertRaisesRegex(IndexError, "No such object"):
            navigator.remove(5)

    def test_remove_last_item_resets_current_index_to_none(self):
        navigator = Navigator(5)
        navigator.remove(5)
        with self.assertRaisesRegex(IndexError, "List empty"):
            navigator.current()

    def test_next_empty_list_raises_index_error(self):
        navigator = Navigator()
        with self.assertRaisesRegex(IndexError, "List empty"):
            navigator.next()

    def test_next_one_item_return_itself(self):
        navigator = Navigator(5)
        self.assertEqual(navigator.next(), 5)

    def test_next_few_items_return_next(self):
        navigator = Navigator(5, 6, 7)
        navigator.prev()
        navigator.prev()
        self.assertEqual(navigator.next(), 6)
        self.assertEqual(navigator.next(), 7)

    def test_next_last_item_return_first(self):
        navigator = Navigator(5, 6, 7)
        self.assertEqual(navigator.next(), 5)

    def test_prev_empty_list_raises_index_error(self):
        navigator = Navigator()
        with self.assertRaisesRegex(IndexError, "List empty"):
            navigator.prev()

    def test_prev_one_item_return_first(self):
        navigator = Navigator(99)
        self.assertEqual(navigator.prev(), 99)

    def test_prev_few_items_return_prev(self):
        navigator = Navigator(99, 45, 74)
        self.assertEqual(navigator.prev(), 45)

    def test_prev_first_item_return_last(self):
        navigator = Navigator(99, 45, 74)
        navigator.prev()
        navigator.prev()
        self.assertEqual(navigator.prev(), 74)

    def test_current_empty_list_raises_index_error(self):
        navigator = Navigator()
        with self.assertRaisesRegex(IndexError, "List empty"):
            navigator.current()

    def test_current_few_objects_return_current(self):
        navigator = Navigator(5, 7, 14, 33)
        self.assertEqual(navigator.current(), 33)


if __name__ == '__main__':
    unittest.main()
