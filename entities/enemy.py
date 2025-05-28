from entities.entity import Entity


class EnemyFactory:
    @staticmethod
    def create_goblin():
        data = {
            "hp": 50,
            "atk": 10,
            "speed": 0.8,
            "defense": 0,
            "resistance": 0,
            "attack_speed": 1.5,
            "sprite_image": "assets/image/038.png",
            "type": 0
        }
        return Entity(data)
