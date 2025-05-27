import pygame
from convex_hull import ConvexHull

SIZE = (800,600)

def main():
    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption("Convex Hull - Monotone Chain Algorithm")
    convex_hull = ConvexHull()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = event.pos
                    convex_hull.append_point(x,y)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    convex_hull.calculate_monotone_chain()
        
        screen.fill((125, 0, 125))

        convex_hull.draw(screen)
        
        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    main()