import pygame
from pathlib import Path
from UI.screen_manager import ScreenManager
from audio.audio_manager import AudioManager
from utility.file_utils import save_dict_to_file, load_dict_from_file
import utility.data


# Load game progress data from file into global variables
def init_progress():
    data = load_dict_from_file("config/game_progress.json")
    utility.data.ELITE_PROGRESS = data["ELITE_PROGRESS"]
    utility.data.LEVEL_PROGRESS = data["LEVEL_PROGRESS"]
    utility.data.ELITE_BADGE = data["ELITE_BADGE"]
    utility.data.STORY_PROGRESS = data["STORY_PROGRESS"]
    utility.data.SKILL_SELECTED = data["SKILL_SELECTED"]


# Save current game progress data to file
def save_progress():
    data = {
        "ELITE_PROGRESS": utility.data.ELITE_PROGRESS,
        "LEVEL_PROGRESS": utility.data.LEVEL_PROGRESS,
        "ELITE_BADGE": utility.data.ELITE_BADGE,
        "STORY_PROGRESS": utility.data.STORY_PROGRESS,
        "SKILL_SELECTED": utility.data.SKILL_SELECTED
    }
    save_dict_to_file(data, "config/game_progress.json")


# Initialize game progress from file
init_progress()

# Initialize Pygame
pygame.init()

# Set game window size and title
screen = pygame.display.set_mode((704, 512))
pygame.display.set_caption("Infinity Heaven")

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Initialize audio manager and screen manager
audio_manager = AudioManager(Path("assets/audio"))
screen_manager = ScreenManager(audio_manager)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        # Quit the game if window is closed
        if event.type == pygame.QUIT:
            running = False
        # Handle user input events through screen manager
        screen_manager.handle_event(screen, event)
        # Allow the screen manager to signal a quit
        if screen_manager.quit:
            running = False

    # Update game state
    screen_manager.update()

    # Draw everything on the screen
    screen_manager.draw(screen)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate at 60 FPS
    clock.tick(60)

# Clean up and save progress on exit
pygame.quit()
save_progress()