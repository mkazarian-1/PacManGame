import pygame
from win32api import GetSystemMetrics

import LevelMap
from LevelBuilder import LevelBuilder
from LevelLoopCounter import LevelLoopCounter


class PacManGame:
    HEIGHT = GetSystemMetrics(1) - 70
    WIDTH = HEIGHT * 0.95
    FPS = 60

    def start_game(self):
        pygame.init()

        timer = pygame.time.Clock()
        level_loop_counter = LevelLoopCounter()

        screen = pygame.display.set_mode([self.WIDTH, self.HEIGHT])
        level_controller = LevelBuilder(screen, self.WIDTH, self.HEIGHT, LevelMap.boards, level_loop_counter).build()

        running = True

        while running:
            timer.tick(self.FPS)
            screen.fill("black")
            level_controller.update()
            level_loop_counter.increase()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            pygame.display.flip()

        pygame.quit()

