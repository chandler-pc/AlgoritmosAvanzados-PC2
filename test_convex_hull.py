import unittest
import random
from convex_hull import ConvexHull
from dynamic_convex_hull import DynamicConvexHull
from point import Point

def generate_random_points(n, seed=42):
    random.seed(seed)
    return [Point(random.randint(0, 500), random.randint(0, 500)) for _ in range(n)]

def sort_points_lexicographically(points):
    return sorted((p.x, p.y) for p in points)

class TestConvexHullComparison(unittest.TestCase):

    def setUp(self):
        self.num_points = 100
        self.test_points = generate_random_points(self.num_points)

        # Estructura estática
        self.static_hull = ConvexHull()
        for p in self.test_points:
            self.static_hull.append_point(p.x, p.y)
        self.static_hull.calculate_monotone_chain()

        # Estructura dinámica
        self.dynamic_hull = DynamicConvexHull()
        for p in self.test_points:
            self.dynamic_hull.insert(p)

    def test_convex_hull_equality(self):
        static_result = sort_points_lexicographically(self.static_hull.hull)
        dynamic_result = sort_points_lexicographically(self.dynamic_hull.get_combined_hull())
        self.assertEqual(static_result, dynamic_result, "Convex hulls do not match between static and dynamic")

    def test_is_inside_consistency(self):
        query_points = generate_random_points(50, seed=999)
        for p in query_points:
            result_static = self.static_hull.is_inside_convex_hull(p)
            result_dynamic = self.dynamic_hull.is_inside(p)
            self.assertEqual(result_static, result_dynamic, f"Inconsistent result for point {p.x}, {p.y}")

if __name__ == "__main__":
    unittest.main()
