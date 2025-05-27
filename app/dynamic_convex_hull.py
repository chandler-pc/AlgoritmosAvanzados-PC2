from app.convex_hull import ConvexHull
from app.point import Point
from typing import Optional

class DynamicConvexHull:
    def __init__(self):
        self.structures: list[Optional[ConvexHull]] = []
        self._global_hull: ConvexHull = None
        self._is_outdated = True

    def insert(self, point):
        new_ch = ConvexHull()
        new_ch.append_point(point.x, point.y)
        new_ch.get_hull()
        
        i = 0
        while i < len(self.structures):
            if self.structures[i] is None: # new structure
                self.structures[i] = new_ch
                self._is_outdated = True
                return
            else: # combine structures
                combined = ConvexHull()
                combined.points = self.structures[i].get_hull() + new_ch.get_hull()
                combined.get_hull()
                new_ch = combined
                self.structures[i] = None
                i += 1
        self.structures.append(new_ch)
        self._is_outdated = True


    def _recalculate_global_hull(self):
        all_points = []
        for s in self.structures:
            if s:
                all_points.extend(s.hull)
        final = ConvexHull()
        final.points = all_points
        final.get_hull()
        self._global_hull = final
        self._is_outdated = False

    def get_hull(self):
        if self._is_outdated or self._global_hull is None:
            self._recalculate_global_hull()
        return self._global_hull.hull


    def is_inside(self, point):
        self.get_hull()
        return self._global_hull.is_inside_convex_hull(point)

