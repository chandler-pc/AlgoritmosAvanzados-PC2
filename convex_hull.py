from point import Point
import pygame
from config import HULL_LINE_COLOR

class ConvexHull:
    def __init__(self):
        self.points = []
        self.hull = []
        self.is_calculated = False

    def cross(self, a, b, c):
            return (b.x - a.x)*(c.y - a.y) - (b.y - a.y)*(c.x - a.x)

    def calculate_monotone_chain(self):
        if len(self.points) < 3:
            return
        n = len(self.points)
        self.hull = []
        ordered_points = sorted(self.points, key=lambda p: (p.x, p.y))
        U = []
        L = []
        for i in range(n):
            while len(L) >= 2 and self.cross(L[-2], L[-1], ordered_points[i]) <= 0:
                L.pop()
            L.append(ordered_points[i])

        for i in range(n - 1, -1, -1):
            while len(U) >= 2 and self.cross(U[-2], U[-1], ordered_points[i]) <= 0:
                U.pop()
            U.append(ordered_points[i])
        L.pop()
        U.pop()
        self.is_calculated = True
        self.hull = U + L

    def append_point(self, x, y):
        point = Point(x, y)
        self.points.append(point)
        # self.is_calculated = False

    def draw(self, surface):
        for point in self.points:
            point.draw(surface)
        if self.is_calculated:
            n = len(self.hull)
            for i in range(n):
                initial_point = self.hull[i].get_tuple()
                final_point = self.hull[(i + 1) % len(self.hull)].get_tuple()
                pygame.draw.aaline(surface, HULL_LINE_COLOR, initial_point, final_point)

    def point_in_hull(self, point):
        if not self.hull or len(self.hull) < 3:
            return False

        n = len(self.hull)
        for i in range(n):
            a = self.hull[i]
            b = self.hull[(i + 1) % n]
            if self.cross(a, b, point) < 0:
                return False
        return True
