from UI.screens.screen import Screen
from battle.battle_manager import BattleManager

class BattleScreen(Screen):
    def __init__(self, manager):
        super().__init__(manager)
        self.screen_id = 1
        self.battle = BattleManager()

    def update(self):
        self.battle.update()

    def draw(self, screen):
        self.battle.draw(screen)

    def on_exit(self):
        self.battle = None