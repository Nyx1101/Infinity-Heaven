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
            "dead": False,
        }
        self.path = list(path)  # 确保是可变列表
        self.sprite = pygame.image.load(entity.sprite_image).convert_alpha()
        self.dead = False
        # 初始位置：格子左上角像素坐标，不偏移中心
        self.position = pygame.Vector2(
            self.path[0][0] * TILE_SIZE,
            self.path[0][1] * TILE_SIZE
        )
        self.speed_grid_per_sec = entity.speed  # 格子/秒速度
        self.speed_pixel_per_frame = self.speed_grid_per_sec * TILE_SIZE / FPS

    def die(self):
        self.dead = True
        self.blackboard["dead"] = True
        print("Enemy died")

    def update(self):
        if self.blackboard["hp"] <= 0 and not self.dead:
            self.die()
            return

        if self.dead or not self.path:
            return

        target_tile = self.path[0]
        target_pos = pygame.Vector2(
            target_tile[0] * TILE_SIZE,
            target_tile[1] * TILE_SIZE
        )

        delta = target_pos - self.position
        distance = delta.length()

        # 到达阈值，这里设为 1 像素
        if distance < 1:
            self.path.pop(0)
            return

        # 移动方向限制上下或左右
        move = pygame.Vector2(0, 0)
        if abs(delta.x) > abs(delta.y):
            move.x = self.speed_pixel_per_frame if delta.x > 0 else -self.speed_pixel_per_frame
        else:
            move.y = self.speed_pixel_per_frame if delta.y > 0 else -self.speed_pixel_per_frame

        if move.length() > distance:
            move = delta

        # 防止“移动过头”，夹住目标点
        if move.length() > distance:
            move = delta

        self.position += move

    def draw(self, screen):
        if not self.dead:
            screen.blit(self.sprite, self.position)