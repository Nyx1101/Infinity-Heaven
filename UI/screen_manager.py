from UI.screens.main_menu import MainMenuScreen
from UI.screens.stage_select import StageSelectScreen
from UI.screens.battle import BattleScreen
# from UI.screens.character_list import


class ScreenManager:
    def __init__(self):
        self.current = None
        self.history = []

        self.id_map = {
            0: lambda: MainMenuScreen(self),
            1: lambda: BattleScreen(self),
            2: lambda: StageSelectScreen(self),
            # 3: lambda: CharacterScreen(self),
            # 4: lambda: DifficultySelectScreen(self)
        }

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
            id = self.history.pop()

        if id in self.id_map:
            self.current = self.id_map[id]()
            if data is not None:
                self.current.data = data
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
