import pygame
from battle.level.level_loader import load_level_1

# class AIManager:
#     def __init__(self):
#         self.ais = []
#
#     def register(self, ai):
#         self.ais.append(ai)
#
#     def unregister(self, ai):
#         if ai in self.ais:
#             self.ais.remove(ai)
#
#     def update_all(self):
#         for ai in self.ais:
#             ai.update()


class BattleManager:
    def __init__(self):
        self.map = load_level_1()

    def handle_event(self, event):
        pass

    def update(self):
        pass

    def draw(self, screen):
        self.map.draw(screen)