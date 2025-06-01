from app.convex_hull import ConvexHull
from app.point import Point
from typing import Optional

class DynamicConvexHull:
    def __init__(self):
        self.structures: list[Optional[ConvexHull]] = []
        self.deletions: list[set] = []
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
                self.deletions[i] = set()
                i += 1
        self.structures.append(new_ch)
        self.deletions.append(set())
        self._is_outdated = True

    def delete(self, point):
        key = (point.x, point.y)
        for i, S in enumerate(self.structures):
            if S is not None:
                all_points = [(p.x, p.y) for p in S.points]
                if key in all_points:
                    self.deletions[i].add(key)
                    if len(self.deletions[i]) > len(all_points) // 2:
                        new_points = [p for p in S.points if (p.x, p.y) not in self.deletions[i]]
                        new_ch = ConvexHull()
                        for p in new_points:
                            new_ch.append_point(p.x, p.y)
                        new_ch.get_hull()
                        self.structures[i] = new_ch
                        self.deletions[i] = set()
                    self._is_outdated = True
                    return True
        return False


    def _recalculate_global_hull(self):
        all_points = []
        for S, deleted in zip(self.structures, self.deletions):
            if S is not None:
                all_points += [p for p in S.hull if (p.x, p.y) not in deleted]
                
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

