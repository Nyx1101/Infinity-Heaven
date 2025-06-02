class Entity:
    def __init__(self, data):
        self.hp = data["hp"]
        self.atk = data["atk"]
        self.atk_type = data["atk_type"]
        if data.get("speed") is not None:
            self.speed = data["speed"]
        else:
            self.speed = 0
        if data.get("cost") is not None:
            self.cost = data["cost"]
        else:
            self.cost = 0
        self.defense = data["defense"]
        self.resistance = data["resistance"]
        self.attack_speed = data["attack_speed"]
        self.range = data["range"]
        if data.get("redeployment_time") is not None:
            self.redeployment_time = data["redeployment_time"]
        else:
            self.redeployment_time = 0
        if data.get("cd") is not None:
            self.cd = data["cd"]
        else:
            self.cd = 0
        if data.get("duration") is not None:
            self.duration = data["duration"]
        else:
            self.duration = 0
        self.sprite_image = data["sprite_image"]
        self.type = data["type"]
        self.id = data["id"]
