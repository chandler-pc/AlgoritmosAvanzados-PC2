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

if __name__ == "__main__":
    unittest.main()
