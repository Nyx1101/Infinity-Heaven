from battle.timer import Timer
from battle.level.level_loader import LevelLoader
from battle.AI.enemy_ai import NormalAI, EliteAI1, EliteAI2, EliteAI3, BossAI
from entities.enemy import EnemyFactory
from entities.character import CharacterFactory
from battle.event_handler import EventHandler
from entities.modifier import Modifier
import utility.data
import pygame

TILE_SIZE = 64


class BattleManager:
    def __init__(self, level, selected_items, formation, on_finish_callback=None):
        """
        Initializes the battle manager for a specific level.

        Args:
            level (int): The current level identifier.
            selected_items (dict): Dictionary with keys 'hp', 'attack', 'defense' and integer values.
            formation (list): List of character placements including IDs and skill assignments.
            on_finish_callback (function, optional): Callback function to be called on win/lose.
        """
        self.on_finish = on_finish_callback
        self.modifier = Modifier(selected_items)  # Apply item-based stat modifiers
        self.loader = LevelLoader(level)  # Load level-specific data
        self.map = self.loader.load_map()  # Load map layout
        self.level_flow = self.loader.load_enemy()  # Load enemy spawn schedule
        self.enemy_factory = EnemyFactory(self.modifier)  # Factory for spawning enemies with modifiers
        self.character_factory = CharacterFactory()  # Factory for creating characters
        self.AIs = []  # List of all active AI units (characters and enemies)
        self.timer = Timer()
        self.resource = 10  # Initial deploy resource points
        self.event_handler = EventHandler(self)  # Handles user input and UI events
        self.units = []  # Units that can be deployed or have died
        self.formation = formation

        # Create initial character units from the provided formation
        for data in self.formation:
            char_id = data["id"]
            character_entity = CharacterFactory.create_character_by_id(char_id, data["skill_id"])
            unit_info = {
                "entity": character_entity,
                "death_time": None  # Initially alive
            }
            self.units.append(unit_info)

        self.start_time = self.timer.time()
        self.dragging_unit = None  # Currently dragged unit
        self.drag_offset = pygame.Vector2(0, 0)  # Offset when dragging unit
        self.selected_unit_ai = None  # Selected unit in the UI
        self.paused = False  # Game pause state

        # UI elements
        self.pause_button_rect = pygame.Rect(0, 8 * TILE_SIZE - 64, 64, 64)
        self.cost_icon_rect = pygame.Rect(64, 8 * TILE_SIZE - 64, 64, 64)
        self.pause_icon = pygame.transform.scale(pygame.image.load("assets/image/pause.png"), (64, 64))
        self.start_icon = pygame.transform.scale(pygame.image.load("assets/image/start.png"), (64, 64))
        self.cost_icon = pygame.transform.scale(pygame.image.load("assets/image/cost.png"), (64, 64))
        self.last_update_time = self.timer.time()

    def get_all_characters(self):
        """Returns a list of all currently active characters."""
        return [ai for ai in self.AIs if ai.entity.type == 1 or ai.entity.type == 2]

    def get_all_enemies(self):
        """Returns a list of all currently active enemies."""
        return [ai for ai in self.AIs if ai.entity.type == 0]

    def draw_characters_in_corner(self, screen):
        """
        Draws character portraits in the lower-right corner with redeployment cooldown overlays and cost.

        Args:
            screen (pygame.Surface): The game screen to draw on.
        """
        spacing = 0
        sprite_size = 64
        bottom_offset = 0
        right_offset = 0
        font = pygame.font.SysFont(None, 20)

        for i, unit in enumerate(reversed(self.units)):
            entity = unit["entity"]
            sprite_raw = pygame.image.load(entity.sprite_image).convert_alpha()
            sprite = pygame.transform.scale(sprite_raw, (64, 64))
            x = screen.get_width() - right_offset - (sprite_size + spacing) * (i + 1)
            y = screen.get_height() - sprite_size - bottom_offset

            screen.blit(sprite, (x, y))

            death_time = unit["death_time"]
            redeploy_time = entity.redeployment_time

            if death_time is not None:
                elapsed = self.timer.time() - death_time
                progress = min(elapsed / redeploy_time, 1.0)

                overlay = pygame.Surface((sprite_size, sprite_size), pygame.SRCALPHA)
                grayness = max(0, min(255, int((1.0 - progress) * 180)))
                overlay.fill((50, 50, 50, grayness))
                screen.blit(overlay, (x, y))

                if progress < 1.0:
                    cooldown_height = int((1.0 - progress) * sprite_size)
                    cooldown_bar = pygame.Surface((sprite_size, cooldown_height), pygame.SRCALPHA)
                    cooldown_bar.fill((0, 0, 0, 120))
                    screen.blit(cooldown_bar, (x, y))

            cost = entity.cost
            color = (0, 255, 0) if cost <= self.resource else (255, 0, 0)
            cost_text = font.render(f"{cost}", True, color)
            cost_text_rect = cost_text.get_rect(center=(x + sprite_size // 2, y + sprite_size - 10))
            screen.blit(cost_text, cost_text_rect)

    def handle_event(self, screen, event):
        """Delegates event handling to the EventHandler."""
        self.event_handler.handle_event(screen, event)

    def update(self):
        """
        Main update loop for the battle logic.
        Handles enemy spawning, unit AI updates, and win/loss conditions.
        """
        if self.paused:
            return

        # Resource regeneration
        self.resource = min(self.resource + (self.timer.time() - self.last_update_time), 99)
        self.last_update_time = self.timer.time()
        current_time = self.timer.time() - self.start_time
        result = self.level_flow.pop_next_if_due(current_time)

        # Spawn new enemy if needed
        if result:
            new_enemy = self.enemy_factory.create_enemy_by_id(result["id"])
            if result["id"] == 205:
                ai = EliteAI1(new_enemy, self.timer, self, result["path"])
            elif result["id"] == 208:
                ai = EliteAI2(new_enemy, self.timer, self, result["path"])
            elif result["id"] == 207:
                ai = EliteAI3(new_enemy, self.timer, self, result["path"])
            elif result["id"] == 209:
                ai = BossAI(new_enemy, self.timer, self, result["path"])
            else:
                ai = NormalAI(new_enemy, self.timer, self, result["path"])
            self.AIs.append(ai)

        # Update enemies
        for AI in self.get_all_enemies():
            AI.update(self.get_all_characters())
            if AI.dead:
                self.AIs.remove(AI)
            if AI.score:  # Player lost
                if self.on_finish:
                    self.on_finish(result="lose")

        # Update characters
        for AI in self.get_all_characters():
            if AI.entity.type == 2:  # Support unit?
                AI.update(self.get_all_characters())
            else:
                AI.update(self.get_all_enemies())
            if AI.dead:
                unit_info = {
                    "entity": AI.entity,
                    "death_time": self.timer.time()
                }
                self.units.append(unit_info)
                self.AIs.remove(AI)

        # Check win condition
        if not self.level_flow.has_remaining() and not self.get_all_enemies():
            stage_idx = utility.data.CURRENT_STAGE - 1
            if self.modifier.atk_multiplier == 1:
                if utility.data.LEVEL_PROGRESS[stage_idx] < 1:
                    utility.data.LEVEL_PROGRESS[stage_idx] = 1
            elif self.modifier.atk_multiplier == 1.1:
                if utility.data.LEVEL_PROGRESS[stage_idx] < 2:
                    utility.data.LEVEL_PROGRESS[stage_idx] = 2
                    utility.data.ELITE_BADGE[0] += 1
            else:
                if utility.data.LEVEL_PROGRESS[stage_idx] <= 1:
                    utility.data.ELITE_BADGE[0] += 1
                    utility.data.ELITE_BADGE[1] += 1
                elif utility.data.LEVEL_PROGRESS[stage_idx] == 2:
                    utility.data.ELITE_BADGE[1] += 1
                utility.data.LEVEL_PROGRESS[stage_idx] = 3

            self.on_finish(result="win")

    def draw(self, screen):
        """
        Draws the full battle scene, including the map, units, UI, and overlays.

        Args:
            screen (pygame.Surface): The game screen to draw on.
        """
        self.map.draw(screen)
        self.draw_characters_in_corner(screen)

        for AI in self.AIs:
            AI.draw(screen)

        self.event_handler.draw_selected_unit_ui(screen)

        if self.dragging_unit:
            mouse_pos = pygame.mouse.get_pos()
            pos = pygame.Vector2(mouse_pos) - self.drag_offset
            sprite_raw = pygame.image.load(self.dragging_unit.sprite_image).convert_alpha()
            sprite = pygame.transform.scale(sprite_raw, (64, 64))
            screen.blit(sprite, pos)

        # Draw pause/start icon and cost icon
        screen.blit(self.start_icon if self.paused else self.pause_icon, self.pause_button_rect.topleft)
        screen.blit(self.cost_icon, self.cost_icon_rect.topleft)

        # Draw current resource count
        font = pygame.font.SysFont(None, 24)
        resource_text = font.render(str(int(self.resource)), True, (255, 255, 255))
        text_rect = resource_text.get_rect(center=(self.cost_icon_rect.centerx, self.cost_icon_rect.bottom - 10))
        screen.blit(resource_text, text_rect)

        self.event_handler.draw_dragged_unit_range(screen)

        # If paused, draw transparent overlay
        if self.paused:
            overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))
            screen.blit(overlay, (0, 0))
