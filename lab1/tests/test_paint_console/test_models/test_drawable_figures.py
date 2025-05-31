import unittest
from unittest.mock import patch, MagicMock, PropertyMock

from parameterized import parameterized

from paint_console.models import (
    DrawableFigure,
    DrawableEllipse,
    DrawableTriangle,
    DrawableRectangle,
)


class TestableDrawableFigure(DrawableFigure):
    def render(self) -> list[list[str]]:
        return MagicMock()


class TestDrawableFigure(unittest.TestCase):
    def test_drawable_figure_init_with_empty_bg_raises_error(self):
        with self.assertRaisesRegex(
            ValueError, "Background must be a single character"
        ):
            TestableDrawableFigure("")

    def test_drawable_figure_init_with_len_bg_greater_one_raises_error(self):
        with self.assertRaisesRegex(
            ValueError, "Background must be a single character"
        ):
            TestableDrawableFigure("ff")

    def test_drawable_figure_init_with_len_bg_one_normal(self):
        self.assertEqual(TestableDrawableFigure("e").background, "e")

    def test_background_setter_with_empty_bg_raises_error(self):
        figure = TestableDrawableFigure("e")
        with self.assertRaisesRegex(
            ValueError, "Background must be a single character"
        ):
            figure.background = ""

    def test_background_setter_with_len_bg_greater_one_raises_error(self):
        figure = TestableDrawableFigure("e")
        with self.assertRaisesRegex(
            ValueError, "Background must be a single character"
        ):
            figure.background = "ee"


class TestDrawableEllipse(unittest.TestCase):
    def test_drawable_ellipse_init_all_properties_match(self):
        figure = DrawableEllipse(4, 5, "e")
        self.assertEqual(figure.vertical_radius, 4)
        self.assertEqual(figure.horizontal_radius, 5)
        self.assertEqual(figure.background, "e")

    @parameterized.expand(
        [
            ("negative_both_radii", -1, -1),
            ("negative_vertical_radius", -1, 10),
            ("negative_horizontal_radius", 1, -1),
            ("zero_both_radii", 0, 0),
            ("zero_vertical_radius", 0, 10),
            ("zero_horizontal_radius", 1, 0),
        ]
    )
    def test_drawable_ellipse_init_with_unvalidated_coords(self, test_name, v_r, h_r):
        with self.subTest(msg=test_name, v_r=v_r, h_r=h_r):
            with self.assertRaises(Exception):
                DrawableEllipse(v_r, h_r, "t")

    @parameterized.expand(
        [
            ("two_symbols", "tt"),
            ("empty", ""),
        ]
    )
    def test_drawable_ellipse_init_with_unvalidated_background(self, test_name, bg):
        with self.subTest(msg=test_name, bg=bg):
            with self.assertRaises(Exception):
                DrawableEllipse(1, 1, bg)

    def test_info_given_correctly(self):
        figure = DrawableEllipse(4, 5, "e")

        with (
            patch(
                "paint_console.utils.EllipseMath.info", new_callable=PropertyMock
            ) as mock_ellipse_info,
            patch(
                "paint_console.models.DrawableFigure.info", new_callable=PropertyMock
            ) as mock_drawable_info,
        ):
            mock_ellipse_info.return_value = {
                "type": "ellipse",
                "vertical_radius": 4,
                "horizontal_radius": 5,
            }

            mock_drawable_info.return_value = {"background": "e"}

            expected_result = {
                "type": "ellipse",
                "vertical_radius": 4,
                "horizontal_radius": 5,
                "background": "e",
            }

            result = figure.info
            self.assertDictEqual(result, expected_result)


class TestDrawableRectangle(unittest.TestCase):
    def test_drawable_rectangle_init_all_properties_match(self):
        figure = DrawableRectangle(10, 56, "r")
        self.assertEqual(figure.width, 10)
        self.assertEqual(figure.height, 56)
        self.assertEqual(figure.background, "r")

    @parameterized.expand(
        [
            ("negative_both_width_height", -1, -1),
            ("negative_width", -1, 1),
            ("negative_height", 1, -1),
            ("zero_both_width_height", 0, 0),
            ("zero_width", 0, 10),
            ("zero_height", 1, 0),
        ]
    )
    def test_drawable_rectangle_init_with_unvalidated_coords(
        self, test_name, width, height
    ):
        with self.subTest(msg=test_name, width=width, height=height):
            with self.assertRaises(Exception):
                DrawableRectangle(width, height, "t")

    @parameterized.expand(
        [
            ("two_symbols", "tt"),
            ("empty", ""),
        ]
    )
    def test_drawable_rectangle_init_with_unvalidated_background(self, test_name, bg):
        with self.subTest(msg=test_name, bg=bg):
            with self.assertRaises(Exception):
                DrawableRectangle(1, 1, bg)

    def test_info_given_correctly(self):
        figure = DrawableRectangle(10, 56, "r")

        with (
            patch(
                "paint_console.utils.RectangleMath.info", new_callable=PropertyMock
            ) as mock_rectangle_info,
            patch(
                "paint_console.models.DrawableFigure.info", new_callable=PropertyMock
            ) as mock_drawable_info,
        ):
            mock_rectangle_info.return_value = {
                "type": "rectangle",
                "width": 4,
                "height": 5,
            }

            mock_drawable_info.return_value = {"background": "r"}

            expected_result = {
                "type": "rectangle",
                "width": 4,
                "height": 5,
                "background": "r",
            }

            result = figure.info
            self.assertDictEqual(result, expected_result)


class TestDrawableTriangle(unittest.TestCase):
    def test_drawable_triangle_init_all_properties_match(self):
        figure = DrawableTriangle(((0, 0), (0, 4), (3, 0)), "t")
        self.assertEqual(figure.vertices, ((0, 0), (0, 4), (3, 0)))
        self.assertEqual(figure.background, "t")

    def test_drawable_triangle_init_with_unvalidated_coords(self):
        with self.assertRaises(Exception):
            DrawableTriangle(((0, 0), (0, 0), (5, 0)), "t")

    @parameterized.expand(
        [
            ("two_symbols", "tt"),
            ("empty", ""),
        ]
    )
    def test_drawable_triangle_init_with_unvalidated_background(self, test_name, bg):
        with self.subTest(msg=test_name, bg=bg):
            with self.assertRaises(Exception):
                DrawableTriangle(((0, 0), (0, 4), (3, 0)), bg)

    def test_info_given_correctly(self):
        figure = DrawableTriangle(((0, 0), (0, 4), (3, 0)), "t")

        with (
            patch(
                "paint_console.utils.TriangleMath.info", new_callable=PropertyMock
            ) as mock_triangle_info,
            patch(
                "paint_console.models.DrawableFigure.info", new_callable=PropertyMock
            ) as mock_drawable_info,
        ):
            mock_triangle_info.return_value = {"type": "triangle", "sides": (4, 5, 6)}

            mock_drawable_info.return_value = {"background": "t"}

            expected_result = {
                "type": "triangle",
                "sides": (4, 5, 6),
                "background": "t",
            }

            result = figure.info
            self.assertDictEqual(result, expected_result)


if __name__ == "__main__":
    unittest.main()
