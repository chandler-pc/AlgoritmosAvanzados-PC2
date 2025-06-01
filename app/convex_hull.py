from app.point import Point

class ConvexHull:
    def __init__(self):
        self.points = []
        self.hull = []
        self.is_calculated = False

    def calculate_monotone_chain(self):
        if len(self.points) < 3:
            self.hull = []
            self.is_calculated = False
            return self.points
        n = len(self.points)
        self.hull = []
        ordered_points = sorted(self.points, key=lambda p: (p.x, p.y))
        U = []
        L = []
        for i in range(n):
            while len(L) >= 2 and Point.cross(L[-2], L[-1], ordered_points[i]) <= 0:
                L.pop()
            L.append(ordered_points[i])

        for i in range(n - 1, -1, -1):
            while len(U) >= 2 and Point.cross(U[-2], U[-1], ordered_points[i]) <= 0:
                U.pop()
            U.append(ordered_points[i])
        L.pop()
        U.pop()
        self.is_calculated = True
        self.hull = U + L
        return self.hull
    
    def remove_point(self, point):
        if point in self.points:
            self.points.remove(point)
        self.hull.clear()
        self.is_calculated = False


    def append_point(self, x, y):
        self.points.append(Point(x, y))

    def is_inside_convex_hull(self, point):
        if len(self.hull) < 3:
            return False
        n = len(self.hull)
        for i in range(n):
            a, b = self.hull[i], self.hull[(i + 1) % n]
            if Point.cross(a, b, point) < 0:
                return False
        return True

    def clear(self):
        self.points.clear()
        self.hull.clear()
        self._is_calculated = False

    def get_hull(self):
        return self.calculate_monotone_chain()

    def __str__(self):
        if not self.hull:
            return "Convex hull is empty."
        return "Convex Hull:\n" + "\n".join(str(p) for p in self.hull)
