from point import Point

class ConvexHull:
    def __init__(self):
        self.points = []
        self.hull = []
        self.is_calculated = False

    def cross(self, a, b, c):
        return (b.x - a.x)*(c.y - a.y) - (b.y - a.y)*(c.x - a.x)

    def calculate_monotone_chain(self):
        if len(self.points) < 3:
            self.hull = []
            self.is_calculated = False
            return

        ordered = sorted(self.points, key=lambda p: (p.x, p.y))
        L, U = [], []

        for p in ordered:
            while len(L) >= 2 and self.cross(L[-2], L[-1], p) <= 0:
                L.pop()
            L.append(p)

        for p in reversed(ordered):
            while len(U) >= 2 and self.cross(U[-2], U[-1], p) <= 0:
                U.pop()
            U.append(p)

        self.hull = L[:-1] + U[:-1]
        self.is_calculated = True

    def append_point(self, x, y):
        self.points.append(Point(x, y))

    def is_inside_convex_hull(self, point):
        if not self.is_calculated or len(self.hull) < 3:
            return False
        n = len(self.hull)
        for i in range(n):
            a, b = self.hull[i], self.hull[(i + 1) % n]
            if self.cross(a, b, point) < 0:
                return False
        return True

    def clear(self):
        self.points.clear()
        self.hull.clear()
        self._is_calculated = False