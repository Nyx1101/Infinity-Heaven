class Modifier:
    def __init__(self, selected_items):
        # Initialize multipliers for HP, attack, and defense to 1 (no modification)
        self.hp_multiplier = 1.0
        self.atk_multiplier = 1.0
        self.def_multiplier = 1.0

        # Apply initial modifications based on the selected items
        self.modify(selected_items)

    def modify(self, items):
        # Update the multipliers by multiplying with corresponding item values
        self.hp_multiplier *= items["hp"]
        self.atk_multiplier *= items["attack"]
        self.def_multiplier *= items["defense"]

    def apply(self, data: dict):
        # Apply the multipliers to the input data dictionary (modifying stats)
        data["hp"] *= self.hp_multiplier
        data["atk"] *= self.atk_multiplier
        data["defense"] *= self.def_multiplier

        # Return the modified data dictionary
        return data