from entities.entity import Entity


class EnemyFactory:
    @staticmethod
    def create_goblin():
        data = {
            "hp": 50,
            "atk": 10,
            "atk_type": 0,
            "speed": 0.8,
            "defense": 0,
            "resistance": 0,
            "attack_speed": 1.5,
            "sprite_image": "assets/image/271.png",
            "type": 0,
            "id": "000"
        }
        return Entity(data)

    @staticmethod
    def create_orc():
        data = {
            "hp": 100,
            "atk": 20,
            "atk_type": 0,
            "speed": 0.6,
            "defense": 5,
            "resistance": 2,
            "attack_speed": 2.0,
            "sprite_image": "assets/image/271.png",
            "type": 0,
            "id": "001"
        }
        return Entity(data)

    enemy_map = {
        "000": create_goblin.__func__,
        "001": create_orc.__func__,
    }

    @staticmethod
    def create_enemy_by_id(enemy_id: str) -> Entity:
        if enemy_id in EnemyFactory.enemy_map:
            return EnemyFactory.enemy_map[enemy_id]()
        else:
            raise ValueError(f"Unknown enemy ID: {enemy_id}")
