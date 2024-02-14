import pygame
from win32api import GetSystemMetrics
import copy

import LevelMap
from LevelBuilder import LevelBuilder
from LevelLoopCounter import LevelLoopCounter
from PacMan import PacMan

class PacManGame:
    HEIGHT = GetSystemMetrics(1) - 70
    WIDTH = HEIGHT * 0.95
    FPS = 60
    level = copy.deepcopy(LevelMap.boards)
    def start_game(self):
        pygame.init()
        timer = pygame.time.Clock()
        level_loop_counter = LevelLoopCounter()

        screen = pygame.display.set_mode([self.WIDTH, self.HEIGHT])
        level_controller = LevelBuilder(screen, self.WIDTH, self.HEIGHT, LevelMap.boards, level_loop_counter).build()

        pacman = PacMan(self.WIDTH, self.HEIGHT, self.level)
        turns_allowed = [False, False, False, False]

        running = True

        while running:
            timer.tick(self.FPS)
            screen.fill("black")
            level_controller.update()
            level_loop_counter.increase()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        pacman.direction = 0
                        pacman.update_position()
                    elif event.key == pygame.K_LEFT:
                        pacman.direction = 1
                        pacman.update_position()
                    elif event.key == pygame.K_UP:
                        pacman.direction = 2
                        pacman.update_position()
                    elif event.key == pygame.K_DOWN:
                        pacman.direction = 3
                        pacman.update_position()

            pacman.draw_player(screen, level_loop_counter.get())

            pygame.display.flip()

        pygame.quit()

