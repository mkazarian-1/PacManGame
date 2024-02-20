import pygame
import copy
import LevelMap
from win32api import GetSystemMetrics
from LevelBuilder import LevelBuilder
from LevelLoopCounter import LevelLoopCounter
from PacMan import PacMan


class PacManGame:
    HEIGHT = GetSystemMetrics(1) - 70
    WIDTH = HEIGHT * 0.95
    FPS = 60

    def start_game(self):
        pygame.init()
        timer = pygame.time.Clock()
        level_loop_counter = LevelLoopCounter()

        screen = pygame.display.set_mode([self.WIDTH, self.HEIGHT])

        level_controller = (LevelBuilder(screen, self.WIDTH, self.HEIGHT, LevelMap.boards, level_loop_counter)
                            .build())
        pacman = PacMan(screen, self.WIDTH, self.HEIGHT, level_controller, level_loop_counter)

        running = True

        while running:
            timer.tick(self.FPS)
            level_loop_counter.increase()

            screen.fill("black")
            level_controller.update()
            pacman.update_position()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        pacman.set_turn_right()
                    elif event.key == pygame.K_LEFT:
                        pacman.set_turn_left()
                    elif event.key == pygame.K_UP:
                        pacman.set_turn_up()
                    elif event.key == pygame.K_DOWN:
                        pacman.set_turn_down()

            pygame.display.flip()

        pygame.quit()
