from entities.entity import Entity
from utility.data import CHARACTER_DATA, SKILL_MAP


class CharacterFactory:

    @staticmethod
    def create_character_by_id(char_id: int, skill_id: int) -> Entity:
        # Create a character Entity instance based on character ID and selected skill ID

        if char_id not in CHARACTER_DATA:
            raise ValueError(f"Unknown character ID: {char_id}")  # Raise an error if character ID is invalid

        character = CHARACTER_DATA[char_id].copy()  # Copy base character data to avoid mutation

        skill_key = (char_id, skill_id)  # Tuple key to look up the skill configuration
        if skill_key in SKILL_MAP:
            cd, duration = SKILL_MAP[skill_key]  # Get cooldown and duration of the selected skill
            character["cd"] = cd  # Assign cooldown to character data
            character["duration"] = duration  # Assign skill duration
        else:
            # If no skill mapping is found, assign default values
            character["cd"] = 0
            character["duration"] = 0

        return Entity(character)  # Return a new Entity initialized with character data
