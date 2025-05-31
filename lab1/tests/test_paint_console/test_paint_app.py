import unittest
from unittest.mock import MagicMock, patch

from paint_console import PaintApp


# Other functions use only logic of others, so they (others) tested in another modules


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.mock_navigator = MagicMock()
        self.mock_canvas_model = MagicMock()
        self.mock_canvas_view = MagicMock()
        self.mock_history = MagicMock()

        self.patchers = [
            patch(
                "paint_console.models.CanvasModel", return_value=self.mock_canvas_model
            ),
            patch(
                "paint_console.models.CanvasView", return_value=self.mock_canvas_view
            ),
            patch("paint_console.core.HistoryManager", return_value=self.mock_history),
            patch("paint_console.utils.Navigator", return_value=self.mock_navigator),
        ]

        for patcher in self.patchers:
            patcher.start()

        self.app = PaintApp()

    def test_app_initialization(self):
        self.assertEqual(self.app.canvas_width, 50)
        self.assertEqual(self.app.canvas_height, 20)


if __name__ == "__main__":
    unittest.main()
