import pygame
from app.convex_hull import ConvexHull
from app.point import Point
from app.utils import draw_point, draw_convex_hull
from app.config import SIZE, BACKGROUND_COLOR, POINT_COLOR_INSIDE, POINT_COLOR_OUTSIDE, POINT_RADIUS

convex_hull = ConvexHull()
test_points = []

def main():
    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption("Convex Hull - Monotone Chain Algorithm")
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if event.button == 1:
                    convex_hull.append_point(x, y)
                elif event.button == 3:
                    test_points.append(Point(x, y))
                elif event.button == 2:
                    for p in convex_hull.points:
                        if Point.distance(p, Point(x, y)) < POINT_RADIUS:
                            convex_hull.points.remove(p)
                            break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    convex_hull.get_hull()

        screen.fill(BACKGROUND_COLOR)

        for p in convex_hull.points:
            draw_point(screen, p, color=(255, 255, 255), radius=POINT_RADIUS)

        if convex_hull.is_calculated:
            draw_convex_hull(screen, convex_hull)

        for p in test_points:
            color = POINT_COLOR_INSIDE if convex_hull.is_inside_convex_hull(p) else POINT_COLOR_OUTSIDE
            draw_point(screen, p, color=color, radius=POINT_RADIUS)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
