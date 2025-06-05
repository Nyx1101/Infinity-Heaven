import pygame
from UI.screens.screen import Screen
import utility.data as data
from entities.skill import SkillFactory

# 角色编号到名称的映射
CHARACTER_NAMES = [
    "WARRIOR", "ARCHER", "HEALER", "MAGE", "TANK_PHYSICAL",
    "ASSASSIN", "CONTROLLER", "TANK_MAGIC", "SUPPORTER"
]

# 攻击类型映射
ATK_TYPE_MAP = {0: "physical", 1: "magic", 2: "heal"}


class CharacterDetailScreen(Screen):
    def __init__(self, manager, info=None):
        super().__init__(manager, info)
        self.screen_id = 5
        self.font = pygame.font.SysFont("arial", 20)
        self.big_font = pygame.font.SysFont("arial", 24)
        self.char_id = None
        self.set_data(self.info)

        # 返回按钮
        self.back_text = self.font.render("← Back", True, (255, 255, 255))
        self.back_rect = self.back_text.get_rect(topleft=(10, 10))

        # 左右箭头
        self.left_arrow = self.big_font.render("<", True, (255, 255, 255))
        self.right_arrow = self.big_font.render(">", True, (255, 255, 255))
        self.left_rect = self.left_arrow.get_rect(center=(30, 256))
        self.right_rect = self.right_arrow.get_rect(center=(674, 256))

        # 精英化按钮
        self.elite_button_rect = pygame.Rect(250, 460, 200, 30)

        # 背景
        bg_raw = pygame.image.load("assets/image/background.png").convert()
        self.background = pygame.transform.scale(bg_raw, (704, 512))

    def set_data(self, char_id):
        self.char_id = char_id
        self.char_name = CHARACTER_NAMES[char_id]
        self.char_data = getattr(data, self.char_name)
        self.elite_level = data.ELITE_PROGRESS[char_id]

        # 立绘
        img = pygame.image.load(self.char_data["sprite_image"]).convert_alpha()
        self.portrait = pygame.transform.scale(img, (180, 240))
        self.portrait_rect = self.portrait.get_rect(topleft=(80, 100))

        # 技能
        self.skill_ids = [char_id * 2 + 1, char_id * 2 + 2]
        self.skills = [SkillFactory.get_behavior(sid) for sid in self.skill_ids]

        # 技能图标
        self.skill_icons = []
        for i, sid in enumerate(self.skill_ids):
            icon = pygame.image.load(f"assets/image/skill{sid}.png").convert_alpha()
            icon = pygame.transform.scale(icon, (48, 48))
            rect = icon.get_rect()
            rect.center = (400 + i * 120, 350)
            self.skill_icons.append((icon, rect))

    def handle_event(self, screen, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos

            # 返回
            if self.back_rect.collidepoint(pos):
                self.swift()
                return

            for i, (icon, rect) in enumerate(self.skill_icons):
                if rect.collidepoint(pos):
                    if self.elite_level >= (i + 1):  # 技能是否已解锁
                        data.SKILL_SELECTED[self.char_id] = i + 1  # 设置为1或2
                        return

            # 左右切换
            if self.left_rect.collidepoint(pos) and self.char_id > 0:
                self.set_data(self.char_id - 1)
                return
            if self.right_rect.collidepoint(pos) and self.char_id < 8:
                self.set_data(self.char_id + 1)
                return

            # 精英化按钮
            if self.elite_button_rect.collidepoint(pos) and self.elite_level < 2:
                badge_type = self.elite_level  # 0 -> badge[0], 1 -> badge[1]
                if data.ELITE_BADGE[badge_type] > 0:
                    # 消耗道具
                    data.ELITE_BADGE[badge_type] -= 1
                    data.ELITE_PROGRESS[self.char_id] += 1
                    self.set_data(self.char_id)

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        screen.blit(self.back_text, self.back_rect)
        screen.blit(self.left_arrow, self.left_rect)
        screen.blit(self.right_arrow, self.right_rect)
        screen.blit(self.portrait, self.portrait_rect)

        # 基本信息
        d = self.char_data
        info_lines = [
            f"HP: {d['hp']}",
            f"ATK: {d['atk']}",
            f"DEF: {d['defense']}",
            f"RES: {d['resistance']}",
            f"Range: {'Close Combat' if d['range'] == 0 else d['range']}",
            f"ATK Type: {ATK_TYPE_MAP[d['atk_type']]}",
            f"ATK Speed: {d['attack_speed']}",
            f"Redeployment_Time: {d['redeployment_time']}s"
        ]
        for i, line in enumerate(info_lines):
            text = self.font.render(line, True, (255, 255, 255))
            screen.blit(text, (320, 60 + i * 25))

        # 技能图标 + 描述
        selected_skill = data.SKILL_SELECTED[self.char_id]
        for i, (icon, rect) in enumerate(self.skill_icons):
            active = self.elite_level >= (i + 1)
            icon_copy = icon.copy()
            if not active:
                icon_copy.set_alpha(100)
            screen.blit(icon_copy, rect)
            # 高亮技能（只高亮解锁且已被选中的技能）
            if selected_skill == i + 1 and active:
                pygame.draw.rect(screen, (255, 215, 0), rect.inflate(6, 6), 3)

            if self.skills[i]:
                name, desc = self.skills[i].description
                name_text = self.font.render(name, True, (255, 255, 255))
                desc_text = self.font.render(desc, True, (255, 255, 255))
                screen.blit(name_text, (rect.x, rect.y + 55))
                screen.blit(desc_text, (rect.x - 40, rect.y + 75))

        # 精英按钮显示
        btn_text = f"Upgrade to Elite {self.elite_level + 1}" if self.elite_level < 2 else "Max Elite"
        badge_count = data.ELITE_BADGE[self.elite_level] if self.elite_level < 2 else 0
        color = (180, 180, 180) if badge_count == 0 or self.elite_level >= 2 else (50, 200, 100)

        pygame.draw.rect(screen, color, self.elite_button_rect)
        txt = self.font.render(btn_text, True, (0, 0, 0))
        screen.blit(txt, self.elite_button_rect.move(10, 5))

        # 拥有道具显示
        badge_text = self.font.render(f"Available Elite Badge {self.elite_level + 1}：{badge_count}", True, (255, 255, 255))
        screen.blit(badge_text, (self.elite_button_rect.x, self.elite_button_rect.y + 35))
