from entities.entity import Entity
import utility.data


class EnemyFactory:
    def __init__(self, modifier):
        self.modifier = modifier  # A stat modifier applied to enemy attributes (e.g., based on stage difficulty)

        # Create a lookup map for enemy base data using their ID as the key
        self.enemy_map = {
            data["id"]: data for data in utility.data.ENEMY_DATA.values()
        }

    def create_enemy_by_id(self, enemy_id: str) -> Entity:
        # Create an enemy Entity instance based on its ID

        if enemy_id in self.enemy_map:
            base_data = self.enemy_map[enemy_id].copy()  # Copy base enemy data to avoid mutation
            modified_data = self.modifier.apply(base_data)  # Apply stage or difficulty modifiers
            return Entity(modified_data)  # Return a new Entity initialized with modified data
