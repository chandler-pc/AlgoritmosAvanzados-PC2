import pygame
from config import HULL_LINE_COLOR, POINT_COLOR_DEFAULT, POINT_RADIUS

def draw_point(surface, point, color=None, radius=None):
    pygame.draw.circle(
        surface,
        color if color else POINT_COLOR_DEFAULT,
        point.get_tuple(),
        radius if radius else POINT_RADIUS
    )

def draw_convex_hull(surface, convex_hull):
    if convex_hull.is_calculated and len(convex_hull.hull) >= 3:
        for i in range(len(convex_hull.hull)):
            a = convex_hull.hull[i].get_tuple()
            b = convex_hull.hull[(i + 1) % len(convex_hull.hull)].get_tuple()
            pygame.draw.aaline(surface, HULL_LINE_COLOR, a, b)
