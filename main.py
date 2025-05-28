import pygame
import sys
from UI.screen_manager import ScreenManager
from UI.screens.main_menu import DummyScreen
from UI.screens.battle import BattleScreen

pygame.init()
screen = pygame.display.set_mode((704, 448))
pygame.display.set_caption("Demo")
clock = pygame.time.Clock()

# 初始化并挂载第一个页面
dummy_screen = DummyScreen(None)
battle_screen = BattleScreen(None)
manager = ScreenManager(battle_screen)
dummy_screen.manager = manager  # 注入 manager 回屏幕类（如需切换）

# 主循环
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        manager.get_screen().handle_event(event)

    manager.get_screen().update()
    manager.get_screen().draw(screen)
    pygame.display.flip()
    clock.tick(60)