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
insertions_total = 2000
query_interval = 100  # cada cuántas inserciones se consulta el hull

# Generar puntos iniciales y de inserción
initial_points = generate_points(initial_n)
insertion_points = generate_points(insertions_total)

# --- Estático: inserciones intercaladas + consulta periódica ---
ch = ConvexHull()
for p in initial_points:
    ch.append_point(p.x, p.y)
ch.calculate_monotone_chain()

static_times = []
start = time.time()
for i, p in enumerate(insertion_points, 1):
    ch.append_point(p.x, p.y)
    if i % query_interval == 0:
        ch.calculate_monotone_chain()
        static_times.append(time.time() - start)

# --- Dinámico: inserciones intercaladas + consulta periódica ---
dch = DynamicConvexHull()
for p in initial_points:
    dch.insert(p)

dynamic_times = []
start = time.time()
for i, p in enumerate(insertion_points, 1):
    dch.insert(p)
    if i % query_interval == 0:
        dch.get_combined_hull()
        dynamic_times.append(time.time() - start)

# Preparar eje X (número acumulado de inserciones)
x_values = list(range(query_interval, insertions_total + 1, query_interval))

# Graficar resultados
plt.figure(figsize=(10, 6))
plt.plot(x_values, static_times, marker='o', label='Estático (recalcula cada consulta)')
plt.plot(x_values, dynamic_times, marker='s', label='Dinámico (Bentley-Saxe)')
plt.xlabel("Puntos insertados adicionalmente")
plt.ylabel("Tiempo acumulado (segundos)")
plt.title("Rendimiento con inserciones intercaladas y consultas periódicas")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
