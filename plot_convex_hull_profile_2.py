import matplotlib.pyplot as plt
import time
import random
from point import Point
from convex_hull import ConvexHull
from dynamic_convex_hull import DynamicConvexHull

def generate_points(n, max_coord=1000):
    return [Point(random.randint(0, max_coord), random.randint(0, max_coord)) for _ in range(n)]

# Configuración del experimento
initial_n = 500
stream_n = 3000  # cuántos puntos nuevos se insertan y se consulta si están dentro del hull

# Generar puntos iniciales y del "stream"
initial_points = generate_points(initial_n)
stream_points = generate_points(stream_n)

# -------- Estático --------
ch = ConvexHull()
for p in initial_points:
    ch.append_point(p.x, p.y)
ch.calculate_monotone_chain()

static_query_times = []
start = time.time()
for p in stream_points:
    ch.append_point(p.x, p.y)
    ch.calculate_monotone_chain()
    ch.is_inside_convex_hull(p)  # Consulta tras cada inserción
    static_query_times.append(time.time() - start)

# -------- Dinámico --------
dch = DynamicConvexHull()
for p in initial_points:
    dch.insert(p)

dynamic_query_times = []
start = time.time()
for p in stream_points:
    dch.insert(p)
    dch.is_inside(p)  # Consulta tras cada inserción
    dynamic_query_times.append(time.time() - start)

# Eje X
x_values = list(range(1, stream_n + 1))

# Graficar resultados
plt.figure(figsize=(10, 6))
plt.plot(x_values, static_query_times, label="Estático (recalcula + consulta)", linestyle='--')
plt.plot(x_values, dynamic_query_times, label="Dinámico (insert + consulta amortizada)", linestyle='-')
plt.xlabel("Número de puntos procesados del flujo (stream)")
plt.ylabel("Tiempo acumulado (segundos)")
plt.title("Comparación de rendimiento en flujo continuo de inserciones y consultas")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
