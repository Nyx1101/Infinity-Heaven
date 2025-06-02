import pygame
import sys
from UI.screens.screen import Screen


class MainMenuScreen(Screen):
    def __init__(self, manager):
        super().__init__(manager)
        self.screen_id = 0

        # 加载背景和 logo
        # 原始加载
        raw_background = pygame.image.load("assets/image/background.jpg").convert()
        # 缩放到屏幕尺寸（704x512）
        self.background = pygame.transform.scale(raw_background, (704, 512))
        # self.logo = pygame.image.load("assets/image/logo.png").convert_alpha()

        # 字体
        self.font = pygame.font.SysFont(None, 48)
        self.button_font = pygame.font.SysFont(None, 36)

        # 按钮（用 Rect 管理）
        self.start_button = pygame.Rect(250, 300, 200, 50)
        self.quit_button = pygame.Rect(250, 370, 200, 50)

    def handle_event(self, screen, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.start_button.collidepoint(event.pos):
                self.swift(2)  # 暂时跳转到 BattleScreen（你可以改成 StageSelectScreen）
            elif self.quit_button.collidepoint(event.pos):
                pygame.quit()
                sys.exit()

    def draw(self, screen):
        screen.blit(self.background, (0, 0))

        # Logo 居中上方
        # logo_rect = self.logo.get_rect(center=(screen.get_width() // 2, 120))
        # screen.blit(self.logo, logo_rect)

        # Start 按钮
        pygame.draw.rect(screen, (70, 130, 180), self.start_button)
        start_text = self.button_font.render("Start", True, (255, 255, 255))
        screen.blit(start_text, start_text.get_rect(center=self.start_button.center))

        # Quit 按钮
        pygame.draw.rect(screen, (180, 70, 70), self.quit_button)
        quit_text = self.button_font.render("Quit", True, (255, 255, 255))
        screen.blit(quit_text, quit_text.get_rect(center=self.quit_button.center))
