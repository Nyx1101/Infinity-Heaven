import pygame
from pathlib import Path
from UI.screen_manager import ScreenManager
from audio.audio_manager import AudioManager
from utility.file_utils import save_dict_to_file, load_dict_from_file
import utility.data


def init_progress():
    data = load_dict_from_file("config/game_progress.json")
    utility.data.ELITE_PROGRESS = data["ELITE_PROGRESS"]
    utility.data.LEVEL_PROGRESS = data["LEVEL_PROGRESS"]
    utility.data.ELITE_BADGE = data["ELITE_BADGE"]
    utility.data.STORY_PROGRESS = data["STORY_PROGRESS"]
    utility.data.SKILL_SELECTED = data["SKILL_SELECTED"]


def save_progress():
    data = {
        "ELITE_PROGRESS": utility.data.ELITE_PROGRESS,
        "LEVEL_PROGRESS": utility.data.LEVEL_PROGRESS,
        "ELITE_BADGE": utility.data.ELITE_BADGE,
        "STORY_PROGRESS": utility.data.STORY_PROGRESS,
        "SKILL_SELECTED": utility.data.SKILL_SELECTED
    }
    save_dict_to_file(data, "config/game_progress.json")


init_progress()
pygame.init()
screen = pygame.display.set_mode((704, 512))
pygame.display.set_caption("Infinity Heaven")
clock = pygame.time.Clock()

audio_manager = AudioManager(Path("assets/audio"))
screen_manager = ScreenManager(audio_manager)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        screen_manager.handle_event(screen, event)
        if screen_manager.quit:
            running = False

    screen_manager.update()
    screen_manager.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
save_progress()
