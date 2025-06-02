import pygame
from battle.AI.base_ai import BaseAI

TILE_SIZE = 64
FPS = 60


class NormalAI(BaseAI):
    def __init__(self, entity, timer, path):
        super().__init__(entity, timer)
        self.path = list(path)
        self.score = False
        self.position = pygame.Vector2(
            self.path[0][0] * TILE_SIZE,
            self.path[0][1] * TILE_SIZE
        )
        self.speed_grid_per_sec = entity.speed
        self.speed_pixel_per_frame = self.speed_grid_per_sec * TILE_SIZE / FPS

    def check_blocked(self, units):
        for unit in units:
            enemy_tile = unit.grid_pos
            target_pos = pygame.Vector2(
                enemy_tile[0] * TILE_SIZE,
                enemy_tile[1] * TILE_SIZE
            )
            delta = target_pos - self.position
            distance = delta.length()
            if distance < 20:
                self.blocked = True
                self.blocker.append(unit)
                unit.blocker.append(self)
                unit.blocked = True

    def move(self):
        if not self.path:
            self.score = True
            return
        target_tile = self.path[0]
        target_pos = pygame.Vector2(
            target_tile[0] * TILE_SIZE,
            target_tile[1] * TILE_SIZE
        )

        delta = target_pos - self.position
        distance = delta.length()

        if distance < 1:
            self.path.pop(0)
            return

        move = pygame.Vector2(0, 0)
        if abs(delta.x) > abs(delta.y):
            move.x = self.speed_pixel_per_frame if delta.x > 0 else -self.speed_pixel_per_frame
        else:
            move.y = self.speed_pixel_per_frame if delta.y > 0 else -self.speed_pixel_per_frame

        if move.length() > distance:
            move = delta

        if move.length() > distance:
            move = delta

        self.position += move

    def update(self, units):
        self.check_blocked(units)
        super().update(units)
        if not self.blocked:
            self.move()
