import pygame
from battle.AI.base_ai import BaseAI

TILE_SIZE = 64
FPS = 60


class NormalAI(BaseAI):
    """
    Normal enemy AI that follows a path and checks for blocking units.
    """
    def __init__(self, entity, timer, manager, path):
        super().__init__(entity, timer, manager)
        self.path = list(path)  # Remaining movement path (grid coordinates)
        self.score = False  # Marks whether the unit has reached the goal
        self.position = pygame.Vector2(
            self.path[0][0] * TILE_SIZE,
            self.path[0][1] * TILE_SIZE
        )
        self.last_update = self.timer.time()
        self.speed_pixel_per_sec = entity.speed * TILE_SIZE

    def check_blocked(self, units):
        """
        Check whether this unit is blocked by any player units.
        """
        for unit in units:
            enemy_tile = unit.grid_pos
            target_pos = pygame.Vector2(
                enemy_tile[0] * TILE_SIZE,
                enemy_tile[1] * TILE_SIZE
            )
            delta = target_pos - self.position
            distance = delta.length()
            if distance < 20:  # Consider blocked if very close
                self.blocked = True
                self.blocker.append(unit)
                unit.blocker.append(self)
                unit.blocked = True

    def move(self):
        """
        Move along the path toward the next tile.
        """
        if not self.path:
            self.score = True  # Reached the goal
            return

        target_tile = self.path[0]
        target_pos = pygame.Vector2(
            target_tile[0] * TILE_SIZE,
            target_tile[1] * TILE_SIZE
        )

        delta = target_pos - self.position
        distance = delta.length()

        if distance < 1:
            self.path.pop(0)  # Reached this tile, go to next
            return

        # Move along the dominant axis (X or Y)
        move = pygame.Vector2(0, 0)
        if abs(delta.x) > abs(delta.y):
            move.x = self.speed_pixel_per_sec * (self.timer.time() - self.last_update) if delta.x > 0 else -self.speed_pixel_per_sec * (self.timer.time() - self.last_update)
        else:
            move.y = self.speed_pixel_per_sec * (self.timer.time() - self.last_update) if delta.y > 0 else -self.speed_pixel_per_sec * (self.timer.time() - self.last_update)

        # Clamp movement to avoid overshooting
        if move.length() > distance:
            move = delta

        self.position += move

    def update(self, units):
        """
        Update AI behavior each frame.
        """
        self.check_blocked(units)
        super().update(units)
        if not self.blocked:
            self.move()
        self.last_update = self.timer.time()


class EliteAI1(NormalAI):
    """
    Elite enemy AI that takes damage over time when blocked.
    """
    def __init__(self, entity, timer, manager, path):
        super().__init__(entity, timer, manager, path)

    def update(self, units):
        super().update(units)
        if self.blocked:
            self.hp -= self.entity.hp * 0.02 / FPS  # Lose 2% HP per second if blocked


class EliteAI2(NormalAI):
    """
    Elite AI that performs area-of-effect attacks.
    """
    def __init__(self, entity, timer, manager, path):
        super().__init__(entity, timer, manager, path)

    def perform_attack(self, units):
        """
        Attack all units around the target.
        """
        if self.timer.time() - self.last_atk > self.atk_spd:
            target = self.search_enemy(units)
            if target is not None:
                for unit in units:
                    if unit.position.distance_to(target.position) < 1.5 * TILE_SIZE:
                        self.normal_attack(unit)


class EliteAI3(NormalAI):
    """
    Elite AI that instantly kills the target and continues attacking another.
    """
    def __init__(self, entity, timer, manager, path):
        super().__init__(entity, timer, manager, path)

    def perform_attack(self, units):
        """
        Remove the first target from the list, then attack another.
        """
        if self.timer.time() - self.last_atk > self.atk_spd:
            target = self.search_enemy(units)
            if target is not None:
                self.normal_attack(target)
                units.remove(target)  # Instantly remove target
                self.normal_attack(self.search_enemy(units))


class BossAI(NormalAI):
    """
    Boss AI with an ultimate phase and crowd control ability.
    """
    def __init__(self, entity, timer, manager, path):
        super().__init__(entity, timer, manager, path)
        self.ultimate = False  # Whether ultimate has been triggered
        self.ultimate_triggered = False  # Currently in ultimate mode
        self.ultimate_trigger_time = None

    def be_controlled(self, time):
        """
        Boss is immune to control effects.
        """
        pass

    def perform_attack(self, units):
        """
        Boss performs normal or ultimate attack depending on state.
        """
        if self.timer.time() - self.last_atk > self.atk_spd:
            if self.ultimate_triggered:
                for unit in units:
                    self.normal_attack(unit)
                return

            target = self.search_enemy(units)
            if target is not None:
                self.normal_attack(target)

            # Crowd control when blocked
            if self.blocked:
                for unit in units:
                    if self.position.distance_to(unit.position) < self.range * TILE_SIZE:
                        unit.be_controlled(1)

    def update(self, units):
        """
        Update the boss logic, including triggering ultimate.
        """
        self.check_blocked(units)
        self.is_blocked()
        if self.is_dead():
            return

        # Trigger ultimate when HP < 50%
        if self.hp <= self.entity.hp * 0.5 and not self.ultimate:
            self.ultimate = True
            self.ultimate_triggered = True
            self.ultimate_trigger_time = self.timer.time()
            self.atk_spd = 1.5
            self.atk = 400

        # Ultimate ends after 10 seconds
        if self.ultimate_triggered:
            if self.timer.time() - self.ultimate_trigger_time > 10:
                self.ultimate_triggered = False
                self.atk_spd = self.entity.attack_speed
                self.atk = self.entity.atk

        self.perform_attack(units)
        self.update_attack_animation()

        # Boss doesn't move during ultimate
        if not self.blocked and not self.ultimate_triggered:
            self.move()

        self.last_update = self.timer.time()
