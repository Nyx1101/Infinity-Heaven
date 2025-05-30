import time
import pygame
from statemachine import StateMachine, State

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


class CharacterAI(StateMachine):
    normal = State("Normal", initial=True)
    using_skill = State("UsingSkill")
    to_skill = normal.to(using_skill)
    to_normal = using_skill.to(normal)

    def __init__(self, entity, tile_x, tile_y):
        StateMachine.__init__(self)
        self.entity = entity
        self.hp = self.entity.hp
        self.atk = self.entity.atk
        self.dfs = self.entity.defense
        self.res = self.entity.resistance
        self.atk_spd = self.entity.attack_speed
        self.atk_type = self.entity.atk_type
        self.controlled = False
        self.blocked = False
        self.blocker = []
        self.sprite = pygame.image.load(entity.sprite_image).convert_alpha()
        self.dead = False
        self.tile_x = tile_x
        self.tile_y = tile_y
        self.last_atk = time.time()
        self.skill_triggered = False
        self.skill_start_time = None
        self.skill_duration = 3
        self.sprite = pygame.image.load(entity.sprite_image).convert_alpha()
        self.position = pygame.Vector2(tile_x * TILE_SIZE, tile_y * TILE_SIZE)

    @property
    def grid_pos(self):
        return self.tile_x, self.tile_y

    def normal_attack(self, unit):
        if not unit:
            return
        if self.atk_type == 0:
            unit.hp -= (self.atk - unit.dfs)
        elif self.atk_type == 1:
            unit.hp -= (self.atk * (1 - unit.res / 100))

    def skill_attack(self):
        pass

    def has_enemy_in_range(self):
        pass

    def execute_normal(self):
        if self.hp <= 0:
            self.dead = True
            return

        if self.controlled:
            return

        if self.blocked:
            if time.time() - self.last_atk > self.atk_spd:
                self.last_atk = time.time()
                self.normal_attack(self.blocker)
                return
            else:
                return

    def execute_using_skill(self):
        if time.time() - self.skill_start_time > self.skill_duration:
            print("Skill finished.")
            self.to_normal()
            self.skill_triggered = False
            return
        if self.controlled:
            print("Character is controlled during skill.")
            return
        if self.has_enemy_in_range():
            self.skill_attack()
        else:
            print("Waiting during skill.")

    def update(self):
        if self.current_state == self.normal:
            self.execute_normal()
        elif self.current_state == self.using_skill:
            self.execute_using_skill()

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
