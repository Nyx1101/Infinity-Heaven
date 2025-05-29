import time
from battle.level.level_loader import LevelLoader
from battle.AI.normal_ai import NormalAI
from entities.enemy import EnemyFactory
import pygame

class BattleManager:
    def __init__(self):
        self.loader = LevelLoader()
        self.map = self.loader.load_level_1_map()
        self.level_flow = self.loader.load_level_1_enemy()
        self.enemy_factory = EnemyFactory()
        self.AIs = []
        self.start_time = time.time()

    def update(self):
        current_time = time.time()-self.start_time
        result = self.level_flow.pop_next_if_due(current_time)

        if result:
            new_enemy = self.enemy_factory.create_enemy_by_id(result["id"])
            ai = NormalAI(new_enemy, result["path"])
            self.AIs.append(ai)

        for AI in self.AIs:
            AI.update()

    def draw(self, screen):
        self.map.draw(screen)
        for AI in self.AIs:
            AI.draw(screen)





