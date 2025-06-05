from battle.AI.base_ai import BaseAI
import pygame

TILE_SIZE = 64


class CharacterAI(BaseAI):
    def __init__(self, entity, timer, manager, tile_x, tile_y, skill_behavior):
        super().__init__(entity, timer, manager)
        self.tile_x = tile_x
        self.tile_y = tile_y
        self.cd = self.entity.cd
        self.duration = self.entity.duration
        self.skill_triggered = False
        self.skill_start_time = self.timer.time()
        self.skill_end_time = self.timer.time()
        self.position = pygame.Vector2(tile_x * TILE_SIZE, tile_y * TILE_SIZE)
        self.skill = skill_behavior

    @property
    def grid_pos(self):
        return self.tile_x, self.tile_y

    @property
    def in_cd(self):
        return self.timer.time() - self.skill_end_time

    def trigger_skill(self):
        self.skill_triggered = True
        self.skill.trigger_skill(self)
        self.skill_start_time = self.timer.time()

    def skill_attack(self, units):
        self.skill.skill_attack(self, units)

    def perform_attack(self, units):
        if self.timer.time() - self.skill_start_time > self.duration:
            self.skill_triggered = False
            self.skill_end_time = self.timer.time()
            self.skill.end_skill(self)
        if self.timer.time() - self.last_atk > self.atk_spd:
            if self.skill_triggered:
                if self.skill_attack(units):
                    self.last_atk = self.timer.time()
            else:
                target = self.search_enemy(units)
                if target is not None:
                    self.normal_attack(target)

    def update(self, units):
        self.is_blocked()
        if self.is_dead():
            return
        if self.is_controlled():
            return
        self.perform_attack(units)

    def draw(self, screen):
        if not self.dead:
            screen.blit(self.sprite, self.position)

            bar_width = 50
            bar_height = 5
            x = self.position.x
            y = self.position.y + self.sprite.get_height() + 2

            pygame.draw.rect(screen, (255, 0, 0), (x, y, bar_width, bar_height))

            hp_ratio = max(self.hp / self.entity.hp, 0)
            green_width = int(bar_width * hp_ratio)
            pygame.draw.rect(screen, (0, 255, 0), (x, y, green_width, bar_height))

            skill_y = y + bar_height + 2
            pygame.draw.rect(screen, (50, 50, 50), (x, skill_y, bar_width, bar_height))  # 灰底

            now = self.timer.time()

            if self.skill_triggered:
                elapsed = now - self.skill_start_time
                if self.duration > 0:
                    ratio = max(0, 1 - elapsed / self.duration)
                    width = int(bar_width * ratio)
                    pygame.draw.rect(screen, (255, 165, 0),
                                     (x + bar_width - width, skill_y, width, bar_height))

            elif now - self.skill_end_time < self.cd:
                cd_elapsed = now - self.skill_end_time
                if self.cd > 0:
                    ratio = min(cd_elapsed / self.cd, 1)
                    width = int(bar_width * ratio)
                    pygame.draw.rect(screen, (255, 255, 255), (x, skill_y, width, bar_height))
