from convex_hull import ConvexHull
from point import Point

class DynamicConvexHull:
    def __init__(self):
        self.structures = []
        self._global_hull = None
        self._is_outdated = True

    def insert(self, point):
        new_block = [point]
        i = 0
        while i < len(self.structures):
            if self.structures[i] is None:
                self.structures[i] = new_block
                self._is_outdated = True
                return
            else:
                new_block = self.structures[i] + new_block
                self.structures[i] = None
                i += 1
        self.structures.append(new_block)
        self._is_outdated = True

    def _recalculate_global_hull(self):
        all_points = []
        for s in self.structures:
            if s:
                all_points.extend(s)
        ch = ConvexHull()
        ch.points = all_points
        ch.calculate_monotone_chain()
        self._global_hull = ch
        self._is_outdated = False

    def is_inside(self, point):
        if self._is_outdated or self._global_hull is None:
            self._recalculate_global_hull()
        return self._global_hull.is_inside_convex_hull(point)

    def get_combined_hull(self):
        if self._is_outdated or self._global_hull is None:
            self._recalculate_global_hull()
        return self._global_hull.hull
