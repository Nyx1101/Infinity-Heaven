from battle.AI.base_ai import BaseAI
import pygame

TILE_SIZE = 64


class CharacterAI(BaseAI):
    def __init__(self, entity, timer, manager, tile_x, tile_y, skill_behavior):
        super().__init__(entity, timer, manager)
        # Character's grid position
        self.tile_x = tile_x
        self.tile_y = tile_y

        # Skill cooldown and duration (from the entity data)
        self.cd = self.entity.cd
        self.duration = self.entity.duration

        # Skill state management
        self.skill_triggered = False
        self.skill_start_time = self.timer.time()
        self.skill_end_time = self.timer.time()

        # Character's pixel position on screen
        self.position = pygame.Vector2(tile_x * TILE_SIZE, tile_y * TILE_SIZE)

        # Skill behavior (must implement trigger_skill, skill_attack, end_skill)
        self.skill = skill_behavior

    @property
    def grid_pos(self):
        # Return current tile (grid) position
        return self.tile_x, self.tile_y

    @property
    def in_cd(self):
        # Return time since last skill ended (used for checking cooldown)
        if self.skill_triggered:
            return 0
        else:
            return self.timer.time() - self.skill_end_time

    def trigger_skill(self):
        # Trigger the skill: update state and call skill's trigger method
        self.skill_triggered = True
        self.skill_start_time = self.timer.time()
        self.skill.trigger_skill(self)

    def skill_attack(self, units):
        # Perform the skill attack (defined by skill_behavior)
        self.skill.skill_attack(self, units)

    def perform_attack(self, units):
        # Determine whether to perform normal or skill attack
        if self.skill is None:
            # No skill: use normal attack only
            if self.timer.time() - self.last_atk > self.atk_spd:
                if self.skill_triggered:
                    if self.skill_attack(units):
                        self.last_atk = self.timer.time()
                else:
                    target = self.search_enemy(units)
                    if target is not None:
                        self.normal_attack(target)
            return

        # If skill is active and expired, end the skill
        if self.skill_triggered:
            if self.timer.time() - self.skill_start_time > self.duration:
                self.skill_triggered = False
                self.skill_end_time = self.timer.time()
                self.skill.end_skill(self)

        # Execute attack logic (skill or normal)
        if self.timer.time() - self.last_atk > self.atk_spd:
            if self.skill_triggered:
                if self.skill_attack(units):
                    self.last_atk = self.timer.time()
            else:
                target = self.search_enemy(units)
                if target is not None:
                    self.normal_attack(target)

    def update(self, units):
        # Update character behavior per frame
        self.is_blocked()
        if self.is_dead():
            return
        if self.is_controlled():
            return
        self.perform_attack(units)
        self.update_attack_animation()

    def draw(self, screen):
        # Draw the character sprite and status bars (HP, skill)
        if not self.dead:
            # Draw attack frame if attacking, otherwise draw idle sprite
            if self.playing_attack_anim:
                frame = self.attack_frames[self.attack_frame_index]
                screen.blit(frame, self.position)
            else:
                screen.blit(self.sprite, self.position)

            # Draw HP bar
            bar_width = 50
            bar_height = 5
            x = self.position.x
            y = self.position.y + self.sprite.get_height() + 2
            pygame.draw.rect(screen, (255, 0, 0), (x, y, bar_width, bar_height))  # Red background

            hp_ratio = max(self.hp / self.entity.hp, 0)
            green_width = int(bar_width * hp_ratio)
            pygame.draw.rect(screen, (0, 255, 0), (x, y, green_width, bar_height))  # Green foreground

            # If character has skill, draw skill duration/cooldown bar
            if self.skill is None:
                return

            skill_y = y + bar_height + 2
            pygame.draw.rect(screen, (50, 50, 50), (x, skill_y, bar_width, bar_height))  # Gray background

            now = self.timer.time()

            if self.skill_triggered:
                # Draw remaining skill duration (orange bar)
                elapsed = now - self.skill_start_time
                if self.duration > 0:
                    ratio = max(0, 1 - elapsed / self.duration)
                    width = int(bar_width * ratio)
                    pygame.draw.rect(screen, (255, 165, 0),
                                     (x + bar_width - width, skill_y, width, bar_height))

            elif now - self.skill_end_time < self.cd:
                # Draw skill cooldown progress (white bar)
                cd_elapsed = now - self.skill_end_time
                if self.cd > 0:
                    ratio = min(cd_elapsed / self.cd, 1)
                    width = int(bar_width * ratio)
                    pygame.draw.rect(screen, (255, 255, 255), (x, skill_y, width, bar_height))
