from UI.screens.main_menu import MainMenuScreen
from UI.screens.battle import BattleScreen

class ScreenManager:
    def __init__(self):
        self.current = None
        self.history = []

        self.id_map = {
            0: lambda: MainMenuScreen(self),
            1: lambda: BattleScreen(self),
        }

        self.switch_to(0)

    def switch_to(self, id=None):
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
        else:
            print(f"[Error] Invalid screen id: {id}")

    def handle_event(self, event):
        if self.current:
            self.current.handle_event(event)

    def update(self):
        if self.current:
            self.current.update()

    def draw(self, screen):
        if self.current:
            self.current.draw(screen)

    def handle_events(self, events):
        if self.current_screen:
            self.current_screen.handle_events(events)