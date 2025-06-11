from UI.screens.screen import Screen
from battle.battle_manager import BattleManager
import utility.data


class BattleScreen(Screen):
    def __init__(self, manager, info):
        super().__init__(manager)
        self.screen_id = 1  # Unique ID for the battle screen

        # Item buffs used in the current battle (HP, ATK, DEF)
        self.items = {
            "hp": info["items"]["HP"],
            "attack": info["items"]["Attack"],
            "defense": info["items"]["Defense"]
        }

        # Formation: convert character id to runtime format (id + 100) and attach selected skill
        self.formation = []
        for data in info["formation"]:
            self.formation.append({
                "id": data + 100,  # 100+ indicates battle-time ID
                "skill_id": utility.data.SKILL_SELECTED[data]  # Use selected skill based on elite level
            })

        # Initialize the battle manager with stage info, item buffs, formation, and a callback
        self.battle = BattleManager(
            utility.data.CURRENT_STAGE,
            self.items,
            self.formation,
            self.on_battle_end
        )

    def on_battle_end(self, result):
        # Callback function when battle ends
        if result == "win":
            # If player wins, proceed to result screen (screen_id 7)
            self.swift(7, {"stage": utility.data.CURRENT_STAGE, "progress": "end"})
        elif result == "lose":
            # If player loses, go to fail screen (screen_id 6)
            self.swift(6, "lose")

    def handle_event(self, screen, event):
        # Delegate input events to the battle manager
        self.battle.handle_event(screen, event)

    def update(self):
        # Update battle logic (AI, timers, actions, etc.)
        self.battle.update()

    def draw(self, screen):
        # Draw the current frame of the battle
        self.battle.draw(screen)

    def on_exit(self):
        # Clean up or reset battle reference when screen exits
        self.battle = None