# battle/entities/battle_entity.py

from typing import TypeVar, Generic
import pygame
from battle.AI.ai_interface import IAI

T = TypeVar("T")  # 泛型，绑定任意数据类型

class BattleEntity(Generic[T]):
    def __init__(self, data: T, sprite: pygame.sprite.Sprite, ai: IAI = None):
        self.data: T = data
        self.sprite: pygame.sprite.Sprite = sprite
        self.ai: IAI | None = ai

    def update(self) -> None:
        # 更新 AI 行为
        if self.ai:
            self.ai.update()

        # 更新 sprite 状态（动画、位置等）
        self.sprite.update()

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.sprite.image, self.sprite.rect)