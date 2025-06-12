import pygame
from entities.entity import Entity
import os

TILE_SIZE = 64  # Size of each tile in pixels


class BaseAI:
    def __init__(self, entity: Entity, timer, manager):
        # Reference to the entity this AI controls
        self.entity = entity
        self.manager = manager

        # Combat stats
        self.hp = self.entity.hp
        self.atk = self.entity.atk
        self.dfs = self.entity.defense
        self.res = self.entity.resistance
        self.atk_spd = self.entity.attack_speed
        self.atk_type = self.entity.atk_type  # 0: Physical, 1: Magical, 2: Healing
        self.range = self.entity.range  # Range in tiles

        self.timer = timer  # External timer for time tracking

        # State flags
        self.controlled = False  # Is currently under control effect
        self.controlled_time = None  # Time when control started
        self.control_duration = 0  # Duration of control effect
        self.blocked = False  # Whether movement is blocked
        self.blocker = []  # List of enemies or objects currently blocking this unit
        self.dead = False  # Death status

        # Combat timing
        self.last_atk = self.timer.time()  # Timestamp of last attack

        # Position will be updated externally
        self.position = None

        # Attack animation frames
        self.attack_frames = self.load_attack_animation(f"assets/animation/{self.entity.id}")
        self.sprite = self.attack_frames[0] if self.attack_frames else None
        self.attack_anim_fps = 12  # Animation speed (frames per second)
        self.attack_anim_start_time = 0
        self.attack_frame_index = 0
        self.playing_attack_anim = False

    def load_attack_animation(self, folder):
        """Load attack animation frames from a folder."""
        frames = []
        if not os.path.exists(folder):
            return frames

        files = os.listdir(folder)
        png_files = [f for f in files if f.endswith(".png")]
        entity_id = self.entity.id

        # Select different file sorting logic based on entity ID
        if 100 <= entity_id <= 108:
            # Format: attack_0.png, attack_1.png, ...
            attack_files = [f for f in png_files if f.startswith("attack_")]
            attack_files.sort(key=lambda name: int(name.split("_")[1].split(".")[0]))

        elif 200 <= entity_id <= 209:
            # Format: anyfilename ending in two digits before .png
            attack_files = []
            for f in png_files:
                base = os.path.splitext(f)[0]
                if len(base) >= 2 and base[-2:].isdigit():
                    attack_files.append(f)
            attack_files.sort(key=lambda name: int(os.path.splitext(name)[0][-2:]))

        else:
            # Default fallback to attack_*.png format
            attack_files = [f for f in png_files if f.startswith("attack_")]
            attack_files.sort(key=lambda name: int(name.split("_")[1].split(".")[0]))

        # Load images into memory
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
        """Begin playing the attack animation from the start."""
        self.playing_attack_anim = True
        self.attack_anim_start_time = self.timer.time()
        self.attack_frame_index = 0

    def update_attack_animation(self):
        """Update the animation frame based on elapsed time."""
        if not self.playing_attack_anim:
            return

        elapsed = self.timer.time() - self.attack_anim_start_time
        frame_duration = 1 / self.attack_anim_fps
        self.attack_frame_index = int(elapsed / frame_duration)

        # Animation ends when we reach the last frame
        if self.attack_frame_index >= len(self.attack_frames):
            self.playing_attack_anim = False
            self.attack_frame_index = 0

    def normal_attack(self, unit):
        """Perform a normal attack or healing action on a target unit."""
        if not unit:
            # No target: still trigger animation
            self.last_atk = self.timer.time()
            self.start_attack_animation()
            return None

        # Calculate damage based on attack type
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
        """Check if unit has died and perform cleanup."""
        if self.hp <= 0 or self.dead:
            self.dead = True
            for blocker in self.blocker:
                if self in blocker.blocker:
                    blocker.blocker.remove(self)
            return True

    def be_controlled(self, time):
        """Apply a control effect (e.g., stun or freeze)."""
        self.controlled = True
        self.control_duration = time
        self.controlled_time = self.timer.time()

    def is_controlled(self):
        """Check if the unit is still under control effect."""
        if self.controlled:
            if self.controlled_time + self.control_duration < self.timer.time():
                self.controlled = False
                self.controlled_time = None
                self.control_duration = 0
                return False
            return True

    def is_blocked(self):
        """Check if unit is currently blocked by others."""
        self.blocked = bool(self.blocker)

    def search_enemy(self, units):
        """Find a target unit to attack or heal."""
        if self.atk_type == 2:  # Healing logic
            min_hp = float("inf")
            target = None
            for ally in units:
                distance = self.position.distance_to(ally.position)
                if distance < self.range * TILE_SIZE and ally.hp < ally.entity.hp:
                    if ally.hp <= min_hp:
                        min_hp = ally.hp
                        target = ally
            return target

        # Blocked enemies take priority
        if self.blocker:
            return self.blocker[0]

        if self.range == 0:
            return None

        # Search nearest target in range
        nearest = float("inf")
        target = None
        for unit in units:
            distance = self.position.distance_to(unit.position)
            if distance < nearest:
                nearest = distance
                target = unit

        return target if nearest < self.range * TILE_SIZE else None

    def perform_attack(self, units):
        """Check attack cooldown and perform attack if ready."""
        if self.timer.time() - self.last_atk > self.atk_spd:
            target = self.search_enemy(units)
            if target is not None:
                self.normal_attack(target)

    def update(self, units):
        """Main update function to be called every frame."""
        self.is_blocked()
        if self.is_dead():
            return
        if self.is_controlled():
            return
        self.perform_attack(units)
        self.update_attack_animation()

    def draw(self, screen):
        """Draw the unit sprite and its health bar."""
        if self.dead:
            return

        # Select current frame
        if self.playing_attack_anim and self.attack_frame_index < len(self.attack_frames):
            frame = self.attack_frames[self.attack_frame_index]
        else:
            frame = self.sprite  # Use idle/static frame if animation is not active

        screen.blit(frame, self.position)

        # Draw health bar below the sprite
        bar_width = 50
        bar_height = 5
        x = self.position.x
        y = self.position.y + frame.get_height() + 2

        # Background (red) bar
        pygame.draw.rect(screen, (255, 0, 0), (x, y, bar_width, bar_height))

        # Foreground (green) bar showing current HP
        hp_ratio = max(self.hp / self.entity.hp, 0)
        green_width = int(bar_width * hp_ratio)
        pygame.draw.rect(screen, (0, 255, 0), (x, y, green_width, bar_height))
        
