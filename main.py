import pygame
from convex_hull import ConvexHull
from point import Point
from config import SIZE, BACKGROUND_COLOR, POINT_COLOR_INSIDE, POINT_COLOR_OUTSIDE, POINT_RADIUS

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

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    convex_hull.calculate_monotone_chain()

        screen.fill(BACKGROUND_COLOR)
        convex_hull.draw(screen)

        for p in test_points:
            color = POINT_COLOR_INSIDE if convex_hull.point_in_hull(p) else POINT_COLOR_OUTSIDE
            pygame.draw.circle(screen, color, p.get_tuple(), POINT_RADIUS)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
