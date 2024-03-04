import pygame

import Score
from Health import Health
from level import LevelMap
from win32api import GetSystemMetrics
from level.LevelBuilder import LevelBuilder, LevelBar
from level.LevelLoopCounter import LevelLoopCounter
from menu_pg.Options import Options
from PacMan import PacMan
from EnemiesCreator import RedGhost, OrangeGhost, PinkGhost, BlueGhost


class PacManGame:
    pygame.init()
    HEIGHT = GetSystemMetrics(1) - 70
    WIDTH = HEIGHT * 0.95
    FPS = 60
    RED_GHOST_CELL_COORDINATE = [12, 12]
    PINK_GHOST_CELL_COORDINATE = [12, 15]
    BLUE_GHOST_CELL_COORDINATE = [17, 15]
    ORANGE_GHOST_CELL_COORDINATE = [15, 15]

    def __init__(self, width, height, back, image, ins):
        self.options = Options()
        self.current_screen_size = self.options.get_current_screen_size()
        self.WIDTH = width
        self.HEIGHT = height
        self.background = back
        self.image_inserted = self.options.is_image_inserted()
        self.background_image = image
        self.ins = ins

    def set_screen_size(self):
        self.HEIGHT, self.WIDTH = self.options.SCREEN_SIZES[self.current_screen_size]

    def start_game(self):

        pygame.init()

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

        level_surface = pygame.Surface((self.screen.get_width(), self.screen.get_height() - 50))
        level_bar_surface = pygame.Surface(
            (self.screen.get_width(), self.screen.get_height() - level_surface.get_height()))

        clock = pygame.time.Clock()
        level_loop_counter = LevelLoopCounter()

        score = Score.PlayerScore(level_bar_surface)
        health = Health(level_bar_surface)

        level_bar = LevelBar(level_bar_surface, score, health)

        level_controller = LevelBuilder(level_surface, LevelMap.boards,
                                        level_loop_counter, score).build()

        cell_len_x, cell_len_y = level_controller.get_amount_of_cells()

        pacman = PacMan(level_surface, level_controller, level_loop_counter)
        ghosts = [
            RedGhost(level_surface, level_controller, health,
                     self.RED_GHOST_CELL_COORDINATE,
                     [cell_len_x, 0], pacman),
            BlueGhost(level_surface, level_controller, health,
                      self.BLUE_GHOST_CELL_COORDINATE,
                      [cell_len_x, cell_len_y]),
            PinkGhost(level_surface, level_controller, health,
                      self.PINK_GHOST_CELL_COORDINATE,
                      [0, 0]),
            OrangeGhost(level_surface, level_controller, health,
                        self.ORANGE_GHOST_CELL_COORDINATE,
                        [0, cell_len_y]),
        ]

        running = True

        while running:
            clock.tick(self.FPS)

            self.screen.blit(level_surface, (0, 0))
            self.screen.blit(level_bar_surface, (0, level_surface.get_height()))

            level_surface.fill(self.background)
            level_bar_surface.fill(self.background)
            if self.ins:
                level_surface.blit(self.background_image, (0, 0))

            level_loop_counter.increase()
            level_controller.update()
            level_bar.update()
            pacman.update_position()

            for ghost in ghosts:
                ghost.update_position()

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
                    elif event.key == pygame.K_ESCAPE:
                        return

            pygame.display.flip()
        pygame.quit()
