import pygame
from entities.entity import Entity
import os

TILE_SIZE = 64


class BaseAI:
    def __init__(self, entity: Entity, timer, manager):
        self.entity = entity
        self.manager = manager
        self.hp = self.entity.hp
        self.atk = self.entity.atk
        self.dfs = self.entity.defense
        self.res = self.entity.resistance
        self.atk_spd = self.entity.attack_speed
        self.atk_type = self.entity.atk_type
        self.range = self.entity.range
        self.timer = timer

        # 状态初始化
        self.controlled = False
        self.controlled_time = None
        self.control_duration = 0
        self.blocked = False
        self.blocker = []
        self.dead = False
        self.last_atk = self.timer.time()
        self.position = None

        # 预加载攻击动画帧
        self.attack_frames = self.load_attack_animation(f"assets/animation/{self.entity.id}")
        self.sprite = self.attack_frames[0]
        self.attack_anim_fps = 12
        self.attack_anim_start_time = 0
        self.attack_frame_index = 0
        self.playing_attack_anim = False

    def load_attack_animation(self, folder):
        frames = []
        if not os.path.exists(folder):
            return frames
        files = os.listdir(folder)
        png_files = [f for f in files if f.endswith(".png")]

        entity_id = self.entity.id

        if 100 <= entity_id <= 108:
            # 使用 attack_0.png 到 attack_x.png，按 _ 后数字排序
            attack_files = [f for f in png_files if f.startswith("attack_")]
            attack_files.sort(key=lambda name: int(name.split("_")[1].split(".")[0]))

        elif 200 <= entity_id <= 209:
            # 只提取 .png 前的最后两位数字排序
            attack_files = []
            for f in png_files:
                base = os.path.splitext(f)[0]
                if len(base) >= 2 and base[-2:].isdigit():
                    attack_files.append(f)
            attack_files.sort(key=lambda name: int(os.path.splitext(name)[0][-2:]))

        else:
            # 默认行为：尝试使用 attack_0.png 命名规则
            attack_files = [f for f in png_files if f.startswith("attack_")]
            attack_files.sort(key=lambda name: int(name.split("_")[1].split(".")[0]))

        for file in attack_files:
            path = os.path.join(folder, file)
            try:
                img = pygame.image.load(path).convert_alpha()
                img = pygame.transform.smoothscale(img, (TILE_SIZE, TILE_SIZE))
                frames.append(img)
            except Exception as e:
                print(f"Failed to load {path}: {e}")

        return frames

    def start_attack_animation(self):
        self.playing_attack_anim = True
        self.attack_anim_start_time = self.timer.time()
        self.attack_frame_index = 0

    def update_attack_animation(self):
        if not self.playing_attack_anim:
            return

        elapsed = self.timer.time() - self.attack_anim_start_time
        frame_duration = 1 / self.attack_anim_fps
        self.attack_frame_index = int(elapsed / frame_duration)

        if self.attack_frame_index >= len(self.attack_frames):
            self.playing_attack_anim = False
            self.attack_frame_index = 0

    def normal_attack(self, unit):
        if not unit:
            self.last_atk = self.timer.time()
            self.start_attack_animation()
            return None
        if self.atk_type == 0:  # Physical
            damage = max(self.atk - unit.dfs, self.atk * 0.1)
            unit.hp -= damage
        elif self.atk_type == 1:  # Magical
            damage = max(self.atk * (1 - unit.res / 100), self.atk * 0.1)
            unit.hp -= damage
        else:  # Healing
            unit.hp += self.atk
            unit.hp = min(unit.hp, unit.entity.hp)
            damage = None
        self.last_atk = self.timer.time()
        self.start_attack_animation()
        return damage

    def is_dead(self):
        if self.hp <= 0 or self.dead:
            self.dead = True
            for blocker in self.blocker:
                if self in blocker.blocker:
                    blocker.blocker.remove(self)
            return True

    def be_controlled(self, time):
        self.controlled = True
        self.control_duration = time
        self.controlled_time = self.timer.time()

    def is_controlled(self):
        if self.controlled:
            if self.controlled_time + self.control_duration < self.timer.time():
                self.controlled = False
                self.controlled_time = None
                self.control_duration = 0
                return False
            return True

    def is_blocked(self):
        self.blocked = bool(self.blocker)

    def search_enemy(self, units):
        if self.atk_type == 2:  # Heal
            min_hp = 10000
            target = None
            for ally in units:
                distance = self.position.distance_to(ally.position)
                if distance < self.range * TILE_SIZE and ally.hp < ally.entity.hp:
                    if ally.hp <= min_hp:
                        min_hp = ally.hp
                        target = ally
            return target
        if self.blocker:
            return self.blocker[0]
        if self.range == 0:
            return None
        nearest = 10000
        target = None
        for unit in units:
            distance = self.position.distance_to(unit.position)
            if distance < nearest:
                nearest = distance
                target = unit
        return target if nearest < self.range * TILE_SIZE else None

    def perform_attack(self, units):
        if self.timer.time() - self.last_atk > self.atk_spd:
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
        self.update_attack_animation()

    def draw(self, screen):
        if self.dead:
            return

        # 判断播放帧
        if self.playing_attack_anim and self.attack_frame_index < len(self.attack_frames):
            frame = self.attack_frames[self.attack_frame_index]
        elif self.attack_frames:
            frame = self.attack_frames[0]  # idle 显示攻击第 0 帧
        else:
            frame = self.sprite  # 如果没有动画帧，则显示静态 sprite

        screen.blit(frame, self.position)

        # 绘制血条
        bar_width = 50
        bar_height = 5
        x = self.position.x
        y = self.position.y + frame.get_height() + 2

        pygame.draw.rect(screen, (255, 0, 0), (x, y, bar_width, bar_height))

        hp_ratio = max(self.hp / self.entity.hp, 0)
        green_width = int(bar_width * hp_ratio)
        pygame.draw.rect(screen, (0, 255, 0), (x, y, green_width, bar_height))