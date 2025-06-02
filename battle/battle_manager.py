from battle.timer import Timer
from battle.level.level_loader import LevelLoader
from battle.AI.normal_ai import NormalAI
from entities.enemy import EnemyFactory
from entities.character import CharacterFactory
from battle.AI.elite_ai import CharacterAI
from battle.event_handler import EventHandler
from entities.modifier import Modifier
import pygame

TILE_SIZE = 64


class BattleManager:
    def __init__(self, level, selected_items, formation):
        self.modifier = Modifier(selected_items)
        self.loader = LevelLoader(level)
        self.map = self.loader.load_level_1_map()
        self.level_flow = self.loader.load_enemy()
        self.enemy_factory = EnemyFactory(self.modifier)
        self.character_factory = CharacterFactory()
        self.AIs = []
        self.timer = Timer()
        self.resource = 10
        self.event_handler = EventHandler(self)
        self.units = []
        self.formation = formation
        for data in self.formation:
            char_id = data["id"]
            character_entity = CharacterFactory.create_character_by_id(char_id, data["skill_id"], data["artefact_id"])
            unit_info = {
                "entity": character_entity,
                "death_time": None
            }
            self.units.append(unit_info)
        self.start_time = self.timer.time()
        self.dragging_unit = None
        self.drag_offset = pygame.Vector2(0, 0)
        self.selected_unit_ai = None

    def get_all_characters(self):
        return [ai for ai in self.AIs if ai.entity.type == 1 or ai.entity.type == 2]

    def get_all_enemies(self):
        return [ai for ai in self.AIs if ai.entity.type == 0]

    def draw_characters_in_corner(self, screen):
        spacing = 0
        sprite_size = 64
        bottom_offset = 0
        right_offset = 0

        current_time = self.timer.time()

        for i, unit in enumerate(reversed(self.units)):
            sprite = pygame.image.load(unit["entity"].sprite_image).convert_alpha()
            x = screen.get_width() - right_offset - (sprite_size + spacing) * (i + 1)
            y = screen.get_height() - sprite_size - bottom_offset

            screen.blit(sprite, (x, y))

            death_time = unit["death_time"]
            redeploy_time = unit["entity"].redeployment_time

            if death_time is not None:
                elapsed = current_time - death_time
                progress = min(elapsed / redeploy_time, 1.0)

                overlay = pygame.Surface((sprite_size, sprite_size), pygame.SRCALPHA)
                grayness = int((1.0 - progress) * 180)
                overlay.fill((50, 50, 50, grayness))
                screen.blit(overlay, (x, y))

                if progress < 1.0:
                    cooldown_height = int((1.0 - progress) * sprite_size)
                    cooldown_bar = pygame.Surface((sprite_size, cooldown_height), pygame.SRCALPHA)
                    cooldown_bar.fill((0, 0, 0, 120))
                    screen.blit(cooldown_bar, (x, y))

    def handle_event(self, screen, event):
        self.event_handler.handle_event(screen, event)

    def update(self):
        self.resource = min(self.resource + 1 / 60, 99)
        current_time = self.timer.time()-self.start_time
        result = self.level_flow.pop_next_if_due(current_time)

        if result:
            new_enemy = self.enemy_factory.create_enemy_by_id(result["id"])
            ai = NormalAI(new_enemy, self.timer, result["path"])
            self.AIs.append(ai)

        for AI in self.get_all_enemies():
            AI.update(self.get_all_characters())
            if AI.dead:
                self.AIs.remove(AI)
            if AI.score:
                self.AIs.remove(AI)

        for AI in self.get_all_characters():
            if AI.entity.type == 2:
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

    def draw(self, screen):
        self.map.draw(screen)
        self.draw_characters_in_corner(screen)
        self.event_handler.draw_selected_unit_ui(screen)
        for AI in self.AIs:
            AI.draw(screen)
        if self.dragging_unit:
            mouse_pos = pygame.mouse.get_pos()
            pos = pygame.Vector2(mouse_pos) - self.drag_offset
            sprite = pygame.image.load(self.dragging_unit.sprite_image).convert_alpha()
            screen.blit(sprite, pos)
