WARRIOR = {
    "hp": 800,
    "atk": 200,
    "atk_type": 0,
    "defense": 100,
    "resistance": 30,
    "attack_speed": 1.2,
    "range": 0,
    "cost": 10,
    "redeployment_time": 30,
    "sprite_image": "assets/image/character1.png",
    "type": 1,
    "id": 100
}

ARCHER = {
    "hp": 400,
    "atk": 200,
    "atk_type": 0,
    "defense": 40,
    "resistance": 20,
    "attack_speed": 1,
    "range": 3,
    "cost": 10,
    "redeployment_time": 30,
    "sprite_image": "assets/image/character2.png",
    "type": 1,
    "id": 101
}

HEALER = {
    "hp": 500,
    "atk": 150,
    "atk_type": 2,
    "defense": 50,
    "resistance": 30,
    "attack_speed": 2.5,
    "range": 1.5,
    "cost": 10,
    "redeployment_time": 40,
    "sprite_image": "assets/image/character3.png",
    "type": 2,
    "id": 102
}

MAGE = {
    "hp": 400,
    "atk": 250,
    "atk_type": 1,
    "defense": 30,
    "resistance": 50,
    "attack_speed": 1.6,
    "range": 2.5,
    "cost": 10,
    "redeployment_time": 40,
    "sprite_image": "assets/image/character4.png",
    "type": 1,
    "id": 103
}

TANK_PHYSICAL = {
    "hp": 1200,
    "atk": 120,
    "atk_type": 0,
    "defense": 150,
    "resistance": 40,
    "attack_speed": 2,
    "range": 0,
    "cost": 10,
    "redeployment_time": 40,
    "sprite_image": "assets/image/character5.png",
    "type": 1,
    "id": 104
}

ASSASSIN = {
    "hp": 500,
    "atk": 180,
    "atk_type": 0,
    "defense": 70,
    "resistance": 20,
    "attack_speed": 0.8,
    "range": 0,
    "cost": 10,
    "redeployment_time": 20,
    "sprite_image": "assets/image/character6.png",
    "type": 1,
    "id": 105
}

CONTROLLER = {
    "hp": 600,
    "atk": 150,
    "atk_type": 1,
    "defense": 80,
    "resistance": 30,
    "attack_speed": 2,
    "range": 2,
    "cost": 10,
    "redeployment_time": 30,
    "sprite_image": "assets/image/character7.png",
    "type": 1,
    "id": 106
}

TANK_MAGIC = {
    "hp": 1000,
    "atk": 150,
    "atk_type": 1,
    "defense": 120,
    "resistance": 50,
    "attack_speed": 1.5,
    "range": 0,
    "cost": 10,
    "redeployment_time": 50,
    "sprite_image": "assets/image/character8.png",
    "type": 1,
    "id": 107
}

SUPPORTER = {
    "hp": 600,
    "atk": 0,
    "atk_type": 0,
    "defense": 70,
    "resistance": 30,
    "attack_speed": 3600,
    "range": 2,
    "cost": 10,
    "redeployment_time": 30,
    "sprite_image": "assets/image/character9.png",
    "type": 1,
    "id": 108
}

SKILL_MAP = {
    (100, 1): (30, 3600),
    (100, 2): (10, 10),
    (101, 1): (20, 10),
    (101, 2): (10, 0),
    (102, 1): (30, 3600),
    (102, 2): (20, 30),
    (103, 1): (5, 0),
    (103, 2): (30, 10),
    (104, 1): (10, 0),
    (104, 2): (20, 20),
    (105, 1): (0, 10),
    (105, 2): (0, 0),
    (106, 1): (10, 10),
    (106, 2): (30, 20),
    (107, 1): (30, 3600),
    (107, 2): (20, 15),
    (108, 1): (7, 0),
    (108, 2): (60, 6),
}

SKILL_SELECTED = [0, 0, 0, 0, 0, 0, 0, 0, 0]

DOG = {
    "hp": 400,
    "atk": 100,
    "atk_type": 0,
    "defense": 0,
    "resistance": 0,
    "attack_speed": 1.2,
    "range": 0,
    "speed": 1,
    "sprite_image": "assets/image/271.png",
    "type": 0,
    "id": 200
}

SOLDIER = {
    "hp": 800,
    "atk": 140,
    "atk_type": 0,
    "defense": 50,
    "resistance": 20,
    "attack_speed": 1.5,
    "range": 0,
    "speed": 0.5,
    "sprite_image": "assets/image/271.png",
    "type": 0,
    "id": 201
}

SHOOTER = {
    "hp": 600,
    "atk": 120,
    "atk_type": 0,
    "defense": 30,
    "resistance": 10,
    "attack_speed": 1,
    "range": 2.5,
    "speed": 0.4,
    "sprite_image": "assets/image/202.png",
    "type": 0,
    "id": 202
}

WITCH = {
    "hp": 1000,
    "atk": 120,
    "atk_type": 1,
    "defense": 50,
    "resistance": 40,
    "attack_speed": 1.5,
    "range": 1.8,
    "speed": 0.4,
    "sprite_image": "assets/image/203.png",
    "type": 0,
    "id": 206
}

BIG_SHIELD = {
    "hp": 2000,
    "atk": 160,
    "atk_type": 0,
    "defense": 120,
    "resistance": 0,
    "attack_speed": 2.5,
    "range": 0,
    "speed": 0.3,
    "sprite_image": "assets/image/204.png",
    "type": 0,
    "id": 204
}

CANNON = {
    "hp": 1200,
    "atk": 150,
    "atk_type": 0,
    "defense": 80,
    "resistance": 0,
    "attack_speed": 2.5,
    "range": 2,
    "speed": 0.3,
    "sprite_image": "assets/image/205.png",
    "type": 0,
    "id": 203
}

ELITE_PHYSICAL = {
    "hp": 3000,
    "atk": 250,
    "atk_type": 0,
    "defense": 100,
    "resistance": 30,
    "attack_speed": 2,
    "range": 0,
    "speed": 0.6,
    "sprite_image": "assets/image/206.png",
    "type": 0,
    "id": 205
}

ELITE_MAGIC = {
    "hp": 1500,
    "atk": 180,
    "atk_type": 1,
    "defense": 50,
    "resistance": 50,
    "attack_speed": 1.5,
    "range": 1.8,
    "speed": 0.4,
    "sprite_image": "assets/image/207.png",
    "type": 0,
    "id": 208
}

ELITE_AOE = {
    "hp": 1800,
    "atk": 250,
    "atk_type": 0,
    "defense": 80,
    "resistance": 20,
    "attack_speed": 2.5,
    "range": 0,
    "speed": 0.3,
    "sprite_image": "assets/image/208.png",
    "type": 0,
    "id": 207
}

BOSS = {
    "hp": 10000,
    "atk": 250,
    "atk_type": 0,
    "defense": 200,
    "resistance": 70,
    "attack_speed": 2.5,
    "range": 1.5,
    "speed": 0.5,
    "sprite_image": "assets/image/208.png",
    "type": 0,
    "id": 209
}

CHARACTER_DATA = {
    100: WARRIOR,
    101: ARCHER,
    102: HEALER,
    103: MAGE,
    104: TANK_PHYSICAL,
    105: TANK_MAGIC,
    106: ASSASSIN,
    107: CONTROLLER,
    108: SUPPORTER
}

ENEMY_DATA = {
    "DOG": DOG,
    "SOLDIER": SOLDIER,
    "SHOOTER": SHOOTER,
    "WITCH": WITCH,
    "BIG_SHIELD": BIG_SHIELD,
    "CANNON": CANNON,
    "ELITE_PHYSICAL": ELITE_PHYSICAL,
    "ELITE_MAGIC": ELITE_MAGIC,
    "ELITE_AOE": ELITE_AOE
}

LEVEL_1_MAP = [
    [1, 1, 1, 1, 1, 5, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 3, 0, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 2, 2, 2, 0, 1, 1],
    [1, 5, 3, 2, 0, 2, 0, 2, 2, 4, 1],
    [1, 1, 0, 2, 0, 2, 1, 0, 1, 1, 1],
    [1, 1, 1, 2, 2, 2, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

LEVEL_1_SCHEDULE = [
    {"id": 200, "time": [10, 13, 16, 19, 22, 25], "path": [(1, 3), (3, 3), (3, 5), (5, 5), (5, 2), (7, 2), (7, 3), (9, 3)]},
    {"id": 201, "time": [20, 24, 28, 40, 43, 46, 49], "path": [(1, 3), (3, 3), (3, 5), (5, 5), (5, 2), (7, 2), (7, 3), (9, 3)]},
    {"id": 202, "time": [21, 26, 31, 41, 44, 47, 50], "path": [(1, 3), (3, 3), (3, 5), (5, 5), (5, 2), (7, 2), (7, 3), (9, 3)]},
    {"id": 203, "time": [50, 60], "path": [(5, 1), (5, 2), (7, 2), (7, 3), (9, 3)]}
]

LEVEL_2_MAP = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 2, 2, 2, 2, 2, 2, 2, 1, 1],
    [1, 1, 2, 0, 0, 0, 0, 0, 2, 1, 1],
    [1, 1, 2, 2, 2, 2, 2, 2, 2, 1, 1],
    [1, 1, 2, 0, 0, 0, 0, 0, 2, 1, 1],
    [1, 5, 2, 1, 1, 1, 1, 1, 2, 4, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

LEVEL_2_SCHEDULE = [
    {"id": 200, "time": [10.0, 13.0, 16.0, 19.0, 22.0, 25.0], "path": [(1, 5), (2, 5), (2, 1), (8, 1), (8, 5), (9, 5)]},
    {"id": 201, "time": [20.0, 24.0, 28.0, 40.0, 43, 46, 49], "path": [(1, 5), (2, 5), (2, 1), (8, 1), (8, 5), (9, 5)]},
    {"id": 202, "time": [21.0, 26.0, 31.0, 41, 44, 47, 50], "path": [(1, 5), (2, 5), (2, 1), (8, 1), (8, 5), (9, 5)]},
    {"id": 203, "time": [50, 60], "path": [(5, 1), (5, 2), (7, 2), (7, 3), (9, 3)]}
]

LEVEL_3_MAP = [
    [1, 1, 5, 1, 1, 5, 1, 1, 5, 1, 1],
    [1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1],
    [1, 0, 2, 1, 0, 2, 2, 2, 2, 1, 1],
    [1, 1, 2, 0, 0, 2, 0, 0, 2, 1, 1],
    [1, 1, 2, 2, 2, 2, 0, 1, 2, 0, 1],
    [1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1],
    [1, 1, 4, 1, 1, 4, 1, 1, 4, 1, 1]
]

LEVEL_4_MAP = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 2, 2, 2, 5, 1, 1, 1, 1, 1],
    [1, 1, 2, 0, 1, 2, 2, 2, 2, 1, 1],
    [1, 1, 2, 0, 0, 1, 1, 1, 2, 1, 1],
    [1, 1, 2, 2, 2, 0, 1, 1, 2, 1, 1],
    [1, 1, 0, 0, 4, 2, 2, 2, 2, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

LEVEL_5_MAP = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 2, 2, 2, 2, 2, 2, 4, 1],
    [1, 1, 1, 2, 0, 1, 0, 1, 0, 1, 1],
    [1, 5, 2, 2, 2, 2, 2, 2, 2, 4, 1],
    [1, 1, 1, 2, 0, 1, 0, 1, 0, 1, 1],
    [1, 1, 1, 2, 2, 2, 2, 2, 2, 4, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

LEVEL_6_MAP = [
    [5, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4],
    [2, 1, 5, 1, 1, 1, 1, 1, 4, 1, 2],
    [2, 1, 3, 1, 1, 1, 1, 1, 3, 1, 2],
    [2, 0, 3, 0, 1, 1, 1, 0, 3, 1, 2],
    [2, 1, 2, 2, 2, 2, 2, 2, 2, 1, 2],
    [2, 1, 0, 0, 0, 0, 0, 0, 0, 1, 2],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]
]

LEVEL_7_MAP = [
    [5, 1, 2, 2, 2, 0, 2, 2, 2, 0, 4],
    [2, 2, 2, 0, 2, 2, 2, 0, 2, 2, 2],
    [2, 1, 0, 0, 2, 0, 2, 2, 2, 0, 2],
    [5, 2, 2, 2, 2, 2, 2, 2, 2, 2, 4],
    [2, 1, 0, 0, 2, 0, 2, 2, 2, 0, 2],
    [2, 2, 2, 0, 2, 2, 2, 0, 2, 2, 2],
    [5, 1, 2, 2, 2, 0, 2, 2, 2, 0, 4]
]

LEVEL_MAPS = {
    1: LEVEL_1_MAP,
    2: LEVEL_2_MAP,
    3: LEVEL_3_MAP,
    4: LEVEL_4_MAP,
    5: LEVEL_5_MAP,
    6: LEVEL_6_MAP,
    7: LEVEL_7_MAP
}

ELITE_BADGE = [0, 0]
ELITE_PROGRESS = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
LEVEL_PROGRESS = [0, 0, 0, 0, 0, 0, 0]
STORY_PROGRESS = [0, 0, 0, 0, 0, 0, 0]
CURRENT_STAGE = None
