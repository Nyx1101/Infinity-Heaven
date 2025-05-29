import pygame

TILE_SIZE = 64
FPS = 60


class NormalAI:
    def __init__(self, entity, path):
        self.entity = entity
        self.blackboard = {
            "hp": entity.hp,
            "controlled": False,
            "blocked": False,
        }
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

    def attack(self, unit):
        pass

    def update(self, units):
        if self.blackboard["hp"] <= 0:
            self.dead = True
            return

        if not self.path:
            self.score = True
            return

        if self.blackboard["controlled"]:
            return

        if self.blackboard["blocked"]:
            self.attack(self.blackboard["blocker"])
            return

        current_tile = (
            int(self.position.x // TILE_SIZE),
            int(self.position.y // TILE_SIZE)
        )

        for unit in units:
            if hasattr(unit, "grid_pos") and unit.grid_pos == current_tile:
                self.blackboard["blocked"] = True
                self.blackboard["blocker"] = unit
                self.attack(unit)
                return
        else:
            self.blackboard["blocked"] = False
            self.blackboard["blocker"] = None

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
        self.blackboard["hp"] -= 0.1

    def draw(self, screen):
        if not self.dead:
            screen.blit(self.sprite, self.position)

            bar_width = 50
            bar_height = 5
            x = self.position.x
            y = self.position.y + self.sprite.get_height() + 2

            pygame.draw.rect(screen, (255, 0, 0), (x, y, bar_width, bar_height))

            hp_ratio = max(self.blackboard["hp"] / self.entity.hp, 0)
            green_width = int(bar_width * hp_ratio)
            pygame.draw.rect(screen, (0, 255, 0), (x, y, green_width, bar_height))
