import cProfile
import pstats
import random
import os
from typing import List, Tuple
from app.convex_hull import ConvexHull
from app.dynamic_convex_hull import DynamicConvexHull
from app.point import Point

# Configuración
N_INSERTIONS = 2000
N_QUERIES = 200
SEED = 42
OUTPUT_STATIC = "data/profile_static.csv"
OUTPUT_DYNAMIC = "data/profile_dynamic.csv"

os.makedirs("data", exist_ok=True)

def generate_points(n, max_coord=1000):
    return [Point(random.randint(0, max_coord), random.randint(0, max_coord)) for _ in range(n)]

def write_header(f) -> None:
    f.write('structure,phase,method_name,total_time,cumulative_time,per_call_time\n')

def write_row(f, structure: str, phase: str, method_name: str, total_time: float, cumulative_time: float, per_call_time: float) -> None:
    f.write(f'{structure},{phase},{method_name},{total_time:.6f},{cumulative_time:.6f},{per_call_time:.6f}\n')

def get_method_stats(stats: pstats.Stats, target_keywords: List[str]) -> List[Tuple[str, float, float, float]]:
    ps = stats.strip_dirs().stats

    def matches(key):
        return any(kw in key[2] for kw in target_keywords)

    filtered_keys = list(filter(matches, ps.keys()))

    result = []
    for key in filtered_keys:
        method_name = key[2]
        # cc = ps[key][0]  # Call count (with recursion)
        # nc = ps[key][1]  # Number of calls (without recursion)
        # tt = ps[key][2]  # Total time
        # ct = ps[key][3]  # Cumulative time 
        # _ = ps[key][4]  # Callers
        cc, nc, tt, ct, _ = ps[key]
        per_call = ct / nc if nc > 0 else 0
        result.append((method_name, tt, ct, per_call))
    return result

# ------------------------
# STATIC PROFILING
# ------------------------
random.seed(SEED)
points = generate_points(N_INSERTIONS)
queries = generate_points(N_QUERIES)

with open(OUTPUT_STATIC, "w") as f:
    write_header(f)
    ch = ConvexHull()

    profiler_insert = cProfile.Profile()
    profiler_insert.enable()
    for p in points:
        ch.append_point(p.x, p.y)
        ch.get_hull()
    profiler_insert.disable()

    stats_insert = pstats.Stats(profiler_insert)
    for method, tt, ct, pc in get_method_stats(stats_insert, ["append_point", "get_hull"]):
        write_row(f, "static", "insertions_with_recalculation", method, tt, ct, pc)

    profiler_query = cProfile.Profile()
    profiler_query.enable()
    for q in queries:
        ch.is_inside_convex_hull(q)
    profiler_query.disable()

    stats_query = pstats.Stats(profiler_query)
    for method, tt, ct, pc in get_method_stats(stats_query, ["is_inside_convex_hull"]):
        write_row(f, "static", "query_only", method, tt, ct, pc)

# ------------------------
# DYNAMIC PROFILING
# ------------------------
random.seed(SEED)
points = generate_points(N_INSERTIONS)
queries = generate_points(N_QUERIES)

with open(OUTPUT_DYNAMIC, "w") as f:
    write_header(f)
    dch = DynamicConvexHull()

    profiler_insert = cProfile.Profile()
    profiler_insert.enable()
    for p in points:
        dch.insert(p)
        dch.get_hull()
    profiler_insert.disable()

    stats_insert = pstats.Stats(profiler_insert)
    for method, tt, ct, pc in get_method_stats(stats_insert, ["insert", "get_combined_hull"]):
        write_row(f, "dynamic", "insertions_with_recalculation", method, tt, ct, pc)

    profiler_query = cProfile.Profile()
    profiler_query.enable()
    for q in queries:
        dch.is_inside(q)
    profiler_query.disable()

    stats_query = pstats.Stats(profiler_query)
    for method, tt, ct, pc in get_method_stats(stats_query, ["is_inside_convex_hull"]):
        write_row(f, "dynamic", "query_only", method, tt, ct, pc)
