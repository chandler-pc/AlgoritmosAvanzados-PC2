import matplotlib.pyplot as plt
import numpy as np
import time
from app.convex_hull import ConvexHull
from app.dynamic_convex_hull import DynamicConvexHull
from app.point import Point

def random_points(n):
    return [Point(float(x), float(y)) for x, y in zip(
        np.random.uniform(0, 1000, n),
        np.random.uniform(0, 1000, n)
    )]

def static_hull_delete_benchmark(points, points_to_delete):
    current_points = list(points)
    total_time = 0.0
    for pt in points_to_delete:
        current_points = [p for p in current_points if (p.x, p.y) != (pt.x, pt.y)]
        ch = ConvexHull()
        for p in current_points:
            ch.append_point(p.x, p.y)
        t0 = time.time()
        ch.get_hull()
        t1 = time.time()
        total_time += (t1 - t0)
    return total_time

def dynamic_hull_delete_benchmark(points, points_to_delete):
    dch = DynamicConvexHull()
    for p in points:
        dch.insert(p)
    t0 = time.time()
    for pt in points_to_delete:
        dch.delete(pt)
    t1 = time.time()
    return t1 - t0

def main():
    sizes = [1000, 2000, 5000]
    percent_delete = 0.4
    times_static = []
    times_dynamic = []

    for n in sizes:
        pts = random_points(n)
        idx_to_delete = np.random.choice(range(n), int(n * percent_delete), replace=False)
        pts_to_del = [pts[i] for i in idx_to_delete]

        t_static = static_hull_delete_benchmark(pts, pts_to_del)
        t_dynamic = dynamic_hull_delete_benchmark(pts, pts_to_del)

        times_static.append(t_static)
        times_dynamic.append(t_dynamic)

        print(f"N={n} Eliminados={len(pts_to_del)}: Estático={t_static:.4f}s | Dinámico={t_dynamic:.4f}s")

    plt.figure(figsize=(9,6))
    plt.plot(sizes, times_static, marker='o', label='Hull Estático (reconstrucción por eliminación)')
    plt.plot(sizes, times_dynamic, marker='s', label='Hull Dinámico (Bentley-Saxe)')
    plt.xlabel('Cantidad de puntos')
    plt.ylabel('Tiempo total de eliminaciones (segundos)')
    plt.title('Comparación: Eliminación en Convex Hull Estático vs Dinámico')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    main()
