import pygame
from win32api import GetSystemMetrics

import LevelMap
from LevelBuilder import LevelBuilder
from LevelLoopCounter import LevelLoopCounter
from Options import Options

class PacManGame:
    FPS = 60
    def __init__(self, width, height, back):
        self.WIDTH = width
        self.HEIGHT = height
        self.background = back

    def set_screen_size(self):
        self.HEIGHT, self.WIDTH = self.options.SCREEN_SIZES[self.current_screen_size]

    # Додамо метод для оновлення розміру екрану
    def update_screen_size(self):
        self.current_screen_size = self.options.get_current_screen_size()
        self.set_screen_size()

    def start_game(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        timer = pygame.time.Clock()
        level_loop_counter = LevelLoopCounter()

        level_controller = LevelBuilder(self.screen, self.WIDTH, self.HEIGHT, LevelMap.boards, level_loop_counter).build()

        running = True

        while running:
            timer.tick(self.FPS)
            self.screen.fill(self.background)
            level_controller.update()
            level_loop_counter.increase()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return

            pygame.display.flip()

        pygame.quit()

