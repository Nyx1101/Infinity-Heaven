import pygame

TILE_SIZE = 64


class EnemySprite(pygame.sprite.Sprite):
    def __init__(self, entity, start_tile):
        super().__init__()
        self.image = pygame.image.load(entity.sprite_image).convert_alpha()
        self.rect = self.image.get_rect()

        x, y = start_tile
        self.rect.topleft = (x * TILE_SIZE, y * TILE_SIZE)

        self.marked_for_removal = False
