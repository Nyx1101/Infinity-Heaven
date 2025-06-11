from UI.screens.screen import Screen
from battle.battle_manager import BattleManager
import utility.data


class BattleScreen(Screen):
    def __init__(self, manager, info):
        super().__init__(manager)
        self.screen_id = 1
        self.items = {
            "hp": info["items"]["HP"],
            "attack": info["items"]["Attack"],
            "defense": info["items"]["Defense"]
        }
        self.formation = []
        for data in info["formation"]:
            self.formation.append({"id": data + 100, "skill_id": utility.data.SKILL_SELECTED[data]})
        self.battle = BattleManager(utility.data.CURRENT_STAGE, self.items, self.formation, self.on_battle_end)

    def on_battle_end(self, result):
        if result == "win":
            self.swift(7, {"stage": utility.data.CURRENT_STAGE, "progress": "end"})
        elif result == "lose":
            self.swift(6, "lose")

    def handle_event(self, screen, event):
        self.battle.handle_event(screen, event)

    def update(self):
        self.battle.update()

    def draw(self, screen):
        self.battle.draw(screen)

    def on_exit(self):
        self.battle = None
