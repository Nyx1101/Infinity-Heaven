from pathlib import Path
from battle.level.grid import Grid
from battle.level.map import Map

def load_level_1():
    TILE_DEFS = {
        0: Grid(0, "038.png"),
        1: Grid(1, "040.png"),
        2: Grid(2, "061.png"),
        3: Grid(3, "063.png"),
        4: Grid(4, "062.png"),
        5: Grid(5, "064.png")

    }

    MAP_LAYOUT = [
        [5, 1, 2, 2, 2, 0, 2, 2, 2, 0, 4],
        [2, 2, 2, 0, 2, 2, 2, 0, 2, 2, 2],
        [2, 1, 0, 0, 2, 0, 2, 2, 2, 0, 2],
        [5, 2, 2, 2, 2, 2, 2, 2, 2, 2, 4],
        [2, 1, 0, 0, 2, 0, 2, 2, 2, 0, 2],
        [2, 2, 2, 0, 2, 2, 2, 0, 2, 2, 2],
        [5, 1, 2, 2, 2, 0, 2, 2, 2, 0, 4]
    ]

    return Map(
        tile_definitions=TILE_DEFS,
        layout=MAP_LAYOUT,
        tile_size=64,
        asset_dir=Path("assets/image")
    )