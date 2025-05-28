import pygame
from pathlib import Path

class Map:
    def __init__(self, tile_definitions, layout, tile_size, asset_dir):
        """
        tile_definitions: dict[int, GridTile] — 每个 tile id 对应的图块
        layout: List[List[int]] — 关卡数组，如 [[1, 1], [0, 2]]
        tile_size: int — 每个格子的像素大小
        asset_dir: Path — 图像文件路径
        """
        self.tile_definitions = tile_definitions
        self.layout = layout
        self.tile_size = tile_size
        self.asset_dir = "assets/image"

        # 提前加载图像资源
        self.tile_images = {}
        for tile in tile_definitions.values():
            image_path = asset_dir / tile.image_name
            image = pygame.image.load(image_path).convert_alpha()
            self.tile_images[tile.id] = pygame.transform.scale(image, (tile_size, tile_size))

    def draw(self, surface):
        for row_idx, row in enumerate(self.layout):
            for col_idx, tile_id in enumerate(row):
                img = self.tile_images.get(tile_id)
                if img:
                    surface.blit(img, (col_idx * self.tile_size, row_idx * self.tile_size))