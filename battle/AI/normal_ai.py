from battle.AI.ai_interface import IAI
from entities.enemy import Entity

class NormalAI:
    def __init__(self, Entity, sprite_manager):
        # 角色状态数据
        self.entity = Entity
        self.current_hp = self.entity.hp
        self.position = [0, 0]
        self.goal = [128, 128]
        self.path = [[32, 32], [64, 64], [96, 96], [128, 128]]
        self.controlled = False
        self.blocked = False
        self.should_exit = False
        self.sprite = sprite_manager  # 控制表现层

    def update(self):
        # 决策逻辑集中在一个方法里
        if self.position == self.goal:
            self.exit()
            return

        if self.hp <= 0:
            self.exit()
            return

        if self.controlled:
            self.sprite.play_animation("stunned")  # 停止动作
            return

        if self.blocked:
            self.sprite.play_animation("attack")   # 播放攻击动画
            return

        # 默认执行移动
        if self.path:
            self.position = self.path.pop(0)
            self.sprite.move_to(self.position)
            self.sprite.play_animation("walk")

    def exit(self):
        self.should_exit = True
        self.sprite.play_animation("fade_out")

class SpriteManager:
    def __init__(self, image):
        self.image = image
        self.rect = image.get_rect()

    def move_to(self, pos):
        self.rect.topleft = pos

    def play_animation(self, name):
        print(f"[Sprite] 播放动画：{name}")

    def draw(self, surface):
        surface.blit(self.image, self.rect)