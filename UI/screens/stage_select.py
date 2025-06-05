import pygame
from UI.screens.screen import Screen
import utility.data


class StageSelectScreen(Screen):
    def __init__(self, manager, info=None):
        super().__init__(manager)
        self.screen_id = 2

        # 背景
        raw_bg = pygame.image.load("assets/image/background.png").convert()
        self.background = pygame.transform.scale(raw_bg, (704, 512))

        # characters 图标（右上角）
        raw_icon = pygame.image.load("assets/image/CharacterIcon.png").convert_alpha()
        self.char_icon = pygame.transform.smoothscale(raw_icon, (64, 64))
        self.char_icon_rect = self.char_icon.get_rect(topright=(690, 10))  # 右上角位置

        self.stage_icons = []
        for i in range(8):
            img = pygame.image.load(f"assets/image/271.png").convert_alpha()
            icon = pygame.transform.smoothscale(img, (64, 64))
            rect = icon.get_rect()
            rect.center = (90 + i * 75, 250)  # 水平排布
            self.stage_icons.append((icon, rect))

    def handle_event(self, screen, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos

            # 点击 characters 图标
            if self.char_icon_rect.collidepoint(mouse_pos):
                self.swift(3)  # 跳转角色界面
                return

            # 点击关卡图标
            for i, (_, rect) in enumerate(self.stage_icons):
                if rect.collidepoint(mouse_pos):
                    utility.data.CURRENT_STAGE = i + 1
                    self.swift(4)
                    return

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        screen.blit(self.char_icon, self.char_icon_rect)

        for icon, rect in self.stage_icons:
            screen.blit(icon, rect)
