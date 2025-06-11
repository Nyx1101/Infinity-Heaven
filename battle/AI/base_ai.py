import pygame
from entities.entity import Entity

TILE_SIZE = 64


class BaseAI:
    def __init__(self, entity: Entity, timer, manager):
        self.entity = entity
        self.manager = manager
        self.hp = self.entity.hp
        self.atk = self.entity.atk
        self.dfs = self.entity.defense
        self.res = self.entity.resistance
        self.atk_spd = self.entity.attack_speed
        self.atk_type = self.entity.atk_type
        self.range = self.entity.range
        raw_sprite = pygame.image.load(entity.sprite_image).convert_alpha()
        self.sprite = pygame.transform.smoothscale(raw_sprite, (TILE_SIZE, TILE_SIZE))
        self.timer = timer
        self.controlled = False
        self.controlled_time = None
        self.control_duration = 0
        self.blocked = False
        self.blocker = []
        self.dead = False
        self.last_atk = self.timer.time()
        self.position = None

    def normal_attack(self, unit):
        if not unit:
            self.last_atk = self.timer.time()
            return None
        if self.atk_type == 0:
            damage = (self.atk - unit.dfs)
            damage = max(damage, self.atk * 0.1)
            unit.hp -= damage
            self.last_atk = self.timer.time()
            return damage
        elif self.atk_type == 1:
            damage = (self.atk * (1 - unit.res / 100))
            damage = max(damage, self.atk * 0.1)
            unit.hp -= damage
            self.last_atk = self.timer.time()
            return damage
        else:
            unit.hp += self.atk
            unit.hp = min(unit.hp, unit.entity.hp)
            self.last_atk = self.timer.time()

    def is_dead(self):
        if self.hp <= 0 or self.dead:
            self.dead = True
            for blocker in self.blocker:
                blocker.blocker.remove(self)
            return True

    def be_controlled(self, time):
        self.controlled = True
        self.control_duration = time
        self.controlled_time = self.timer.time()

    def is_controlled(self):
        if self.controlled:
            if self.controlled_time + self.control_duration < self.timer.time():
                self.controlled = False
                self.controlled_time = None
                self.control_duration = 0
                return False
            return True

    def is_blocked(self):
        if self.blocker:
            self.blocked = True
        else:
            self.blocked = False

    def search_enemy(self, units):
        if self.atk_type == 2:
            minimum = 10000
            target = None
            for ally in units:
                distance = self.position.distance_to(ally.position)
                if distance < self.range * TILE_SIZE and ally.hp < ally.entity.hp:
                    if ally.hp <= minimum:
                        minimum = ally.hp
                        target = ally
            return target
        if self.blocker:
            return self.blocker[0]
        if self.range == 0:
            return None
        target = None
        nearest = 10000
        for unit in units:
            distance = self.position.distance_to(unit.position)
            if distance < nearest:
                nearest = distance
                target = unit
        if nearest < self.range * TILE_SIZE:
            return target

    def perform_attack(self, units):
        if self.timer.time() - self.last_atk > self.atk_spd:
            target = self.search_enemy(units)
            if target is not None:
                self.normal_attack(target)

    def update(self, units):
        self.is_blocked()
        if self.is_dead():
            return
        if self.is_controlled():
            return
        self.perform_attack(units)

    def draw(self, screen):
        if not self.dead:
            screen.blit(self.sprite, self.position)

            bar_width = 50
            bar_height = 5
            x = self.position.x
            y = self.position.y + self.sprite.get_height() + 2

            pygame.draw.rect(screen, (255, 0, 0), (x, y, bar_width, bar_height))

            hp_ratio = max(self.hp / self.entity.hp, 0)
            green_width = int(bar_width * hp_ratio)
            pygame.draw.rect(screen, (0, 255, 0), (x, y, green_width, bar_height))
