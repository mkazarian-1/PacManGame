import pygame

import Score
from EndGameScreen import EndGameScreen
from Health import Health
from Observer import IObserver
from level import LevelMap
from level.EndGameController import EndGameController
from level.LevelBuilder import LevelBuilder, LevelBar
from PacMan import PacMan
from EnemiesCreator import RedGhost, OrangeGhost, PinkGhost, BlueGhost

from Mode_Counter import ModeCounter
from GhostStartGameCounter import GhostStartGameCounter


def get_font(size, ind):
    return pygame.font.Font("assets/Emulogic-zrEw.ttf", int(size * ind))


class PacManGame(IObserver):
    pygame.init()
    FPS = 60
    RED_GHOST_CELL_COORDINATE = [12, 12]
    PINK_GHOST_CELL_COORDINATE = [12, 15]
    BLUE_GHOST_CELL_COORDINATE = [17, 15]
    ORANGE_GHOST_CELL_COORDINATE = [15, 15]

    def __init__(self, screen_settings):
        self.screen_settings = screen_settings
        self.current_screen_size = self.screen_settings.get_screen_size()
        self.background = self.screen_settings.get_background_color()
        self.image_inserted = self.screen_settings.is_image_inserted()
        self.background_image = self.screen_settings.get_background_image()
        self.play_rect = None
        self.menu_rect = None

        self.set_screen_size()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.level_surface = pygame.Surface((self.screen.get_width(), self.screen.get_height() - 50))
        self.level_bar_surface = pygame.Surface(
            (self.screen.get_width(), self.screen.get_height() - self.level_surface.get_height()))

        self.score = Score.PlayerScore(self.level_bar_surface)
        self.health = Health(self.level_bar_surface)
        self.health.add_observer(self)

        self.endGameController = EndGameController()
        self.level_controller = LevelBuilder(self.level_surface, LevelMap.boards,
                                             self.score, self.endGameController).build()
        self.running = True

    def set_screen_size(self):
        self.HEIGHT, self.WIDTH = self.screen_settings.SCREEN_SIZES[self.current_screen_size]

    def update_observer(self, event):
        self.running = False

    def start_game(self):
        while self.health.is_alive() and not self.endGameController.is_win():
            self.level_start()

        if self.endGameController.is_win():
            game_over_screen = EndGameScreen(self.screen_settings, self.score.get_score(), True)
            game_over_screen.show_game_over()
        else:
            game_over_screen = EndGameScreen(self.screen_settings, self.score.get_score(), False)
            game_over_screen.show_game_over()

    def level_start(self):
        pygame.init()

        clock = pygame.time.Clock()

        mode_counter = ModeCounter()

        ghost_start_game_counter = GhostStartGameCounter()

        level_bar = LevelBar(self.level_bar_surface, self.score, self.health)

        cell_len_x, cell_len_y = self.level_controller.get_amount_of_cells()

        pacman = PacMan(self.level_surface, self.level_controller)

        red_ghost = RedGhost(self.level_surface, self.level_controller, self.health, pacman,
                             self.RED_GHOST_CELL_COORDINATE,
                             [cell_len_x, 0], mode_counter, self.score, ghost_start_game_counter)

        blue_ghost = BlueGhost(self.level_surface, self.level_controller, self.health, pacman,
                               self.BLUE_GHOST_CELL_COORDINATE,
                               [cell_len_x, cell_len_y], red_ghost, mode_counter, self.score, ghost_start_game_counter)

        pink_ghost = PinkGhost(self.level_surface, self.level_controller, self.health, pacman,
                               self.PINK_GHOST_CELL_COORDINATE,
                               [0, 0], mode_counter, self.score, ghost_start_game_counter)
        orange_ghost = OrangeGhost(self.level_surface, self.level_controller, self.health, pacman,
                                   self.ORANGE_GHOST_CELL_COORDINATE,
                                   [0, cell_len_y], mode_counter, self.score, ghost_start_game_counter)

        ghosts = [red_ghost, blue_ghost, pink_ghost, orange_ghost]

        self.running = True

        while self.running:
            clock.tick(self.FPS)

            self.screen.blit(self.level_surface, (0, 0))
            self.screen.blit(self.level_bar_surface, (0, self.level_surface.get_height()))

            self.level_surface.fill(self.background)
            self.level_bar_surface.fill(self.background)
            if self.image_inserted:
                self.level_surface.blit(self.background_image, (0, 0))

            if self.endGameController.is_win():
                self.running = False

            self.level_controller.update()

            ghost_start_game_counter.increase()

            mode_counter.increase()

            level_bar.update()
            pacman.update_position()

            for ghost in ghosts:
                ghost.update_position()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

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
                        self.back_to_menu()

            pygame.display.flip()

    def back_to_menu(self):
        from menu_pg.Menu import Menu
        menu = Menu(self.screen_settings)
        menu.start()
