from entities.entity import Entity
from entities.artefact import Artefact
from utility.data import CHARACTER_DATA


class CharacterFactory:
    SKILL_MAP = {
        ("100", 1): (30, 20),
        ("101", 1): (20, 20),
        ("102", 1): (25, 15),
    }

    @staticmethod
    def create_character_by_id(char_id: str, skill_id: int, artefact_id: str) -> Entity:
        if char_id not in CHARACTER_DATA:
            raise ValueError(f"Unknown character ID: {char_id}")

        character = CHARACTER_DATA[char_id].copy()

        skill_key = (char_id, skill_id)
        if skill_key in CharacterFactory.SKILL_MAP:
            cd, duration = CharacterFactory.SKILL_MAP[skill_key]
            character["cd"] = cd
            character["duration"] = duration
        else:
            character["cd"] = 0
            character["duration"] = 0

        Artefact(artefact_id).apply(character)

        return Entity(character)
