from pathlib import Path
from battle.level.grid import Grid
from battle.level.map import Map
from battle.level.level_flow import LevelFlow
from utility.data import LEVEL_MAPS, LEVEL_SCHEDULES


class LevelLoader:
    def __init__(self, level):
        """
        Initialize the LevelLoader with a specific level number.
        """
        self.asset_dir = Path("assets/image")  # Directory where tile images are stored
        self.tile_size = 64                    # Tile size in pixels
        self.level = level                     # Current level number

    @staticmethod
    def load_tile_defs():
        """
        Load and return tile definitions mapping tile IDs to Grid objects.
        """
        return {
            0: Grid(0, "grid0.png"),
            1: Grid(1, "grid1.png"),
            2: Grid(2, "grid2.png"),
            3: Grid(3, "grid3.png"),
            4: Grid(4, "grid4.png"),
            5: Grid(5, "grid5.png")
        }

    def load_map(self):
        """
        Load the map for the current level using tile definitions and layout.
        """
        tile_defs = self.load_tile_defs()
        layout = LEVEL_MAPS[self.level]  # Get tile layout for current level from global data
        return Map(
            tile_definitions=tile_defs,
            layout=layout,
            tile_size=self.tile_size,
            asset_dir=self.asset_dir
        )

    def load_enemy(self):
        """
        Load the enemy spawn schedule for the current level.
        """
        print(self.level)  # Debug: print the level number being loaded
        return LevelFlow(LEVEL_SCHEDULES[self.level])
