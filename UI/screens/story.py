import pygame
from UI.screens.screen import Screen
from assets.story.story_data import STORY
import utility.data as data

# Mapping character ID to name constants
CHARACTER_NAMES = {
    0: "WARRIOR",
    1: "ARCHER",
    2: "HEALER",
    3: "MAGE",
    4: "TANK_PHYSICAL",
    5: "ASSASSIN",
    6: "CONTROLLER",
    7: "TANK_MAGIC",
    8: "SUPPORTER"
}


class StoryScreen(Screen):
    def __init__(self, manager, info=None):
        super().__init__(manager, info)
        self.screen_id = 7
        self.font = pygame.font.SysFont("arial", 20)

        self.stage = info["stage"]
        self.progress_type = info["progress"]  # "start" or "end"
        self.story_lines = STORY[self.stage][self.progress_type]
        self.index = 0

        # Load and scale background and dialogue box
        raw_background = pygame.image.load("assets/image/background4.png").convert()
        self.background = pygame.transform.scale(raw_background, (704, 512))
        self.dialogue_box = pygame.Surface((680, 140))
        self.dialogue_box.fill((0, 0, 0))
        self.dialogue_box.set_alpha(180)

        self.update_current_line()

    def wrap_text(self, text, font, max_width):
        # Split long text into lines based on width
        words = text.split(" ")
        lines = []
        current_line = ""

        for word in words:
            test_line = current_line + word + " "
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line.strip())
                current_line = word + " "
        if current_line:
            lines.append(current_line.strip())

        return lines

    def update_current_line(self):
        # Update current line and portrait
        if self.index < len(self.story_lines):
            line = self.story_lines[self.index]
            char_id = line["character"]
            self.sentence = line["sentence"]
            self.char_id = char_id

            if char_id == 9:  # Narration
                self.char_data = None
                self.portrait = None
            else:
                self.char_data = getattr(data, CHARACTER_NAMES[char_id])
                image = pygame.image.load(self.char_data["sprite_image"]).convert_alpha()
                self.portrait = pygame.transform.scale(image, (180, 240))
        else:
            # When finished, update story progress and switch screen
            if self.progress_type == "start":
                data.STORY_PROGRESS[self.stage] = 1
                if self.stage == 0:
                    self.swift(2)
                else:
                    self.swift(1, self.info)
            elif self.progress_type == "end":
                data.STORY_PROGRESS[self.stage] = 2
                self.swift(6, "win")

    def handle_event(self, screen, event):
        # Advance story on mouse click
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.index += 1
            self.update_current_line()

    def draw(self, screen):
        screen.blit(self.background, (0, 0))

        if self.index >= len(self.story_lines):
            return

        # Draw character portrait if not narration
        if self.char_id != 9 and self.portrait:
            screen.blit(self.portrait, (30, 100))

        screen.blit(self.dialogue_box, (12, 360))

        # Draw character name
        if self.char_id != 9:
            name_text = self.font.render(f"{CHARACTER_NAMES[self.char_id]}", True, (255, 255, 255))
            screen.blit(name_text, (30, 370))

        # Render wrapped dialogue text
        wrapped_lines = self.wrap_text(self.sentence, self.font, 640)
        for i, line in enumerate(wrapped_lines):
            text_surface = self.font.render(line, True, (255, 255, 255))
            screen.blit(text_surface, (30, 400 + i * 25))