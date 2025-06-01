import matplotlib.pyplot as plt
import time
import random
from app.point import Point
from app.convex_hull import ConvexHull
from app.dynamic_convex_hull import DynamicConvexHull

def generate_points(n, max_coord=1000):
    return [Point(random.randint(0, max_coord), random.randint(0, max_coord)) for _ in range(n)]

# Configuración del experimento
initial_n = 500
insertions_total = 3000

# Generar puntos iniciales y del "stream"
initial_points = generate_points(initial_n)
insertion_points = generate_points(insertions_total)

# -------- Estático --------
static_hull = ConvexHull()
for p in initial_points:
    static_hull.append_point(p.x, p.y)
static_hull.calculate_monotone_chain()

static_query_times = []
start = time.time()
for p in insertion_points:
    static_hull.append_point(p.x, p.y)
    static_hull.get_hull()
    static_hull.is_inside_convex_hull(p)
    static_query_times.append(time.time() - start)

# -------- Dinámico --------
dynamic_hull = DynamicConvexHull()
for p in initial_points:
    dynamic_hull.insert(p)

dynamic_query_times = []
start = time.time()
for p in insertion_points:
    dynamic_hull.insert(p)
    dynamic_hull.get_hull()
    dynamic_hull.is_inside(p)
    dynamic_query_times.append(time.time() - start)

# Eje X
x_values = list(range(1, insertions_total + 1))

# Graficar resultados
plt.figure(figsize=(10, 6))
plt.plot(x_values, static_query_times, label="Static", linestyle='--')
plt.plot(x_values, dynamic_query_times, label="Dynamic", linestyle='-')
plt.xlabel("Number of Insertions")
plt.ylabel("Cumulative Time (seconds)")
plt.title("Cumulative Time for continue Insertions and Queries")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
