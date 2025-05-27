import matplotlib.pyplot as plt
import time
import random
from point import Point
from convex_hull import ConvexHull
from dynamic_convex_hull import DynamicConvexHull

def generate_points(n, max_coord=1000):
    return [Point(random.randint(0, max_coord), random.randint(0, max_coord)) for _ in range(n)]

initial_n = 500
insertions_total = 3000
query_interval = 100 

initial_points = generate_points(initial_n)
insertion_points = generate_points(insertions_total)

# --- Static ---
static_convex_hull = ConvexHull()
for p in initial_points:
    static_convex_hull.append_point(p.x, p.y)
static_convex_hull.get_hull()

static_times = []
start = time.time()
for i, p in enumerate(insertion_points, 1):
    static_convex_hull.append_point(p.x, p.y)
    if i % query_interval == 0:
        static_convex_hull.get_hull()
        static_times.append(time.time() - start)

# --- Dynamic ---
dynamic_convex_hull = DynamicConvexHull()
for p in initial_points:
    dynamic_convex_hull.insert(p)

dynamic_times = []
start = time.time()
for i, p in enumerate(insertion_points, 1):
    dynamic_convex_hull.insert(p)
    if i % query_interval == 0:
        dynamic_convex_hull.get_hull()
        dynamic_times.append(time.time() - start)

x_values = list(range(query_interval, insertions_total + 1, query_interval))

plt.figure(figsize=(10, 6))
plt.plot(x_values, static_times, marker='o', label='Static')
plt.plot(x_values, dynamic_times, marker='s', label='Dynamic')
plt.xlabel("Number of Insertions")
plt.ylabel("Cumulative Time (seconds)")
plt.title("Cumulative Time for Insertions and Queries")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
