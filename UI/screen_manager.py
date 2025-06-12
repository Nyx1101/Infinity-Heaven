import utility.data
from UI.screens.main_menu import MainMenuScreen
from UI.screens.stage_select import StageSelectScreen
from UI.screens.battle import BattleScreen
from UI.screens.character_list import CharacterListScreen
from UI.screens.character_detail import CharacterDetailScreen
from UI.screens.story import StoryScreen
from UI.screens.difficulty_select import DifficultyScreen
from UI.screens.settlement import SettlementScreen


class ScreenManager:
    def __init__(self, audio):
        """
        Initialize the ScreenManager.

        Parameters:
            audio: An instance of AudioManager used for playing background music.

        This manager handles screen switching, navigation history,
        and delegates event handling, updating, and drawing to the current screen.
        """
        self.current = None           # The currently active screen
        self.history = []             # Stack to track screen navigation history
        self.audio = audio            # Audio manager for BGM control
        self.quit = False             # Flag to indicate application should quit

        # Mapping screen IDs to screen constructor functions
        self.id_map = {
            0: lambda data=None: MainMenuScreen(self, data),
            1: lambda data=None: BattleScreen(self, data),
            2: lambda data=None: StageSelectScreen(self, data),
            3: lambda data=None: CharacterListScreen(self, data),
            4: lambda data=None: DifficultyScreen(self, data),
            5: lambda data=None: CharacterDetailScreen(self, data),
            6: lambda data=None: SettlementScreen(self, data),
            7: lambda data=None: StoryScreen(self, data)
        }

        # Start with the main menu screen
        self.switch_to(0)

    def switch_to(self, id=None, data=None):
        """
        Switch to a new screen by ID.

        Parameters:
            id (int or None): The ID of the target screen. If None, go back in history.
            data (optional): Optional data to pass to the new screen.

        Handles music switching and screen exit logic.
        """
        # Handle exiting current screen
        if self.current:
            if hasattr(self.current, "on_exit"):
                self.current.on_exit()
            if hasattr(self.current, "screen_id"):
                self.history.append(self.current.screen_id)

        # If no ID is given, pop from history to go back
        if id is None:
            if not self.history:
                return
            self.history.pop()  # Discard current
            id = self.history.pop()  # Go back to previous

        # Handle background music switching
        if id == 1:
            if utility.data.CURRENT_STAGE == 7:
                self.audio.play_music("boss_bgm.mp3")
            else:
                self.audio.play_music("battle_bgm.mp3")
        elif self.current is None or self.current.screen_id == 1:
            self.audio.play_music("menu_bgm.mp3")

        # Create and switch to new screen
        if id in self.id_map:
            self.current = self.id_map[id](data)
        else:
            print(f"[Error] Invalid screen id: {id}, data: {data}")

    def handle_event(self, screen, event):
        """
        Forward the event to the current screen for handling.

        Parameters:
            screen: The Pygame screen surface.
            event: The Pygame event to handle.
        """
        if self.current:
            self.current.handle_event(screen, event)

    def update(self):
        """
        Call the update method of the current screen.
        """
        if self.current:
            self.current.update()

    def draw(self, screen):
        """
        Call the draw method of the current screen.

        Parameters:
            screen: The Pygame screen surface to draw on.
        """
        if self.current:
            self.current.draw(screen)