# screens/dummy_screen.py
import pygame

class DummyScreen:
    def __init__(self, manager):
        self.manager = manager
        self.color = (100, 100, 255)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            print("Space pressed on DummyScreen!")

    def update(self):
        pass  # 可以添加动画、计时器等逻辑

    def draw(self, screen):
        screen.fill(self.color)
        # 简单地显示一段文字
        font = pygame.font.SysFont(None, 36)
        text = font.render("This is DummyScreen", True, (255, 255, 255))
        screen.blit(text, (50, 50))