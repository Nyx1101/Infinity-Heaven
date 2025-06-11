import pygame
from battle.AI.character_ai import CharacterAI
from entities.skill import SkillFactory
import utility.data
TILE_SIZE = 64


class EventHandler:
    def __init__(self, battle_manager):
        self.battle = battle_manager

    def draw_selected_unit_ui(self, screen):
        if self.battle.selected_unit_ai:
            unit = self.battle.selected_unit_ai
            ux, uy = int(unit.position.x), int(unit.position.y)

            if unit.range > 0:
                center = (ux + TILE_SIZE // 2, uy + TILE_SIZE // 2)
                radius = unit.range * TILE_SIZE
                pygame.draw.circle(screen, (255, 0, 0), center, radius, 1)  # 红色圆圈，线宽为1像素

            font = pygame.font.SysFont(None, 20)
            retreat_text = font.render("Retreat", True, (255, 255, 255))
            screen.blit(retreat_text, (ux + TILE_SIZE, uy + TILE_SIZE))

            if hasattr(unit, "skill"):
                if unit.skill is not None:
                    icon_path = unit.skill.icon
                    icon_image = pygame.image.load(icon_path).convert_alpha()
                    icon_size = (32, 32)
                    icon_image = pygame.transform.smoothscale(icon_image, icon_size)
                    screen.blit(icon_image, (ux + TILE_SIZE, uy))

    def draw_dragged_unit_range(self, screen):
        if self.battle.dragging_unit and self.battle.dragging_unit.range > 0:
            mouse_pos = pygame.mouse.get_pos()
            drag_offset = self.battle.drag_offset
            x = mouse_pos[0] - drag_offset.x
            y = mouse_pos[1] - drag_offset.y

            center = (int(x + TILE_SIZE // 2), int(y + TILE_SIZE // 2))
            radius = self.battle.dragging_unit.range * TILE_SIZE
            pygame.draw.circle(screen, (0, 255, 0), center, radius, 1)  # 绿色圆圈

    def handle_deploy_click(self, screen, mouse_pos):
        for i, unit in enumerate(reversed(self.battle.units)):
            death_time = unit["death_time"]
            redeploy_time = unit["entity"].redeployment_time
            if unit["entity"].cost > self.battle.resource:
                continue
            if death_time is not None:
                elapsed = self.battle.timer.time() - death_time
                if elapsed < redeploy_time:
                    continue

            sprite = pygame.image.load(unit["entity"].sprite_image).convert_alpha()
            sprite_rect = sprite.get_rect()
            x = screen.get_width() - (64 + 0) * (i + 1)
            y = screen.get_height() - 64
            sprite_rect.topleft = (x, y)

            if sprite_rect.collidepoint(mouse_pos):
                self.battle.dragging_unit = unit["entity"]
                self.battle.drag_offset = pygame.Vector2(mouse_pos) - pygame.Vector2(x, y)
                return True
        return False

    def handle_character_selection(self, mouse_pos):
        tile_x = mouse_pos[0] // TILE_SIZE
        tile_y = mouse_pos[1] // TILE_SIZE
        self.battle.selected_unit_ai = None

        for ai in self.battle.AIs:
            unit_x = int(ai.position.x) // TILE_SIZE
            unit_y = int(ai.position.y) // TILE_SIZE
            if unit_x == tile_x and unit_y == tile_y:
                self.battle.selected_unit_ai = ai
                break

    def handle_unit_buttons(self, mouse_pos):
        if not self.battle.selected_unit_ai:
            return

        ux, uy = int(self.battle.selected_unit_ai.position.x), int(self.battle.selected_unit_ai.position.y)

        retreat_rect = pygame.Rect(ux + TILE_SIZE, uy + TILE_SIZE, 50, 20)
        skill_rect = pygame.Rect(ux + TILE_SIZE, uy, 50, 20)

        if retreat_rect.collidepoint(mouse_pos):
            self.battle.selected_unit_ai.dead = True
            self.battle.selected_unit_ai.is_dead()
            self.battle.selected_unit_ai.death_time = self.battle.timer.time()
            self.battle.selected_unit_ai = None
            return

        elif skill_rect.collidepoint(mouse_pos):
            if self.battle.selected_unit_ai.skill is not None:
                if self.battle.selected_unit_ai.in_cd > self.battle.selected_unit_ai.cd:
                    self.battle.selected_unit_ai.trigger_skill()
                    return

    def handle_unit_placement(self, mouse_pos):
        if not self.battle.dragging_unit:
            return

        tile_x = mouse_pos[0] // TILE_SIZE
        tile_y = mouse_pos[1] // TILE_SIZE

        if 0 <= tile_y < len(self.battle.map.layout) and 0 <= tile_x < len(self.battle.map.layout[0]):
            tile_value = self.battle.map.layout[tile_y][tile_x]

            for ai in self.battle.get_all_characters():
                if ai.tile_x == tile_x and ai.tile_y == tile_y:
                    self.battle.dragging_unit = None
                    return

            if tile_value in (0, 2) and self.battle.dragging_unit.cost < self.battle.resource:
                self.battle.resource -= self.battle.dragging_unit.cost
                self.battle.dragging_unit.position = pygame.Vector2(tile_x * TILE_SIZE, tile_y * TILE_SIZE)
                new_unit = None
                skill_behavior = None
                for formation_data in self.battle.formation:
                    if formation_data["id"] == self.battle.dragging_unit.id:
                        skill_id = formation_data["skill_id"] + formation_data["id"] * 2 - 200
                        new_unit = self.battle.character_factory.create_character_by_id(
                            self.battle.dragging_unit.id, formation_data["skill_id"]
                        )
                        skill_behavior = SkillFactory.get_behavior(skill_id)
                        if formation_data["skill_id"] == 0:
                            skill_behavior = None
                        break
                ai = CharacterAI(new_unit, self.battle.timer, self.battle, tile_x, tile_y, skill_behavior)
                self.battle.AIs.append(ai)

                for unit in self.battle.units:
                    if unit["entity"] == self.battle.dragging_unit:
                        self.battle.units.remove(unit)
                        break

        self.battle.dragging_unit = None

    def handle_event(self, screen, event):
        mouse_pos = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.battle.pause_button_rect.collidepoint(mouse_pos):
                if not self.battle.paused:
                    self.battle.timer.pause()
                    self.battle.paused = True
                else:
                    self.battle.timer.resume()
                    self.battle.paused = False

        if self.battle.paused:
            return

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.handle_deploy_click(screen, mouse_pos):
                return
            if self.battle.selected_unit_ai:
                self.handle_unit_buttons(mouse_pos)
                self.battle.selected_unit_ai = None
            else:
                self.handle_character_selection(mouse_pos)

        elif event.type == pygame.MOUSEBUTTONUP:
            self.handle_unit_placement(mouse_pos)
