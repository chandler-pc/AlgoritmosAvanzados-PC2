import unittest
from app.dynamic_convex_hull import DynamicConvexHull
from app.point import Point

def generate_random_points(n, seed=42):
    import random
    random.seed(seed)
    return [Point(random.randint(0, 300), random.randint(0, 300)) for _ in range(n)]

def sort_points(points):
    return sorted((p.x, p.y) for p in points)

class TestDynamicConvexHull(unittest.TestCase):

    def setUp(self):
        self.hull = DynamicConvexHull()

    def test_empty_hull(self):
        self.assertEqual(self.hull.get_hull(), [], "Empty hull should return empty list")

    def test_single_insertion(self):
        p = Point(10, 10)
        self.hull.insert(p)
        hull_points = self.hull.get_hull()
        self.assertEqual(len(hull_points), 1)
        self.assertIn((10, 10), sort_points(hull_points))

    def test_line_insertion(self):
        points = [Point(0, 0), Point(1, 1), Point(2, 2)]
        for p in points:
            self.hull.insert(p)
        hull = self.hull.get_hull()
        self.assertEqual(len(hull), 2, "Hull for colinear points should have 2 endpoints")

    def test_triangle_hull(self):
        triangle = [Point(0, 0), Point(1, 0), Point(0, 1)]
        for p in triangle:
            self.hull.insert(p)
        hull = sort_points(self.hull.get_hull())
        expected = sort_points(triangle)
        self.assertEqual(hull, expected, "Triangle points should form their own hull")

    def test_insertion_then_deletion(self):
        points = [Point(0, 0), Point(1, 0), Point(0, 1), Point(0.5, 0.5)]
        for p in points:
            self.hull.insert(p)

        self.hull.delete(Point(0.5, 0.5))
        hull = sort_points(self.hull.get_hull())
        expected = sort_points(points[:-1])
        self.assertEqual(hull, expected, "Hull should ignore internal deleted point")

    def test_mass_insertion_and_deletion(self):
        points = generate_random_points(100)
        for p in points:
            self.hull.insert(p)
        hull_before = sort_points(self.hull.get_hull())
        self.assertGreaterEqual(len(hull_before), 3)

        for p in points[:30]:
            self.hull.delete(p)
        hull_after = sort_points(self.hull.get_hull())
        self.assertIsInstance(hull_after, list)

    def test_is_inside_after_deletion(self):
        triangle = [Point(0, 0), Point(4, 0), Point(2, 4), Point(2, 1)]
        for p in triangle:
            self.hull.insert(p)
        self.hull.delete(Point(2, 1))

        self.assertTrue(self.hull.is_inside(Point(2, 1)), "Deleted internal point should still be inside")
        self.assertFalse(self.hull.is_inside(Point(5, 5)), "External point should be outside")

if __name__ == "__main__":
    unittest.main()
