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
        self.on_finish = on_finish_callback
        self.modifier = Modifier(selected_items)
        self.loader = LevelLoader(level)
        self.map = self.loader.load_map()
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
            character_entity = CharacterFactory.create_character_by_id(char_id, data["skill_id"])
            unit_info = {
                "entity": character_entity,
                "death_time": None
            }
            self.units.append(unit_info)
        self.start_time = self.timer.time()
        self.dragging_unit = None
        self.drag_offset = pygame.Vector2(0, 0)
        self.selected_unit_ai = None
        self.paused = False
        self.pause_button_rect = pygame.Rect(0, 8 * TILE_SIZE - 64, 64, 64)
        self.cost_icon_rect = pygame.Rect(64, 8 * TILE_SIZE - 64, 64, 64)
        self.pause_icon = pygame.transform.scale(pygame.image.load("assets/image/pause.png"), (64, 64))
        self.start_icon = pygame.transform.scale(pygame.image.load("assets/image/start.png"), (64, 64))
        self.cost_icon = pygame.transform.scale(pygame.image.load("assets/image/cost.png"), (64, 64))
        self.last_update_time = self.timer.time()

    def get_all_characters(self):
        return [ai for ai in self.AIs if ai.entity.type == 1 or ai.entity.type == 2]

    def get_all_enemies(self):
        return [ai for ai in self.AIs if ai.entity.type == 0]

    def draw_characters_in_corner(self, screen):
        spacing = 0
        sprite_size = 64
        bottom_offset = 0
        right_offset = 0

        font = pygame.font.SysFont(None, 20)  # 添加字体对象

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
        self.event_handler.handle_event(screen, event)

    def update(self):
        if self.paused:
            return
        self.resource = min(self.resource + (self.timer.time() - self.last_update_time), 99)
        self.last_update_time = self.timer.time()
        current_time = self.timer.time()-self.start_time
        result = self.level_flow.pop_next_if_due(current_time)

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

        for AI in self.get_all_enemies():
            AI.update(self.get_all_characters())
            if AI.dead:
                self.AIs.remove(AI)
            if AI.score:
                if self.on_finish:
                    self.on_finish(result="lose")

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

        if not self.level_flow.has_remaining() and not self.get_all_enemies():
            if self.modifier.atk_multiplier == 1:
                if utility.data.LEVEL_PROGRESS[utility.data.CURRENT_STAGE - 1] < 1:
                    utility.data.LEVEL_PROGRESS[utility.data.CURRENT_STAGE - 1] = 1
            elif self.modifier.atk_multiplier == 1.1:
                if utility.data.LEVEL_PROGRESS[utility.data.CURRENT_STAGE - 1] < 2:
                    utility.data.LEVEL_PROGRESS[utility.data.CURRENT_STAGE - 1] = 2
                    utility.data.ELITE_BADGE[0] += 1
            else:
                if utility.data.LEVEL_PROGRESS[utility.data.CURRENT_STAGE - 1] <= 1:
                    utility.data.ELITE_BADGE[0] += 1
                    utility.data.ELITE_BADGE[1] += 1
                elif utility.data.LEVEL_PROGRESS[utility.data.CURRENT_STAGE - 1] == 2:
                    utility.data.ELITE_BADGE[1] += 1
                utility.data.LEVEL_PROGRESS[utility.data.CURRENT_STAGE - 1] = 3
            self.on_finish(result="win")

    def draw(self, screen):

        self.map.draw(screen)
        self.draw_characters_in_corner(screen)
        self.event_handler.draw_selected_unit_ui(screen)
        for AI in self.AIs:
            AI.draw(screen)
        if self.dragging_unit:
            mouse_pos = pygame.mouse.get_pos()
            pos = pygame.Vector2(mouse_pos) - self.drag_offset
            sprite_raw = pygame.image.load(self.dragging_unit.sprite_image).convert_alpha()
            sprite = pygame.transform.scale(sprite_raw, (64, 64))
            screen.blit(sprite, pos)

        screen.blit(self.start_icon if self.paused else self.pause_icon, self.pause_button_rect.topleft)
        screen.blit(self.cost_icon, self.cost_icon_rect.topleft)

        font = pygame.font.SysFont(None, 24)
        resource_text = font.render(str(int(self.resource)), True, (255, 255, 255))
        text_rect = resource_text.get_rect(center=(self.cost_icon_rect.centerx, self.cost_icon_rect.bottom - 10))
        screen.blit(resource_text, text_rect)
        self.event_handler.draw_dragged_unit_range(screen)

        if self.paused:
            overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))
            screen.blit(overlay, (0, 0))
