import pygame
from UI.screens.screen import Screen
import utility.data


class StageSelectScreen(Screen):
    def __init__(self, manager, info=None):
        super().__init__(manager)
        self.screen_id = 2

        # Title text
        self.title_text = pygame.font.SysFont("arial", 32, bold=True).render("Select Stage", True, (255, 255, 255))
        self.title_text_rect = self.title_text.get_rect(center=(352, 50))

        # Background image
        raw_bg = pygame.image.load("assets/image/background.png").convert()
        self.background = pygame.transform.scale(raw_bg, (704, 512))

        # Back button
        font = pygame.font.SysFont("arial", 24)
        self.back_text = font.render("← Back", True, (255, 255, 255))
        self.back_rect = self.back_text.get_rect(topleft=(10, 10))

        # Character icon (top-right corner)
        raw_icon = pygame.image.load("assets/image/CharacterIcon.png").convert_alpha()
        self.char_icon = pygame.transform.smoothscale(raw_icon, (64, 64))
        self.char_icon_rect = self.char_icon.get_rect(topright=(690, 10))

        self.font = pygame.font.SysFont("arial", 20)

        # Find the first locked level index
        try:
            self.first_locked_index = utility.data.LEVEL_PROGRESS.index(0)
        except ValueError:
            self.first_locked_index = len(utility.data.LEVEL_PROGRESS)

        # Build stage icons and metadata
        self.stage_data = []
        for i in range(7):
            icon_img = pygame.image.load("assets/image/stage.png").convert_alpha()
            icon = pygame.transform.smoothscale(icon_img, (64, 64))
            rect = icon.get_rect(center=(130 + i * 75, 250))

            # Stage label
            label = self.font.render(str(i + 1), True, (255, 255, 255))
            label_rect = label.get_rect(center=(rect.centerx, rect.centery - 50))

            # Unlock status
            unlocked = i <= self.first_locked_index
            if not unlocked:
                icon.set_alpha(100)

            # Star rating (if cleared)
            star_image = None
            star_rect = None
            progress = utility.data.LEVEL_PROGRESS[i] if i < len(utility.data.LEVEL_PROGRESS) else 0
            if progress in [1, 2, 3]:
                star_image = pygame.image.load(f"assets/image/star_{progress}.png").convert_alpha()
                star_image = pygame.transform.smoothscale(star_image, (50, 20))
                star_rect = star_image.get_rect(center=(rect.centerx, rect.bottom + 5))

            self.stage_data.append({
                "icon": icon,
                "rect": rect,
                "label": label,
                "label_rect": label_rect,
                "unlocked": unlocked,
                "star": star_image,
                "star_rect": star_rect
            })

    def handle_event(self, screen, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos

            # Clicked back button
            if self.back_rect.collidepoint(mouse_pos):
                self.swift(0)
                return

            # Clicked character icon
            if self.char_icon_rect.collidepoint(mouse_pos):
                self.swift(3)
                return

            # Clicked stage icon
            for i, data in enumerate(self.stage_data):
                if data["rect"].collidepoint(mouse_pos):
                    if not data["unlocked"]:
                        return
                    utility.data.CURRENT_STAGE = i + 1
                    self.swift(4)
                    return

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        screen.blit(self.title_text, self.title_text_rect)
        screen.blit(self.back_text, self.back_rect)
        screen.blit(self.char_icon, self.char_icon_rect)

        for data in self.stage_data:
            screen.blit(data["icon"], data["rect"])
            screen.blit(data["label"], data["label_rect"])
            if data["star"]:
                screen.blit(data["star"], data["star_rect"])