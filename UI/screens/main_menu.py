import pygame
from UI.screens.screen import Screen


class MainMenuScreen(Screen):
    def __init__(self, manager):
        super().__init__(manager)
        self.screen_id = 0
        self.font = pygame.font.SysFont(None, 48)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.swift(1)  # 切换到战斗界面

    def draw(self, screen):
        screen.fill((30, 30, 30))
        text = self.font.render("Press SPACE to start battle", True, (255, 255, 255))
        screen.blit(text, (100, 200))
