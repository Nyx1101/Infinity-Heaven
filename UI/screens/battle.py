from UI.screens.screen import Screen
from battle.battle_manager import BattleManager

items = {
    "hp": 1,
    "attack": 1,
    "defense": 1
}
formation = [
    {"id": "100", "skill_id": 1, "artefact_id": 1},
    {"id": "101", "skill_id": 1, "artefact_id": 1}
]


class BattleScreen(Screen):
    def __init__(self, manager):
        super().__init__(manager)
        self.screen_id = 1
        self.battle = BattleManager(1, items, formation)

    def handle_event(self, screen, event):
        self.battle.handle_event(screen, event)

    def update(self):
        self.battle.update()

    def draw(self, screen):
        self.battle.draw(screen)

    def on_exit(self):
        self.battle = None
