import pygame
from UI.screens.screen import Screen


class DifficultyScreen(Screen):
    def __init__(self, manager, info=None):
        super().__init__(manager, info)
        self.screen_id = 4

        # Set up fonts
        self.font = pygame.font.SysFont("arial", 20)
        self.big_font = pygame.font.SysFont("arial", 26)

        # Load and scale background image
        raw_background = pygame.image.load("assets/image/background2.png")
        self.background = pygame.transform.scale(raw_background, (704, 512))

        # Render "Back" text and get its rectangle for click detection
        font = pygame.font.SysFont("arial", 24)
        self.back_text = font.render("← Back", True, (255, 255, 255))
        self.back_rect = self.back_text.get_rect(topleft=(10, 10))

        # Difficulty levels: 0=Easy, 1=Normal, 2=Hard
        self.difficulty_level = 1
        self.difficulty_buttons = self.create_buttons(250, ["Easy", "Normal", "Hard"])

        # Optional limit mode toggle
        self.limit = False
        self.limit_rect = pygame.Rect(500, 100, 180, 40)

        # "Select Characters" button
        self.select_rect = pygame.Rect(500, 350, 180, 50)

    def create_buttons(self, x, labels):
        """
        Create button rects and associate with labels.
        """
        buttons = []
        for i, label in enumerate(labels):
            rect = pygame.Rect(x, 120 + i * 60, 200, 40)
            buttons.append((rect, label))
        return buttons

    def draw_buttons(self, screen):
        """
        Draw difficulty buttons with highlight on selected one.
        """
        for i, (rect, label) in enumerate(self.difficulty_buttons):
            color = (255, 0, 0) if i == self.difficulty_level else (255, 255, 255)
            pygame.draw.rect(screen, (0, 0, 0), rect)
            pygame.draw.rect(screen, color, rect, 2)
            text = self.font.render(label, True, color)
            screen.blit(text, (rect.x + 60, rect.y + 10))

    def handle_event(self, screen, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()

            # Click on a difficulty button
            for i, (rect, _) in enumerate(self.difficulty_buttons):
                if rect.collidepoint(pos):
                    self.difficulty_level = i

            # Toggle limit mode
            if self.limit_rect.collidepoint(pos):
                self.limit = not self.limit

            # Click "Select Characters" to proceed
            if self.select_rect.collidepoint(pos):
                difficulty_map = [
                    {"HP": 1, "Attack": 1, "Defense": 1},
                    {"HP": 1.33, "Attack": 1.1, "Defense": 1.1},
                    {"HP": 1.52, "Attack": 1.15, "Defense": 1.15},
                ]
                result = {"items": difficulty_map[self.difficulty_level]}
                result["items"]["Limit"] = self.limit
                self.swift(3, data=result)

            # Click "Back" button
            if pygame.Rect(20, 20, 80, 40).collidepoint(pos):
                self.swift()

    def draw(self, screen):
        # Draw background
        screen.blit(self.background, (0, 0))

        # Draw back button
        screen.blit(self.back_text, self.back_rect)

        # Draw title
        screen.blit(self.big_font.render("Select Difficulty", True, (255, 255, 255)), (270, 40))

        # Draw difficulty buttons
        self.draw_buttons(screen)

        # Draw "Select Characters" button
        pygame.draw.rect(screen, (0, 0, 0), self.select_rect)
        pygame.draw.rect(screen, (255, 255, 255), self.select_rect, 2)
        screen.blit(self.font.render("Select Characters", True, (255, 255, 255)),
                    (self.select_rect.x + 10, self.select_rect.y + 15))

        # Show first-time rewards for higher difficulties
        reward_text = ""
        if self.difficulty_level == 1:
            reward_text = "First Time Reward: Elite 1 badge"
        elif self.difficulty_level == 2:
            reward_text = "First Time Reward: Elite 1 and Elite 2 badge"

        if reward_text:
            text_surface = self.font.render(reward_text, True, (255, 255, 0))
            text_rect = text_surface.get_rect(center=(352, self.select_rect.top - 20))
            screen.blit(text_surface, text_rect)
