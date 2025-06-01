import unittest
import random
from app.convex_hull import ConvexHull
from app.dynamic_convex_hull import DynamicConvexHull
from app.point import Point

def generate_random_points(n, seed=42):
    random.seed(seed)
    return [Point(random.randint(0, 500), random.randint(0, 500)) for _ in range(n)]

def sort_points(points):
    return sorted((p.x, p.y) for p in points)

class TestConvexHullComparison(unittest.TestCase):
    def setUp(self):
        self.num_points = 8
        self.test_points = generate_random_points(self.num_points)

        # Estructura estática
        self.static_hull = ConvexHull()
        for p in self.test_points:
            self.static_hull.append_point(p.x, p.y)
        self.static_hull.get_hull()

        # Estructura dinámica
        self.dynamic_hull = DynamicConvexHull()
        for p in self.test_points:
            self.dynamic_hull.insert(p)
        self.dynamic_hull.get_hull()

    def test_convex_hull_equality(self):
        static_result = sort_points(self.static_hull.get_hull())
        dynamic_result = sort_points(self.dynamic_hull.get_hull())
        self.assertEqual(static_result, dynamic_result, "Different hull")

    def test_is_inside_consistency(self):
        query_points = generate_random_points(50, seed=999)
        for p in query_points:
            result_static = self.static_hull.is_inside_convex_hull(p)
            result_dynamic = self.dynamic_hull.is_inside(p)
            self.assertEqual(result_static, result_dynamic, f"Different result query {p.x}, {p.y}")

    def test_insert_extreme_points(self):
        extreme_points = [Point(-1000, -1000), Point(1000, 1000), Point(-1000, 1000), Point(1000, -1000)]
        for p in extreme_points:
            self.dynamic_hull.insert(p)
            self.static_hull.append_point(p.x, p.y)
        
        static_result = sort_points(self.static_hull.get_hull())
        dynamic_result = sort_points(self.dynamic_hull.get_hull())
        self.assertEqual(static_result, dynamic_result, "Mismatch after inserting extreme points")

    def test_insert_duplicate_points(self):
        duplicate = self.test_points[0]
        for _ in range(5):
            self.dynamic_hull.insert(duplicate)
            self.static_hull.append_point(duplicate.x, duplicate.y)

        static_result = sort_points(self.static_hull.get_hull())
        dynamic_result = sort_points(self.dynamic_hull.get_hull())
        self.assertEqual(static_result, dynamic_result, "Mismatch after inserting duplicates")

    def test_inside_known_points(self):
        square = [Point(0, 0), Point(0, 10), Point(10, 0), Point(10, 10)]
        dch = DynamicConvexHull()
        for p in square:
            dch.insert(p)

        self.assertTrue(dch.is_inside(Point(5, 5)))
        self.assertTrue(dch.is_inside(Point(0, 5)))
        self.assertFalse(dch.is_inside(Point(15, 5)))


if __name__ == "__main__":
    unittest.main()
