from app.convex_hull import ConvexHull
from app.dynamic_convex_hull import DynamicConvexHull
from app.point import Point

import random
def generate_random_points(n, seed=42):
    random.seed(seed)
    return [Point(random.randint(0, 500), random.randint(0, 500)) for _ in range(n)]

num_points = 16
test_points = generate_random_points(num_points)

static_hull = ConvexHull()
for p in test_points:
    static_hull.append_point(p.x, p.y)
static_hull.get_hull()

dynamic_hull = DynamicConvexHull()
for p in test_points:
    dynamic_hull.insert(p)
dynamic_hull.get_hull()

print("Static Convex Hull:", static_hull)

print("Dynamic Convex Hull:")
for i, s in enumerate(dynamic_hull.structures):
    print(f"Structure :{i}")
    print(s)