import pygame
from UI.screens.screen import Screen


class SettlementScreen(Screen):
    def __init__(self, manager, info=None):
        super().__init__(manager)
        self.screen_id = 6
        self.result = info

        if self.result == "win":
            image_path = "assets/image/win.png"
        else:
            image_path = "assets/image/lose.png"

        raw_background = pygame.image.load(image_path).convert()
        self.background = pygame.transform.scale(raw_background, (704, 512))

    def handle_event(self, screen, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.swift(2)

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
