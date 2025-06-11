from entities.entity import Entity
import utility.data


class EnemyFactory:
    def __init__(self, modifier):
        self.modifier = modifier
        self.enemy_map = {
            data["id"]: data for data in utility.data.ENEMY_DATA.values()
        }

    def create_enemy_by_id(self, enemy_id: str) -> Entity:
        if enemy_id in self.enemy_map:
            base_data = self.enemy_map[enemy_id].copy()
            modified_data = self.modifier.apply(base_data)
            return Entity(modified_data)
