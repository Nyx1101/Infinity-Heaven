import pygame
from battle.level.level_loader import load_level_1

class BattleManager:
    def __init__(self):
        self.map = load_level_1()

    def handle_event(self, event):
        pass

    def update(self):
        pass

    def draw(self, screen):
        self.map.draw(screen)