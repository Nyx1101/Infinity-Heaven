import pygame

TILE_SIZE = 64  # Size of one tile in pixels


class EnemySprite(pygame.sprite.Sprite):
    def __init__(self, entity, start_tile):
        """
        Initialize an enemy sprite.
        """
        super().__init__()

        # Load the sprite image with transparency support
        self.image = pygame.image.load(entity.sprite_image).convert_alpha()

        # Get the rectangular area for positioning and collision detection
        self.rect = self.image.get_rect()

        # Set the top-left corner of the sprite according to tile coordinates
        x, y = start_tile
        self.rect.topleft = (x * TILE_SIZE, y * TILE_SIZE)

        # Flag to mark this sprite for removal from sprite groups or game
        self.marked_for_removal = False
