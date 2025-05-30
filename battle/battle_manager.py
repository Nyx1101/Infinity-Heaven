import time
from battle.level.level_loader import LevelLoader
from battle.AI.normal_ai import NormalAI
from entities.enemy import EnemyFactory
from entities.character import CharacterFactory
from battle.AI.elite_ai import CharacterAI
import pygame

TILE_SIZE = 64


class BattleManager:
    def __init__(self):
        self.loader = LevelLoader()
        self.map = self.loader.load_level_1_map()
        self.level_flow = self.loader.load_level_1_enemy()
        self.enemy_factory = EnemyFactory()
        self.character_factory = CharacterFactory()
        self.AIs = []
        self.units = []
        formation = self.loader.load_character()
        for data in formation:
            char_id = data["id"]
            character_entity = CharacterFactory.create_character_by_id(char_id)
            self.units.append(character_entity)
        self.start_time = time.time()
        self.dragging_unit = None
        self.drag_offset = pygame.Vector2(0, 0)

    def get_all_characters(self):
        return [ai for ai in self.AIs if ai.entity.type == 1]

    def get_all_enemies(self):
        return [ai for ai in self.AIs if ai.entity.type == 0]

    def draw_characters_in_corner(self, screen):
        spacing = 0
        sprite_size = 64
        bottom_offset = 0
        right_offset = 0

        for i, unit in enumerate(reversed(self.units)):  # 从右到左排列
            sprite = pygame.image.load(unit.sprite_image).convert_alpha()
            x = screen.get_width() - right_offset - (sprite_size + spacing) * (i + 1)
            y = screen.get_height() - sprite_size - bottom_offset
            screen.blit(sprite, (x, y))

    def handle_event(self, screen, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            # 检查是否点击到了右下角展示的角色图标（从右到左）
            for i, unit in enumerate(reversed(self.units)):
                sprite = pygame.image.load(unit.sprite_image).convert_alpha()
                sprite_rect = sprite.get_rect()
                x = screen.get_width() - 0 - (64 + 0) * (i + 1)
                y = screen.get_height() - 64 - 0
                sprite_rect.topleft = (x, y)

                if sprite_rect.collidepoint(mouse_pos):
                    self.dragging_unit = unit
                    self.drag_offset = pygame.Vector2(mouse_pos) - pygame.Vector2(x, y)
                    break

        elif event.type == pygame.MOUSEBUTTONUP:
            if self.dragging_unit:
                mouse_pos = pygame.mouse.get_pos()
                tile_x = mouse_pos[0] // TILE_SIZE
                tile_y = mouse_pos[1] // TILE_SIZE

                if 0 <= tile_y < len(self.map.layout) and 0 <= tile_x < len(self.map.layout[0]):
                    tile_value = self.map.layout[tile_y][tile_x]
                    if tile_value in (0, 2):
                        # 允许部署：更新单位位置
                        self.dragging_unit.position = pygame.Vector2(
                            tile_x * TILE_SIZE,
                            tile_y * TILE_SIZE
                        )
                        new_unit = self.character_factory.create_character_by_id(self.dragging_unit.id)
                        ai = CharacterAI(new_unit, tile_x, tile_y)
                        self.AIs.append(ai)
                        self.units.remove(self.dragging_unit)
                    else:
                        pass

            self.dragging_unit = None


    def update(self):
        current_time = time.time()-self.start_time
        result = self.level_flow.pop_next_if_due(current_time)

        if result:
            new_enemy = self.enemy_factory.create_enemy_by_id(result["id"])
            ai = NormalAI(new_enemy, result["path"])
            self.AIs.append(ai)

        for AI in self.get_all_enemies():
            AI.update(self.get_all_characters())
            if AI.dead:
                self.AIs.remove(AI)
            if AI.score:
                self.AIs.remove(AI)

        for AI in self.get_all_characters():
            AI.update()
            if AI.dead:
                self.AIs.remove(AI)

    def draw(self, screen):
        self.map.draw(screen)
        self.draw_characters_in_corner(screen)
        for AI in self.AIs:
            AI.draw(screen)
        if self.dragging_unit:
            mouse_pos = pygame.mouse.get_pos()
            pos = pygame.Vector2(mouse_pos) - self.drag_offset
            sprite = pygame.image.load(self.dragging_unit.sprite_image).convert_alpha()
            screen.blit(sprite, pos)
