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
        self.current = None
        self.history = []
        self.audio = audio
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
        self.quit = False

        self.switch_to(0)

    def switch_to(self, id=None, data=None):
        if self.current:
            if hasattr(self.current, "on_exit"):
                self.current.on_exit()
            if hasattr(self.current, "screen_id"):
                self.history.append(self.current.screen_id)

        if id is None:
            if not self.history:
                return
            self.history.pop()
            id = self.history.pop()

        if id == 1:
            self.audio.play_music("battle_bgm.mp3")
        elif self.current is None or self.current.screen_id == 1:
            self.audio.play_music("menu_bgm.mp3")

        if id in self.id_map:
            self.current = self.id_map[id](data)
        else:
            print(f"[Error] Invalid screen id: {id}, data: {data}")

    def handle_event(self, screen, event):
        if self.current:
            self.current.handle_event(screen, event)

    def update(self):
        if self.current:
            self.current.update()

    def draw(self, screen):
        if self.current:
            self.current.draw(screen)
