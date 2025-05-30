import pygame, time

TILE_SIZE = 64
FPS = 60


class NormalAI:
    def __init__(self, entity, path):
        self.entity = entity
        self.hp = self.entity.hp
        self.atk = self.entity.atk
        self.dfs = self.entity.defense
        self.res = self.entity.resistance
        self.atk_spd = self.entity.attack_speed
        self.atk_type = self.entity.atk_type
        self.controlled = False
        self.blocked = False
        self.blocker = None
        self.path = list(path)
        self.sprite = pygame.image.load(entity.sprite_image).convert_alpha()
        self.dead = False
        self.score = False

        self.position = pygame.Vector2(
            self.path[0][0] * TILE_SIZE,
            self.path[0][1] * TILE_SIZE
        )
        self.speed_grid_per_sec = entity.speed
        self.speed_pixel_per_frame = self.speed_grid_per_sec * TILE_SIZE / FPS
        self.last_atk = time.time()

    def normal_attack(self, unit):
        if not unit:
            return
        if self.atk_type == 0:
            unit.hp -= (self.atk - unit.dfs)
        elif self.atk_type == 1:
            unit.hp -= (self.atk * (1 - unit.res / 100))

    def update(self, units):
        if self.hp <= 0:
            self.dead = True
            if self.blocker:
                self.blocker.remove(self)
            return

        if not self.path:
            self.score = True
            return

        if self.controlled:
            return

        if self.blocked:
            if self.blocker.dead:
                self.blocked = False
                self.blocker = None
                return

            if time.time() - self.last_atk > self.atk_spd:
                self.last_atk = time.time()
                self.normal_attack(self.blocker)
                return
            else:
                return

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
                self.blocker = unit
                unit.blocker.append(self)
                return
        else:
            self.blocked = False
            self.blocker = None

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
