from battle.AI.base_ai import BaseAI
import pygame

TILE_SIZE = 64


# class BossAI(StateMachine):
#     state1 = State("State1", initial=True)
#     state2 = State("State2")
#     to_state2 = state1.to(state2)
#
#     def __init__(self, entity):
#         StateMachine.__init__(self)
#         self.entity = entity
#         self.blocked = False
#         self.dead = False
#         self.controlled = False
#         self.last_skill_time = time.time()
#
#     def move(self):
#         print("Boss is moving.")
#
#     def attack(self, unit=None):
#         if unit:
#             unit.hp -= (self.entity.attack - unit.defense)
#
#     def skill_a(self):
#         print("Boss uses Skill A!")
#
#     def execute_state1(self):
#         if self.entity.hp <= 0:
#             self.dead = True
#             print("Boss has died.")
#             return
#         if self.entity.hp < 30:
#             print("Boss HP < 30, switching to State 2.")
#             self.to_state2()
#             return
#         if self.controlled:
#             print("Boss is controlled.")
#             return
#         if self.blocked:
#             self.attack()
#         else:
#             self.move()
#
#     def execute_state2(self):
#         if self.entity.hp <= 0:
#             self.dead = True
#             print("Boss has died.")
#             return
#         if self.controlled:
#             print("Boss is controlled.")
#             return
#         if self.blocked:
#             if time.time() - self.last_skill_time > 10:
#                 self.skill_a()
#                 self.last_skill_time = time.time()
#             else:
#                 self.attack()
#         else:
#             self.move()
#
#     def update(self):
#         if self.current_state == self.state1:
#             self.execute_state1()
#         elif self.current_state == self.state2:
#             self.execute_state2()


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
