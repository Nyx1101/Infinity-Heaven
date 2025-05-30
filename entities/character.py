from entities.entity import Entity


class CharacterFactory:
    @staticmethod
    def create_warrior():
        data = {
            "hp": 120,
            "atk": 15,
            "atk_type": 0,
            "speed": 0,
            "defense": 10,
            "resistance": 5,
            "attack_speed": 1.2,
            "sprite_image": "assets/image/206.png",
            "type": 1,
            "id": "100"
        }
        return Entity(data)

    @staticmethod
    def create_archer():
        data = {
            "hp": 80,
            "atk": 18,
            "atk_type": 0,
            "speed": 0,
            "defense": 10,
            "resistance": 2,
            "attack_speed": 1.8,
            "sprite_image": "assets/image/206.png",
            "type": 1,
            "id": "101"
        }
        return Entity(data)

    @staticmethod
    def create_mage():
        data = {
            "hp": 70,
            "atk": 25,
            "atk_type": 0,
            "speed": 0,
            "defense": 10,
            "resistance": 10,
            "attack_speed": 2.0,
            "sprite_image": "assets/image/206.png",
            "type": 1,
            "id": "102"
        }
        return Entity(data)

    character_map = {
        "100": create_warrior.__func__,
        "101": create_archer.__func__,
        "102": create_mage.__func__,
    }

    @staticmethod
    def create_character_by_id(char_id: str) -> Entity:
        if char_id in CharacterFactory.character_map:
            return CharacterFactory.character_map[char_id]()
        else:
            raise ValueError(f"Unknown character ID: {char_id}")
