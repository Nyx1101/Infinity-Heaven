from pathlib import Path
from battle.level.grid import Grid
from battle.level.map import Map
from battle.level.level_flow import LevelFlow


class LevelLoader:
    def __init__(self):
        self.asset_dir = Path("assets/image")
        self.tile_size = 64

    def load_tile_defs(self):
        return {
            0: Grid(0, "038.png"),
            1: Grid(1, "040.png"),
            2: Grid(2, "061.png"),
            3: Grid(3, "063.png"),
            4: Grid(4, "062.png"),
            5: Grid(5, "064.png")
        }

    def load_map_layout(self):
        return [
            [5, 1, 2, 2, 2, 0, 2, 2, 2, 0, 4],
            [2, 2, 2, 0, 2, 2, 2, 0, 2, 2, 2],
            [2, 1, 0, 0, 2, 0, 2, 2, 2, 0, 2],
            [5, 2, 2, 2, 2, 2, 2, 2, 2, 2, 4],
            [2, 1, 0, 0, 2, 0, 2, 2, 2, 0, 2],
            [2, 2, 2, 0, 2, 2, 2, 0, 2, 2, 2],
            [5, 1, 2, 2, 2, 0, 2, 2, 2, 0, 4]
        ]

    def load_level_1_map(self):
        tile_defs = self.load_tile_defs()
        layout = self.load_map_layout()
        return Map(
            tile_definitions=tile_defs,
            layout=layout,
            tile_size=self.tile_size,
            asset_dir=self.asset_dir
        )

    def load_level_1_enemy(self):
        spawn_schedule = [
            {"id": "001", "time": 1.0, "path": [(0, 0), (0, 3), (10, 3)]},
            {"id": "001", "time": 3.0, "path": [(0, 0), (0, 3), (10, 3)]},
            {"id": "001", "time": 5.0, "path": [(0, 0), (0, 3), (10, 3)]},
        ]
        return LevelFlow(spawn_schedule)
