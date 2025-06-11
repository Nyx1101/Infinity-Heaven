import pygame
from UI.screens.screen import Screen
import utility.data


class StageSelectScreen(Screen):
    def __init__(self, manager, info=None):
        super().__init__(manager)
        self.screen_id = 2
        # 标题文字
        self.title_text = pygame.font.SysFont("arial", 32, bold=True).render("Select Stage", True, (255, 255, 255))
        self.title_text_rect = self.title_text.get_rect(center=(352, 50))  # 居中于上方
        # 背景
        raw_bg = pygame.image.load("assets/image/background.png").convert()
        self.background = pygame.transform.scale(raw_bg, (704, 512))

        font = pygame.font.SysFont("arial", 24)
        self.back_text = font.render("← Back", True, (255, 255, 255))
        self.back_rect = self.back_text.get_rect(topleft=(10, 10))

        # characters 图标（右上角）
        raw_icon = pygame.image.load("assets/image/CharacterIcon.png").convert_alpha()
        self.char_icon = pygame.transform.smoothscale(raw_icon, (64, 64))
        self.char_icon_rect = self.char_icon.get_rect(topright=(690, 10))  # 右上角位置

        self.font = pygame.font.SysFont("arial", 20)

        # 找到第一个未通关关卡索引
        try:
            self.first_locked_index = utility.data.LEVEL_PROGRESS.index(0)
        except ValueError:
            self.first_locked_index = len(utility.data.LEVEL_PROGRESS)  # 全部通关

        # 构建关卡图标和文字
        self.stage_data = []
        for i in range(7):
            img = pygame.image.load(f"assets/image/stage.png").convert_alpha()
            icon = pygame.transform.smoothscale(img, (64, 64))
            rect = icon.get_rect()
            rect.center = (130 + i * 75, 250)

            # 编号文字
            label = self.font.render(str(i + 1), True, (255, 255, 255))
            label_rect = label.get_rect(center=(rect.centerx, rect.centery - 50))

            # 解锁状态
            unlocked = i <= self.first_locked_index
            if not unlocked:
                icon.set_alpha(100)

            # 星级图片（根据 LEVEL_PROGRESS）
            star_image = None
            star_rect = None
            progress = utility.data.LEVEL_PROGRESS[i] if i < len(utility.data.LEVEL_PROGRESS) else 0
            if progress in [1, 2, 3]:
                star_image = pygame.image.load(f"assets/image/star_{progress}.png").convert_alpha()
                star_image = pygame.transform.smoothscale(star_image, (50, 20))  # 可根据需要调整大小
                star_rect = star_image.get_rect(center=(rect.centerx, rect.bottom + 5))  # 放在图标下方

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

            # 点击返回按钮
            if self.back_rect.collidepoint(mouse_pos):
                self.swift(0)
                return

            # 点击角色图标
            if self.char_icon_rect.collidepoint(mouse_pos):
                self.swift(3)
                return

            # 点击关卡图标
            for i, data in enumerate(self.stage_data):
                if data["rect"].collidepoint(mouse_pos):
                    if not data["unlocked"]:
                        return  # 未解锁则跳过
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
