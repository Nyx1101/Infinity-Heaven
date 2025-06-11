import pygame


class Map:
    def __init__(self, tile_definitions, layout, tile_size, asset_dir):
        """
        Initialize the Map object.
        """
        self.tile_definitions = tile_definitions
        self.layout = layout
        self.tile_size = tile_size

        # Hardcoded asset directory override — consider using the passed asset_dir instead
        self.asset_dir = "assets/image"

        # Dictionary to hold loaded and scaled pygame surfaces for each tile ID
        self.tile_images = {}

        # Load and scale each tile image based on tile definitions
        for tile in tile_definitions.values():
            image_path = asset_dir / tile.image_name  # Construct full path to image file
            image = pygame.image.load(image_path).convert_alpha()  # Load image with alpha transparency
            # Scale the image to the tile size and store it keyed by tile ID
            self.tile_images[tile.id] = pygame.transform.scale(image, (tile_size, tile_size))

    def draw(self, surface):
        """
        Draw the map onto the given surface.
        """
        # Calculate y coordinate of bottom row to clear it with black background
        bottom_y = surface.get_height() - self.tile_size

        # Fill bottom row area with black (to clear previous frame or for UI)
        surface.fill((0, 0, 0), pygame.Rect(0, bottom_y, surface.get_width(), self.tile_size))

        # Iterate over each tile in the 2D layout grid and draw corresponding tile images
        for row_idx, row in enumerate(self.layout):
            for col_idx, tile_id in enumerate(row):
                img = self.tile_images.get(tile_id)
                if img:
                    # Draw tile image at the correct pixel position based on tile size
                    surface.blit(img, (col_idx * self.tile_size, row_idx * self.tile_size))
