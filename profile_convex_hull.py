import cProfile
import pstats
import random
import os
from convex_hull import ConvexHull
from dynamic_convex_hull import DynamicConvexHull
from point import Point

# Configuración
N_INSERTIONS = 2000
N_QUERIES = 200
SEED = 42
OUTPUT_STATIC = "data/profile_static.csv"
OUTPUT_DYNAMIC = "data/profile_dynamic.csv"

# Asegurar directorio de salida
os.makedirs("data", exist_ok=True)

def generate_points(n, max_coord=1000):
    return [Point(random.randint(0, max_coord), random.randint(0, max_coord)) for _ in range(n)]

def write_header(f):
    f.write("structure,phase,method_name,total_time,cumulative_time,per_call_time\n")

def write_stats(f, structure_name, phase, stats: pstats.Stats, filter_keywords):
    stats.strip_dirs()
    for func, (cc, nc, tt, ct, callers) in stats.stats.items():
        if any(keyword in func[2] for keyword in filter_keywords):
            per_call = ct / nc if nc > 0 else 0
            f.write(f"{structure_name},{phase},{func[2]},{tt:.6f},{ct:.6f},{per_call:.6f}\n")

# ------------------------
# PERFILAMIENTO ESTÁTICO
# ------------------------
random.seed(SEED)
points = generate_points(N_INSERTIONS)
queries = generate_points(N_QUERIES)

with open(OUTPUT_STATIC, "w") as f:
    write_header(f)
    ch = ConvexHull()
    for p in points:
        ch.append_point(p.x, p.y)
    
    profiler = cProfile.Profile()
    profiler.enable()
    ch.calculate_monotone_chain()
    for q in queries:
        ch.is_inside_convex_hull(q)
    profiler.disable()
    
    stats = pstats.Stats(profiler)
    write_stats(f, "static", "calculate_and_query", stats, ["calculate_monotone_chain", "is_inside_convex_hull"])

# ------------------------
# PERFILAMIENTO DINÁMICO
# ------------------------
random.seed(SEED)
points = generate_points(N_INSERTIONS)
queries = generate_points(N_QUERIES)

with open(OUTPUT_DYNAMIC, "w") as f:
    write_header(f)
    dch = DynamicConvexHull()
    
    profiler = cProfile.Profile()
    profiler.enable()
    for p in points:
        dch.insert(p)
    for q in queries:
        dch.is_inside(q)
    profiler.disable()
    
    stats = pstats.Stats(profiler)
    write_stats(f, "dynamic", "insert_and_query", stats, ["insert", "calculate_monotone_chain", "is_inside", "is_inside_convex_hull"])
