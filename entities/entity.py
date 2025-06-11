class Entity:
    def __init__(self, data):
        # Initialize entity's hit points (health)
        self.hp = data["hp"]

        # Initialize attack power and attack type (e.g., physical, magic, heal)
        self.atk = data["atk"]
        self.atk_type = data["atk_type"]

        # Initialize movement speed; default to 0 if not provided
        if data.get("speed") is not None:
            self.speed = data["speed"]
        else:
            self.speed = 0

        # Initialize deployment cost; default to 0 if not provided
        if data.get("cost") is not None:
            self.cost = data["cost"]
        else:
            self.cost = 0

        # Initialize defense and resistance values
        self.defense = data["defense"]
        self.resistance = data["resistance"]

        # Initialize attack speed and attack range
        self.attack_speed = data["attack_speed"]
        self.range = data["range"]

        # Initialize redeployment time; default to 0 if not provided
        if data.get("redeployment_time") is not None:
            self.redeployment_time = data["redeployment_time"]
        else:
            self.redeployment_time = 0

        # Initialize skill cooldown (cd); default to 0 if not provided
        if data.get("cd") is not None:
            self.cd = data["cd"]
        else:
            self.cd = 0

        # Initialize skill duration; default to 0 if not provided
        if data.get("duration") is not None:
            self.duration = data["duration"]
        else:
            self.duration = 0

        # Initialize sprite image path or reference
        self.sprite_image = data["sprite_image"]

        # Initialize entity type (e.g., character, enemy)
        self.type = data["type"]

        # Initialize unique entity ID
        self.id = data["id"]
