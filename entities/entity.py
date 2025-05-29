class Entity:
    def __init__(self, data):
        self.hp = data["hp"]
        self.atk = data["atk"]
        self.speed = data["speed"]
        self.defense = data["defense"]
        self.resistance = data["resistance"]
        self.attack_speed = data["attack_speed"]
        self.sprite_image = data["sprite_image"]
        self.type = data["type"]
