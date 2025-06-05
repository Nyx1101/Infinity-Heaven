import pygame
from UI.screens.screen import Screen


class DifficultyScreen(Screen):
    def __init__(self, manager, info=None):
        super().__init__(manager, info)
        self.screen_id = 4
        self.font = pygame.font.SysFont("arial", 20)
        self.big_font = pygame.font.SysFont("arial", 26)
        self.background = pygame.image.load("assets/image/background.png")

        # 当前选项状态
        self.hp_level = 0       # 0,1,2 对应 25%,50%,100%
        self.atk_level = 0      # 0,1,2
        self.def_level = 0      # 0,1,2
        self.limit = False

        # 按钮位置
        self.hp_buttons = self.create_buttons(80, "HP", ["25%", "50%", "100%"])
        self.atk_buttons = self.create_buttons(240, "Attack", ["10%", "20%", "30%"])
        self.def_buttons = self.create_buttons(400, "Defense", ["10%", "20%", "30%"])

        self.limit_rect = pygame.Rect(500, 100, 180, 40)
        self.select_rect = pygame.Rect(500, 350, 180, 50)

    def create_buttons(self, x, label, values):
        buttons = []
        for i, val in enumerate(values):
            rect = pygame.Rect(x, 120 + i * 60, 120, 40)
            buttons.append((rect, val))
        return buttons

    def draw_buttons(self, screen, buttons, level):
        for i, (rect, val) in enumerate(buttons):
            color = (255, 0, 0) if i <= level else (255, 255, 255)
            pygame.draw.rect(screen, (0, 0, 0), rect)
            pygame.draw.rect(screen, color, rect, 2)
            text = self.font.render(val, True, color)
            screen.blit(text, (rect.x + 30, rect.y + 10))

    def handle_event(self, screen, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()

            for i, (rect, _) in enumerate(self.hp_buttons):
                if rect.collidepoint(pos):
                    self.hp_level = i
            for i, (rect, _) in enumerate(self.atk_buttons):
                if rect.collidepoint(pos):
                    self.atk_level = i
            for i, (rect, _) in enumerate(self.def_buttons):
                if rect.collidepoint(pos):
                    self.def_level = i

            if self.limit_rect.collidepoint(pos):
                self.limit = not self.limit

            if self.select_rect.collidepoint(pos):
                result = {
                    "HP": [1.25, 1.5, 2][self.hp_level],
                    "Attack": [1.1, 1.2, 1.3][self.atk_level],
                    "Defense": [1.1, 1.2, 1.3][self.def_level],
                    "Limit": self.limit
                }
                self.swift(3, data=result)

            # 返回按钮检测
            if pygame.Rect(20, 20, 80, 40).collidepoint(pos):
                self.manager.switch_to()

    def draw(self, screen):
        screen.blit(self.background, (0, 0))

        # 返回按钮
        pygame.draw.rect(screen, (255, 255, 255), (20, 20, 80, 40), 2)
        screen.blit(self.font.render("Back", True, (255, 255, 255)), (35, 30))

        # 标题
        screen.blit(self.big_font.render("Select Difficulty", True, (255, 255, 255)), (300, 30))

        # 三列按钮
        screen.blit(self.font.render("HP", True, (255, 255, 255)), (self.hp_buttons[0][0].x + 30, 90))
        screen.blit(self.font.render("Attack", True, (255, 255, 255)), (self.atk_buttons[0][0].x + 20, 90))
        screen.blit(self.font.render("Defense", True, (255, 255, 255)), (self.def_buttons[0][0].x + 20, 90))

        self.draw_buttons(screen, self.hp_buttons, self.hp_level)
        self.draw_buttons(screen, self.atk_buttons, self.atk_level)
        self.draw_buttons(screen, self.def_buttons, self.def_level)

        # Formation 限制按钮
        pygame.draw.rect(screen, (0, 0, 0), self.limit_rect)
        border_color = (255, 0, 0) if self.limit else (255, 255, 255)
        pygame.draw.rect(screen, border_color, self.limit_rect, 2)
        screen.blit(self.font.render("Limited Formation: 6", True, border_color),
                    (self.limit_rect.x + 10, self.limit_rect.y + 10))

        # Select 按钮
        pygame.draw.rect(screen, (0, 0, 0), self.select_rect)
        pygame.draw.rect(screen, (255, 255, 255), self.select_rect, 2)
        screen.blit(self.font.render("Select Characters", True, (255, 255, 255)),
                    (self.select_rect.x + 10, self.select_rect.y + 15))
