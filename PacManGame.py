import pygame
from win32api import GetSystemMetrics

import LevelMap
from LevelBuilder import LevelBuilder


class PacManGame:
    HEIGHT = GetSystemMetrics(1) - 70
    WIDTH = HEIGHT * 0.95
    FPS = 60

    def start_game(self):
        pygame.init()
        screen = pygame.display.set_mode([self.WIDTH, self.HEIGHT])
        timer = pygame.time.Clock()

        running = True

        level_controller = LevelBuilder(screen, self.WIDTH, self.HEIGHT, LevelMap.boards).build()

        while running:
            timer.tick(self.FPS)
            screen.fill("black")

            level_controller.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            pygame.display.flip()

        pygame.quit()
