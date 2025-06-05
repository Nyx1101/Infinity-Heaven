import pygame
from battle.AI.base_ai import BaseAI

TILE_SIZE = 64
FPS = 60


class NormalAI(BaseAI):
    def __init__(self, entity, timer, manager, path):
        super().__init__(entity, timer, manager)
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


class EliteAI1(NormalAI):
    def __init__(self, entity, timer, manager, path):
        super().__init__(entity, timer, manager, path)

    def update(self, units):
        if self.blocked:
            self.hp -= self.entity.hp * 0.02 / FPS


class EliteAI2(NormalAI):
    def __init__(self, entity, timer, manager, path):
        super().__init__(entity, timer, manager, path)

    def perform_attack(self, units):
        if self.timer.time() - self.last_atk > self.atk_spd:
            target = self.search_enemy(units)
            if target is not None:
                for unit in units:
                    if unit.position.distance_to(target) < 1.5 * TILE_SIZE:
                        self.normal_attack(unit)


class EliteAI3(NormalAI):
    def __init__(self, entity, timer, manager, path):
        super().__init__(entity, timer, manager, path)

    def perform_attack(self, units):
        if self.timer.time() - self.last_atk > self.atk_spd:
            target = self.search_enemy(units)
            if target is not None:
                self.normal_attack(target)
                units.remove(target)
                self.normal_attack(self.search_enemy(units))


class BossAI(NormalAI):
    def __init__(self, entity, timer, manager, path):
        super().__init__(entity, timer, manager, path)
        self.ultimate = False
        self.ultimate_triggered = False
        self.ultimate_trigger_time = None
        self.grid_passed = 0

    def be_controlled(self, time):
        pass

    def perform_attack(self, units):
        if self.timer.time() - self.last_atk > self.atk_spd:
            if self.ultimate_triggered:
                for unit in units:
                    self.normal_attack(unit)
                return
            target = self.search_enemy(units)
            if target is not None:
                self.normal_attack(target)
            if self.blocked:
                for unit in units:
                    if self.position.distance_to(unit) < self.range * TILE_SIZE:
                        unit.be_controlled(1)

    def update(self, units):
        self.check_blocked(units)
        self.is_blocked()
        if self.is_dead():
            return
        if self.position.x > (self.grid_passed + 1) * 80:
            self.manager.map.layout[3][self.grid_passed] = 3
            self.grid_passed += 1
        if self.hp <= self.entity.hp * 0.5 and not self.ultimate:
            self.ultimate = True
            self.ultimate_triggered = True
            self.ultimate_trigger_time = self.timer.time()
            self.atk_spd = 1
            self.atk = 1000
        if self.timer.time() - self.ultimate_trigger_time > 10:
            self.ultimate_triggered = False
            self.atk_spd = self.entity.attack_speed
            self.atk = self.entity.atk
        self.perform_attack(units)
        if not self.blocked and not self.ultimate_triggered:
            self.move()
