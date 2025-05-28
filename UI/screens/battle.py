# screens/battle.py
import pygame
from battle.battle_manager import BattleManager

class BattleScreen:
    def __init__(self, manager):
        self.manager = manager
        self.battle = BattleManager()

    def handle_event(self, event):
        self.battle.handle_event(event)

    def update(self):
        self.battle.update()

    def draw(self, screen):
        self.battle.draw(screen)