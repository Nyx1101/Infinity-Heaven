from UI.screens.screen import Screen
from battle.battle_manager import BattleManager
import utility.data

formation = [
    {"id": 100, "skill_id": 1, "artefact_id": 1},
    {"id": 101, "skill_id": 1, "artefact_id": 1}
]

items = {
    "hp": 1,
    "attack": 1,
    "defense": 1
}


class BattleScreen(Screen):
    def __init__(self, manager, info):
        super().__init__(manager)
        self.screen_id = 1
        # self.items = {
        #     "hp": info["HP"],
        #     "attack": info["Attack"],
        #     "defense": info["Defense"]
        # }
        self.battle = BattleManager(7, items, formation)

    def handle_event(self, screen, event):
        self.battle.handle_event(screen, event)

    def update(self):
        self.battle.update()

    def draw(self, screen):
        self.battle.draw(screen)

    def on_exit(self):
        self.battle = None
