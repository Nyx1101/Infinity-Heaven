import pygame
from UI.screens.screen import Screen
import utility.data


class MainMenuScreen(Screen):
    def __init__(self, manager, data=None):
        super().__init__(manager)
        self.screen_id = 0

        # Load and scale the background and logo image
        raw_background = pygame.image.load("assets/image/background1.png").convert()
        self.background = pygame.transform.scale(raw_background, (704, 512))
        raw_logo = pygame.image.load("assets/image/logo.png").convert_alpha()
        self.logo = pygame.transform.scale(raw_logo, (192, 192))

        # Fonts
        self.font = pygame.font.SysFont(None, 48)
        self.button_font = pygame.font.SysFont(None, 36)

        # Define button rectangles
        self.start_button = pygame.Rect(250, 300, 200, 50)
        self.quit_button = pygame.Rect(250, 370, 200, 50)

    def handle_event(self, screen, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.start_button.collidepoint(event.pos):
                # Go to story screen if not seen, otherwise stage selection
                if utility.data.STORY_PROGRESS[0] == 0:
                    self.swift(7, {"stage": 0, "progress": "start"})
                else:
                    self.swift(2)
            elif self.quit_button.collidepoint(event.pos):
                # Exit game
                self.manager.quit = True

    def draw(self, screen):
        screen.blit(self.background, (0, 0))

        # Draw game logo
        logo_rect = self.logo.get_rect(center=(screen.get_width() // 2, 160))
        screen.blit(self.logo, logo_rect)

        # Draw Start button
        pygame.draw.rect(screen, (70, 130, 180), self.start_button)
        start_text = self.button_font.render("Start", True, (255, 255, 255))
        screen.blit(start_text, start_text.get_rect(center=self.start_button.center))

        # Draw Quit button
        pygame.draw.rect(screen, (180, 70, 70), self.quit_button)
        quit_text = self.button_font.render("Quit", True, (255, 255, 255))
        screen.blit(quit_text, quit_text.get_rect(center=self.quit_button.center))
