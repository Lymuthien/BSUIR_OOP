import unittest

from parameterized import parameterized

from paint_console.utils import EllipseMath, RectangleMath, TriangleMath


class TestEllipseMath(unittest.TestCase):
    def setUp(self):
        self.ellipse = EllipseMath(3, 5)

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
    def test_ellipse_init_invalid_radii_raises_error(self, test_name, v_r, h_r):
        with self.subTest(msg=test_name, v_r=v_r, h_r=h_r):
            with self.assertRaisesRegex(
                ValueError, "Vertical radius and horizontal radius must be positive"
            ):
                EllipseMath(v_r, h_r)

    def test_area_property_returns_correct_value(self):
        self.assertAlmostEqual(self.ellipse.area, 47.12389, 5)

    def test_perimeter_property_returns_correct_value(self):
        self.assertAlmostEqual(self.ellipse.perimeter, 25.90624, 5)


class TestRectangleMath(unittest.TestCase):
    def setUp(self):
        self.rectangle = RectangleMath(7.0, 5.5)

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
    def test_rectangle_init_invalid_values_raises_error(self, test_name, width, height):
        with self.subTest(msg=test_name, width=width, height=height):
            with self.assertRaisesRegex(
                ValueError, "Width and height must be positive"
            ):
                RectangleMath(width, height)

    def test_area_property_returns_correct_value(self):
        self.assertEqual(self.rectangle.area, 38.5)

    def test_perimeter_property_returns_correct_value(self):
        self.assertEqual(self.rectangle.perimeter, 25)


class TestTriangleMath(unittest.TestCase):
    def setUp(self):
        self.triangles = [
            TriangleMath(((0, 0), (0, 3), (4, 0))),
            TriangleMath(((0, 0), (4, 0), (2, 5))),
            TriangleMath(((0, 0), (8, 0), (3, 2))),
        ]

    @parameterized.expand(
        [
            ("collinear_points", ((0, 0), (1, 1), (2, 2))),
            ("two_points_same", ((0, 0), (0, 0), (3, 4))),
            ("invalid_triangle", ((0, 0), (1, 0), (5, 0))),
        ]
    )
    def test_init_invalid_vertices_raises_error(self, test_name, vertices):
        with self.subTest(msg=test_name, vertices=vertices):
            with self.assertRaisesRegex(
                ValueError, "All sides must be lower to sum of other sides"
            ):
                TriangleMath(vertices)

    def test_area_property_returns_correct_value(self):
        self.assertAlmostEqual(self.triangles[0].area, 6, delta=0.1)
        self.assertAlmostEqual(self.triangles[1].area, 10, delta=0.1)
        self.assertAlmostEqual(self.triangles[2].area, 8, delta=0.1)

    def test_perimeter_property_returns_correct_value(self):
        self.assertAlmostEqual(self.triangles[0].perimeter, 12, delta=0.1)
        self.assertAlmostEqual(self.triangles[1].perimeter, 14.77, delta=0.1)
        self.assertAlmostEqual(self.triangles[2].perimeter, 16.991, delta=0.1)

    def test_sides_property_returns_correct_value(self):
        self.assertSetEqual(
            set(round(side, 0) for side in self.triangles[0].sides), {3, 4, 5}
        )
        self.assertSetEqual(
            set(round(side, 3) for side in self.triangles[1].sides), {4, 5.385}
        )
        self.assertSetEqual(
            set(round(side, 3) for side in self.triangles[2].sides), {8, 3.606, 5.385}
        )


if __name__ == "__main__":
    unittest.main()
