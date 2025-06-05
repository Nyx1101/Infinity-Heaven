import pygame
from UI.screens.screen import Screen
from assets.story.story_data import STORY
import utility.data as data

CHARACTER_NAMES = [
    "WARRIOR", "ARCHER", "HEALER", "MAGE", "TANK_PHYSICAL",
    "ASSASSIN", "CONTROLLER", "TANK_MAGIC", "SUPPORTER"
]


class StoryScreen(Screen):
    def __init__(self, manager, info=None):
        super().__init__(manager, info)
        self.font = pygame.font.SysFont("arial", 20)
        self.stage = info["stage"]
        self.progress_type = info["progress"]  # "start" or "end"
        self.story_lines = STORY[self.stage][self.progress_type]
        self.index = 0  # 当前句编号

        self.background = pygame.image.load("assets/image/background.png").convert()
        self.dialogue_box = pygame.Surface((680, 140))
        self.dialogue_box.fill((0, 0, 0))
        self.dialogue_box.set_alpha(180)

        self.update_current_line()

    def update_current_line(self):
        if self.index < len(self.story_lines):
            line = self.story_lines[self.index]
            char_id = line["character"]
            self.char_data = getattr(data, CHARACTER_NAMES[char_id])
            self.char_name = CHARACTER_NAMES[char_id]
            self.sentence = line["sentence"]

            # 加载立绘
            image = pygame.image.load(self.char_data["sprite_image"]).convert_alpha()
            self.portrait = pygame.transform.scale(image, (180, 240))
        else:
            # 剧情结束，修改 STORY_PROGRESS 并跳转
            if self.progress_type == "start":
                data.STORY_PROGRESS[self.stage - 1] = 1
            elif self.progress_type == "end":
                data.STORY_PROGRESS[self.stage - 1] = 2
            self.swift(2)  # 返回关卡选择界面

    def handle_event(self, screen, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.index += 1
            self.update_current_line()

    def draw(self, screen):
        screen.blit(self.background, (0, 0))

        if self.index >= len(self.story_lines):
            return

        # 左侧立绘
        screen.blit(self.portrait, (30, 100))

        # 对话框
        screen.blit(self.dialogue_box, (12, 360))
        name_text = self.font.render(f"{self.char_name}", True, (255, 255, 255))
        sentence_text = self.font.render(self.sentence, True, (255, 255, 255))
        screen.blit(name_text, (30, 370))
        screen.blit(sentence_text, (30, 400))
