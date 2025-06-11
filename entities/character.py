from entities.entity import Entity
from utility.data import CHARACTER_DATA, SKILL_MAP


class CharacterFactory:

    @staticmethod
    def create_character_by_id(char_id: int, skill_id: int) -> Entity:
        if char_id not in CHARACTER_DATA:
            raise ValueError(f"Unknown character ID: {char_id}")

        character = CHARACTER_DATA[char_id].copy()

        skill_key = (char_id, skill_id)
        if skill_key in SKILL_MAP:
            cd, duration = SKILL_MAP[skill_key]
            character["cd"] = cd
            character["duration"] = duration
        else:
            character["cd"] = 0
            character["duration"] = 0

        return Entity(character)
