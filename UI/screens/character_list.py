import pygame
from UI.screens.screen import Screen
import utility.data


class CharacterListScreen(Screen):
    def __init__(self, manager, info=None):
        super().__init__(manager, info)
        self.screen_id = 3
        if self.info is not None:
            self.mode = "Select"  # If info is passed, enable character selection mode
            self.selected = []    # List to store selected character indexes

        # Load and scale background image
        raw_bg = pygame.image.load("assets/image/background3.png").convert()
        self.background = pygame.transform.scale(raw_bg, (704, 512))

        # Create the "Back" button
        font = pygame.font.SysFont("arial", 24)
        self.back_text = font.render("← Back", True, (255, 255, 255))
        self.back_rect = self.back_text.get_rect(topleft=(10, 10))

        # Get unlocked characters based on level progress
        level_progress = utility.data.LEVEL_PROGRESS
        self.unlocked = [True] * 3 + [lv > 0 for lv in level_progress[:6]]

        # Create character icon buttons (3x3 grid)
        self.char_buttons = []
        border_raw = pygame.image.load("assets/image/border.png").convert_alpha()

        rows, cols = 3, 3
        icon_size = (96, 96)
        icon_w, icon_h = icon_size
        margin_x = (704 - cols * icon_w) // (cols + 1)  # Horizontal spacing
        margin_y = 40  # Vertical spacing

        for i in range(9):
            img = pygame.image.load(f"assets/image/character{i+1}.png").convert_alpha()
            icon = pygame.transform.smoothscale(img, icon_size)
            rect = icon.get_rect()

            row = i // cols
            col = i % cols
            x = margin_x + col * (icon_w + margin_x)
            y = 80 + row * (icon_h + margin_y)
            rect.topleft = (x, y)

            # Scale border and align to center of icon
            border = pygame.transform.smoothscale(border_raw, (icon_w + 10, icon_h + 10))
            border_rect = border.get_rect(center=rect.center)

            # Determine if character is unlocked
            active = self.unlocked[i] if i < len(self.unlocked) else False

            self.char_buttons.append({
                "index": i,
                "icon": icon,
                "rect": rect,
                "active": active,
                "border": border,
                "border_rect": border_rect,
            })

        # Create "Confirm" button
        self.confirm_font = pygame.font.SysFont("arial", 22)
        self.confirm_text = self.confirm_font.render("Confirm", True, (255, 255, 255))
        self.confirm_rect = pygame.Rect(550, 440, 120, 40)

    def handle_event(self, screen, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos

            # Handle back button click
            if self.back_rect.collidepoint(mouse_pos):
                self.swift()
                return

            # Handle confirm button in selection mode
            if hasattr(self, "mode") and self.confirm_rect.collidepoint(mouse_pos):
                self.info["formation"] = self.selected
                if utility.data.STORY_PROGRESS[utility.data.CURRENT_STAGE] == 0:
                    self.info["stage"] = utility.data.CURRENT_STAGE
                    self.info["progress"] = "start"
                    self.swift(7, self.info)
                else:
                    self.swift(1, self.info)
                return

            # Handle character icon click
            for button in self.char_buttons:
                if button["active"] and button["rect"].collidepoint(mouse_pos):
                    if hasattr(self, "mode"):
                        if button["index"] in self.selected:
                            self.selected.remove(button["index"])  # Deselect
                            return
                        else:
                            self.selected.append(button["index"])  # Select
                            return
                    self.swift(5, data=button["index"])  # Open character detail (non-select mode)
                    return

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        screen.blit(self.back_text, self.back_rect)

        for button in self.char_buttons:
            icon = button["icon"].copy()
            rect = button["rect"]

            # Draw border
            screen.blit(button["border"], button["border_rect"])

            # Render locked characters with transparency
            if not button["active"]:
                icon.set_alpha(80)

            screen.blit(icon, rect)

            # Highlight selected characters
            if button["index"] in getattr(self, "selected", []):
                pygame.draw.rect(screen, (255, 255, 0), rect.inflate(4, 4), width=3)

        # Draw confirm button if in selection mode
        if hasattr(self, "mode"):
            pygame.draw.rect(screen, (50, 180, 100), self.confirm_rect, border_radius=6)
            text_rect = self.confirm_text.get_rect(center=self.confirm_rect.center)
            screen.blit(self.confirm_text, text_rect)
