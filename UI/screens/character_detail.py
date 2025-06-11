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

        self.skill_border = pygame.image.load("assets/image/border.png").convert_alpha()
        self.skill_border = pygame.transform.scale(self.skill_border, (56, 56))

        # 返回按钮
        self.back_text = self.font.render("← Back", True, (255, 255, 255))
        self.back_rect = self.back_text.get_rect(topleft=(10, 10))

        # 左右箭头
        self.left_arrow = self.big_font.render("<", True, (255, 255, 255))
        self.right_arrow = self.big_font.render(">", True, (255, 255, 255))
        self.left_rect = self.left_arrow.get_rect(center=(30, 256))
        self.right_rect = self.right_arrow.get_rect(center=(674, 256))

        # 精英化按钮
        self.elite_button_rect = pygame.Rect(250, 430, 200, 30)

        # 背景
        bg_raw = pygame.image.load("assets/image/background3.png").convert()
        self.background = pygame.transform.scale(bg_raw, (704, 512))

    def set_data(self, char_id):
        self.char_id = char_id
        self.char_name = CHARACTER_NAMES[char_id]
        self.char_data = getattr(data, self.char_name)
        self.elite_level = data.ELITE_PROGRESS[char_id]

        # 立绘
        img = pygame.image.load(self.char_data["sprite_image"]).convert_alpha()
        self.portrait = pygame.transform.scale(img, (180, 240))
        self.portrait_rect = self.portrait.get_rect(topleft=(60, 100))

        # 技能
        self.skill_ids = [char_id * 2 + 1, char_id * 2 + 2]
        self.skills = [SkillFactory.get_behavior(sid) for sid in self.skill_ids]

        # 技能图标
        self.skill_icons = []
        for i, sid in enumerate(self.skill_ids):
            icon = pygame.image.load(f"assets/image/skill{sid}.png").convert_alpha()
            icon = pygame.transform.scale(icon, (48, 48))
            rect = icon.get_rect()
            rect.center = (340 + i * 180, 350)
            self.skill_icons.append((icon, rect))

    def is_unlocked(self, char_id):
        if char_id < 3:
            return True
        return data.LEVEL_PROGRESS[char_id - 3] > 0

    def wrap_text(self, text, max_width):
        words = text.split()
        lines = []
        current_line = ""
        for word in words:
            test_line = current_line + word + " "
            test_surface = self.font.render(test_line, True, (0, 0, 0))
            if test_surface.get_width() <= max_width:
                current_line = test_line
            else:
                lines.append(current_line.strip())
                current_line = word + " "
        if current_line:
            lines.append(current_line.strip())
        return lines

    def handle_event(self, screen, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos

            # 返回
            if self.back_rect.collidepoint(pos):
                self.swift()
                return

            for i, (icon, rect) in enumerate(self.skill_icons):
                display_rect = rect.move(0, -120)
                if display_rect.collidepoint(pos):
                    if self.elite_level >= (i + 1):  # 技能是否已解锁
                        data.SKILL_SELECTED[self.char_id] = i + 1  # 设置为1或2
                        self.set_data(self.char_id)
                        return

            if self.left_rect.collidepoint(pos):
                prev_id = self.char_id - 1
                while prev_id >= 0:
                    if self.is_unlocked(prev_id):
                        self.set_data(prev_id)
                        break
                    prev_id -= 1
                return

            if self.right_rect.collidepoint(pos):
                next_id = self.char_id + 1
                while next_id <= 8:
                    if self.is_unlocked(next_id):
                        self.set_data(next_id)
                        break
                    next_id += 1
                return

            # 精英化按钮
            if self.elite_button_rect.collidepoint(pos) and self.elite_level < 2:
                badge_type = self.elite_level  # 0 -> badge[0], 1 -> badge[1]
                if data.ELITE_BADGE[badge_type] > 0:
                    # 消耗道具
                    data.ELITE_BADGE[badge_type] -= 1
                    data.ELITE_PROGRESS[self.char_id] += 1
                    data.SKILL_SELECTED[self.char_id] = data.ELITE_PROGRESS[self.char_id]
                    self.set_data(self.char_id)

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        screen.blit(self.back_text, self.back_rect)
        screen.blit(self.left_arrow, self.left_rect)
        screen.blit(self.right_arrow, self.right_rect)
        screen.blit(self.portrait, self.portrait_rect)

        # 基本信息（每行两个）
        d = self.char_data
        info_lines = [
            f"HP: {d['hp']}", f"ATK: {d['atk']}",
            f"DEF: {d['defense']}", f"RES: {d['resistance']}",
            f"Range: {'Close Combat' if d['range'] == 0 else d['range']}",
            f"ATK Type: {ATK_TYPE_MAP[d['atk_type']]}",
            f"ATK Speed: {'Not To Attack' if d['attack_speed'] == 3600 else d['attack_speed']}",
            f"Redeployment Time: {d['redeployment_time']}s"
        ]
        for i in range(0, len(info_lines), 2):
            text1 = self.font.render(info_lines[i], True, (255, 255, 255))
            screen.blit(text1, (280, 60 + (i // 2) * 30))
            if i + 1 < len(info_lines):
                text2 = self.font.render(info_lines[i + 1], True, (255, 255, 255))
                screen.blit(text2, (460, 60 + (i // 2) * 30))

        selected_skill = data.SKILL_SELECTED[self.char_id]

        for i, (icon, rect) in enumerate(self.skill_icons):
            # 上移技能区域
            new_rect = rect.move(0, -120)
            center = new_rect.center
            active = self.elite_level >= (i + 1)
            is_selected = selected_skill == (i + 1) and active

            # 绘制边框
            border_rect = pygame.Rect(0, 0, 56, 56)
            border_rect.center = center
            screen.blit(self.skill_border, border_rect)

            # 如果是选中技能，画黄框
            if is_selected:
                pygame.draw.rect(screen, (255, 255, 0), border_rect.inflate(4, 4), width=3)

            # 技能图标（透明度）
            icon_copy = icon.copy()
            if not active:
                icon_copy.set_alpha(100)
            icon_rect = icon_copy.get_rect(center=center)
            screen.blit(icon_copy, icon_rect)

            # 技能名
            if self.skills[i]:
                name, desc = self.skills[i].description
                name_text = self.font.render(name, True, (255, 255, 0))
                name_rect = name_text.get_rect(center=(center[0], icon_rect.bottom + 20))
                screen.blit(name_text, name_rect)

                # 技能描述
                wrapped_lines = self.wrap_text(desc, 180)
                for j, line in enumerate(wrapped_lines):
                    line_surf = self.font.render(line, True, (255, 255, 255))
                    line_rect = line_surf.get_rect(center=(center[0], name_rect.bottom + 10 + j * 24))
                    screen.blit(line_surf, line_rect)

        # 精英按钮显示
        btn_text = f"Upgrade to Elite {self.elite_level + 1}" if self.elite_level < 2 else "Max Elite"
        badge_count = data.ELITE_BADGE[self.elite_level] if self.elite_level < 2 else 0
        color = (180, 180, 180) if badge_count == 0 or self.elite_level >= 2 else (50, 200, 100)

        pygame.draw.rect(screen, color, self.elite_button_rect)
        txt = self.font.render(btn_text, True, (0, 0, 0))
        screen.blit(txt, self.elite_button_rect.move(10, 5))
        if self.elite_level < 2:
            badge_text = self.font.render(f"Available Elite Badge{self.elite_level + 1}: {badge_count}", True,
                                          (255, 255, 255))
            screen.blit(badge_text, (self.elite_button_rect.x, self.elite_button_rect.y + 35))
