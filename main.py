import pygame
from UI.screen_manager import ScreenManager

pygame.init()
screen = pygame.display.set_mode((704, 448))
pygame.display.set_caption("Infinity Heaven")
clock = pygame.time.Clock()

manager = ScreenManager()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        manager.handle_event(event)

    manager.update()
    manager.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
