from pathlib import Path
from battle.level.grid import Grid
from battle.level.map import Map
from battle.level.level_flow import LevelFlow
from utility.data import LEVEL_MAPS, LEVEL_SCHEDULES


class LevelLoader:
    def __init__(self, level):
        self.asset_dir = Path("assets/image")
        self.tile_size = 64
        self.level = level

    @staticmethod
    def load_tile_defs():
        return {
            0: Grid(0, "grid0.png"),
            1: Grid(1, "grid1.png"),
            2: Grid(2, "grid2.png"),
            3: Grid(3, "grid3.png"),
            4: Grid(4, "grid4.png"),
            5: Grid(5, "grid5.png")
        }

    def load_map(self):
        tile_defs = self.load_tile_defs()
        layout = LEVEL_MAPS[self.level]
        return Map(
            tile_definitions=tile_defs,
            layout=layout,
            tile_size=self.tile_size,
            asset_dir=self.asset_dir
        )

    def load_enemy(self):
        print(self.level)
        return LevelFlow(LEVEL_SCHEDULES[self.level])
