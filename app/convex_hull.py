from typing import List
from app.point import Point

class ConvexHull:
    def __init__(self):
        self.points: List[Point] = []
        self.hull: List[Point] = []
        self.is_calculated: bool = False

    def calculate_monotone_chain(self) -> list[Point]:
        try:
            if len(self.points) == 0:
                self.hull = []
                self.is_calculated = True
                return self.hull
            elif len(self.points) == 1:
                self.hull = self.points.copy()
                self.is_calculated = True
                return self.hull
            elif len(self.points) == 2:
                self.hull = self.points.copy()
                self.is_calculated = True
                return self.hull
            
            try:
                ordered_points = sorted(self.points, key=lambda p: (p.x, p.y))
            except TypeError as e:
                print(f"Error sorting points: {e}")
                ordered_points = sorted(self.points)
            
            n = len(ordered_points)
            U = []
            L = []
            
            for i in range(n):
                while len(L) >= 2:
                    try:
                        cross = Point.cross(L[-2], L[-1], ordered_points[i])
                        if cross <= 0:
                            L.pop()
                        else:
                            break
                    except Exception as e:
                        print(f"Error in lower hull calculation: {e}")
                        break
                L.append(ordered_points[i])

            for i in range(n - 1, -1, -1):
                while len(U) >= 2:
                    try:
                        cross = Point.cross(U[-2], U[-1], ordered_points[i])
                        if cross <= 0:
                            U.pop()
                        else:
                            break
                    except Exception as e:
                        print(f"Error in upper hull calculation: {e}")
                        break
                U.append(ordered_points[i])
            
            L.pop()
            U.pop()
            
            self.hull = U + L
            self.is_calculated = True
            return self.hull
        
        except Exception as e:
            print(f"Critical error in convex hull calculation: {e}")
            self.hull = self.points.copy()
            self.is_calculated = True
            return self.hull

    def remove_point(self, point: Point) -> bool:
        try:
            if point in self.points:
                self.points.remove(point)
                self.hull.clear()
                self.is_calculated = False
                return True
            return False
        except Exception as e:
            print(f"Error removing point: {e}")
            return False

    def append_point(self, x, y):
        try:
            if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
                raise ValueError("Coordinates must be numeric")
                
            self.points.append(Point(x, y))
            self.is_calculated = False
        except Exception as e:
            print(f"Error appending point ({x}, {y}): {e}")

    def is_inside_convex_hull(self, point: Point) -> bool:
        try:
            if not self.hull or len(self.hull) < 3:
                return False
                
            n = len(self.hull)
            for i in range(n):
                a, b = self.hull[i], self.hull[(i + 1) % n]
                try:
                    cross = Point.cross(a, b, point)
                    if cross < 0:
                        return False
                except Exception as e:
                    print(f"Error in cross product calculation: {e}")
                    
            return True
        except Exception as e:
            print(f"Error in point containment check: {e}")
            return False

    def clear(self):
        self.points.clear()
        self.hull.clear()
        self.is_calculated = False

    def get_hull(self):
        if not self.is_calculated:
            try:
                return self.calculate_monotone_chain()
            except Exception as e:
                print(f"Error getting hull: {e}")
                return self.hull
        return self.hull

    def __str__(self):
        if not self.hull:
            return "Convex hull is empty."
        try:
            return "Convex Hull:\n" + "\n".join(str(p) for p in self.hull)
        except Exception as e:
            return f"Error stringifying hull: {e}"