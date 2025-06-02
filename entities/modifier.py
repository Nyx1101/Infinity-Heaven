class Modifier:
    def __init__(self, selected_items):
        self.hp_multiplier = 1.0
        self.atk_multiplier = 1.0
        self.def_multiplier = 1.0
        self.modify(selected_items)

    def modify(self, items):
        self.hp_multiplier *= items["hp"]
        self.atk_multiplier *= items["attack"]
        self.def_multiplier *= items["defense"]

    def apply(self, data: dict):
        data["hp"] *= self.hp_multiplier
        data["atk"] *= self.atk_multiplier
        data["defense"] *= self.def_multiplier
        return data
