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
        try:
            new_ch = ConvexHull()
            new_ch.append_point(point.x, point.y)
            new_ch.get_hull()
        except Exception as e:
            print(f"Error creando nuevo ConvexHull: {str(e)}")
            return

        i = 0
        while i < len(self.structures):
            if self.structures[i] is None:
                self.structures[i] = new_ch
                self._is_outdated = True
                return
            else:
                combined = ConvexHull()
                combined.points = self.structures[i].get_hull() + new_ch.get_hull()
                
                try:
                    combined.get_hull()
                except Exception as e:
                    print(f"Error combinando hulls en nivel {i}: {str(e)}")
                    i += 1
                    continue
                
                self.structures[i] = None
                self.deletions[i] = set()
                new_ch = combined
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
                        
                        if len(new_points) < 3 and len(new_points) > 0:
                            new_ch = ConvexHull()
                            for p in new_points:
                                new_ch.append_point(p.x, p.y)
                            new_ch.hull = new_points.copy()
                        elif len(new_points) == 0:
                            new_ch = None
                        else:
                            new_ch = ConvexHull()
                            for p in new_points:
                                new_ch.append_point(p.x, p.y)
                            try:
                                new_ch.get_hull()
                            except Exception as e:
                                print(f"Error reconstruyendo hull: {str(e)}")
                                new_ch.hull = new_points.copy()
                        
                        self.structures[i] = new_ch
                        self.deletions[i] = set()
                    
                    self._is_outdated = True
                    return True
        return False

    def _recalculate_global_hull(self):
        all_points = []
        for S, deleted in zip(self.structures, self.deletions):
            if S is not None:
                source = S.hull if hasattr(S, 'hull') and S.hull else S.points
                all_points += [p for p in source if (p.x, p.y) not in deleted]
        
        final = ConvexHull()
        final.points = all_points
        
        if len(all_points) == 0:
            final.hull = []
        elif len(all_points) < 3:
            final.hull = all_points.copy()
        else:
            try:
                final.get_hull()
            except Exception as e:
                print(f"Error calculando hull global: {str(e)}")
                final.hull = all_points.copy()
        
        self._global_hull = final
        self._is_outdated = False

    def get_hull(self):
        if self._is_outdated or self._global_hull is None:
            self._recalculate_global_hull()
        return self._global_hull.hull

    def is_inside(self, point):
        self.get_hull()
        try:
            return self._global_hull.is_inside_convex_hull(point)
        except Exception as e:
            print(f"Error verificando punto en hull: {str(e)}")
            return False