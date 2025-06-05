import pygame
from UI.screens.screen import Screen
import utility.data


class CharacterListScreen(Screen):
    def __init__(self, manager, info=None):
        super().__init__(manager)
        self.screen_id = 3
        if info is not None:
            self.mode = "Select"
            self.selected = []

        # 背景图加载并缩放
        raw_bg = pygame.image.load("assets/image/img_2.png").convert()
        self.background = pygame.transform.scale(raw_bg, (704, 512))

        # 返回按钮
        font = pygame.font.SysFont("arial", 24)
        self.back_text = font.render("← Back", True, (255, 255, 255))
        self.back_rect = self.back_text.get_rect(topleft=(10, 10))

        # 获取已解锁角色信息
        level_progress = utility.data.LEVEL_PROGRESS  # 假设长度为7
        self.unlocked = [True] * 3 + [lv > 0 for lv in level_progress[:6]]  # 前3个角色默认解锁

        # 创建角色图标按钮（3x3矩阵）
        self.char_buttons = []
        for i in range(9):
            img = pygame.image.load(f"assets/image/character{i+1}.png").convert_alpha()
            icon = pygame.transform.smoothscale(img, (96, 96))
            rect = icon.get_rect()

            row = i // 3
            col = i % 3
            rect.topleft = (70 + col * 180, 80 + row * 130)

            # 是否激活（可点击）
            active = self.unlocked[i] if i < len(self.unlocked) else False

            self.char_buttons.append({
                "index": i,
                "icon": icon,
                "rect": rect,
                "active": active
            })
        # 确定按钮（右下角）
        self.confirm_font = pygame.font.SysFont("arial", 22)
        self.confirm_text = self.confirm_font.render("Confirm", True, (255, 255, 255))
        self.confirm_rect = pygame.Rect(550, 440, 120, 40)

    def handle_event(self, screen, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            # 返回按钮点击
            if self.back_rect.collidepoint(mouse_pos):
                print("back")
                self.swift()  # 无参调用会回到上一 screen
                return

            # 确认按钮点击
            if hasattr(self, "selected") and self.confirm_rect.collidepoint(mouse_pos):
                if self.info["limit"]:
                    if len(self.selected) <= 6:
                        self.info.update({"formation": self.selected})
                        self.swift(1, data=self.info)
                    else:
                        # 写人数过多提示
                        return
                self.info.update({"formation": self.selected})
                self.swift(1, data=self.selected)
                return

            for button in self.char_buttons:
                if button["active"] and button["rect"].collidepoint(mouse_pos):
                    if hasattr(self, "mode"):
                        if button["index"] in self.selected:
                            self.selected.remove(button["index"])
                        else:
                            self.selected.append(button["index"])
                    self.swift(5, data=button["index"])  # 跳转角色详情界面并传递角色编号
                    return

    def draw(self, screen):
        screen.blit(self.background, (0, 0))

        screen.blit(self.back_text, self.back_rect)

        for button in self.char_buttons:
            icon = button["icon"].copy()
            rect = button["rect"]

            if not button["active"]:
                # 若未解锁，则设置为半透明
                icon.set_alpha(80)

            screen.blit(icon, rect)
            if button["index"] in getattr(self, "selected", []):
                pygame.draw.rect(screen, (255, 255, 0), rect.inflate(4, 4), width=3)

        # 仅在 Select 模式下显示确认按钮
        if hasattr(self, "selected"):
            pygame.draw.rect(screen, (50, 180, 100), self.confirm_rect, border_radius=6)
            text_rect = self.confirm_text.get_rect(center=self.confirm_rect.center)
            screen.blit(self.confirm_text, text_rect)
