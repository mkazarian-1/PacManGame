import pygame

import Score
from Health import Health
from level import LevelMap
from level.LevelBuilder import LevelBuilder, LevelBar
from level.LevelLoopCounter import LevelLoopCounter
from menu_pg.Options import Options
from PacMan import PacMan
from EnemiesCreator import RedGhost, OrangeGhost, PinkGhost, BlueGhost

from Mode_Counter import ModeCounter


def get_font(size, ind):
    return pygame.font.Font("assets/Emulogic-zrEw.ttf", int(size * ind))


class PacManGame:
    pygame.init()
    FPS = 60
    RED_GHOST_CELL_COORDINATE = [12, 12]
    PINK_GHOST_CELL_COORDINATE = [12, 15]
    BLUE_GHOST_CELL_COORDINATE = [17, 15]
    ORANGE_GHOST_CELL_COORDINATE = [15, 15]

    def __init__(self, screen_settings):
        self.screen_settings = screen_settings
        self.options = Options(self.screen_settings)
        self.current_screen_size = self.screen_settings.get_screen_size()
        self.background = self.screen_settings.get_background_color()
        self.image_inserted = self.screen_settings.is_image_inserted()
        self.background_image = self.screen_settings.get_background_image()
        self.play_rect = None
        self.menu_rect = None

    def set_screen_size(self):
        self.HEIGHT, self.WIDTH = self.screen_settings.SCREEN_SIZES[self.current_screen_size]

    def start_game(self):
        pygame.init()
        self.set_screen_size()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

        level_surface = pygame.Surface((self.screen.get_width(), self.screen.get_height() - 50))
        level_bar_surface = pygame.Surface(
            (self.screen.get_width(), self.screen.get_height() - level_surface.get_height()))

        clock = pygame.time.Clock()
        level_loop_counter = LevelLoopCounter()

        mode_counter = ModeCounter()

        score = Score.PlayerScore(level_bar_surface)
        health = Health(level_bar_surface, self.show_game_over)

        level_bar = LevelBar(level_bar_surface, self.score, health)

        level_controller = LevelBuilder(level_surface, LevelMap.boards,
                                        level_loop_counter, self.score).build()

        cell_len_x, cell_len_y = level_controller.get_amount_of_cells()

        pacman = PacMan(level_surface, level_controller, level_loop_counter)

        red_ghost = RedGhost(level_surface, level_controller, health, pacman,
                             self.RED_GHOST_CELL_COORDINATE,
                             [cell_len_x, 0], mode_counter, score)

        blue_ghost = BlueGhost(level_surface, level_controller, health, pacman,
                               self.BLUE_GHOST_CELL_COORDINATE,
                               [cell_len_x, cell_len_y], red_ghost, mode_counter, score)

        pink_ghost = PinkGhost(level_surface, level_controller, health, pacman,
                               self.PINK_GHOST_CELL_COORDINATE,
                               [0, 0],  mode_counter, score)
        orange_ghost = OrangeGhost(level_surface, level_controller, health, pacman,
                                   self.ORANGE_GHOST_CELL_COORDINATE,
                                   [0, cell_len_y], mode_counter, score)

        ghosts = [red_ghost, blue_ghost, pink_ghost, orange_ghost]

        running = True

        while running:
            clock.tick(self.FPS)

            self.screen.blit(level_surface, (0, 0))
            self.screen.blit(level_bar_surface, (0, level_surface.get_height()))

            level_surface.fill(self.background)
            level_bar_surface.fill(self.background)

            if self.image_inserted:
                level_surface.blit(self.background_image, (0, 0))

            level_loop_counter.increase()
            mode_counter.increase()
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
                    elif event.key == pygame.K_SPACE:
                        health.decrease_health()
                    elif event.key == pygame.K_ESCAPE:
                        self.back_to_menu()

            pygame.display.flip()
        pygame.quit()

    def show_game_over(self):
        clock = pygame.time.Clock()
        screen = self.screen
        self.draw_end(screen)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    menu_mouse_pos = pygame.mouse.get_pos()
                    if self.play_rect.collidepoint(menu_mouse_pos):
                        self.start_game()
                    if self.menu_rect.collidepoint(menu_mouse_pos):
                        self.back_to_menu()
            self.draw_end(screen)
            pygame.display.flip()
            clock.tick(60)
        pygame.quit()

    def draw_end(self, screen):
        if self.current_screen_size == "Large":
            ind = 1
        elif self.current_screen_size == "Medium":
            ind = 0.7
        elif self.current_screen_size == "Small":
            ind = 0.5

        overlay = pygame.Surface(screen.get_size())
        overlay.set_alpha(10)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        text = get_font(65, ind).render("Game Over", True, (255, 0, 0))
        text_rect = text.get_rect(center=(self.WIDTH // 2, (self.HEIGHT // 2) - (250 * ind)))
        screen.blit(text, text_rect)

        score_instance = Score.PlayerScore(self.screen)
        score_text = get_font(30, ind).render("Score: " + str(self.score.get_score()), True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(self.WIDTH // 2, (self.HEIGHT // 2) - (160 * ind)))
        screen.blit(score_text, score_rect)

        play_button = get_font(55, ind).render("Restart", True, (255, 255, 255))
        self.play_rect = play_button.get_rect(center=(self.WIDTH // 2, (self.HEIGHT // 2) - (35 * ind)))
        self.screen.blit(play_button, self.play_rect)

        if self.play_rect.collidepoint(pygame.mouse.get_pos()):
            play_button = get_font(55, ind).render("Restart", True, (255, 242, 204))
            self.screen.blit(play_button, self.play_rect)

        menu_button = get_font(55, ind).render("Back to menu", True, (255, 255, 255))
        self.menu_rect = menu_button.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2 + (105 * ind)))
        self.screen.blit(menu_button, self.menu_rect)

        if self.menu_rect.collidepoint(pygame.mouse.get_pos()):
            menu_button = get_font(55, ind).render("Back to menu", True, (255, 242, 204))
            self.screen.blit(menu_button, self.menu_rect)

    def back_to_menu(self):
        from menu_pg.Menu import Menu
        menu = Menu(self.screen_settings)
        menu.start()
