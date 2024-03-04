import pygame
from level import LevelMap
from win32api import GetSystemMetrics
from level.LevelBuilder import LevelBuilder
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

        clock = pygame.time.Clock()

        level_loop_counter = LevelLoopCounter()

        level_controller = LevelBuilder(self.screen, self.WIDTH, self.HEIGHT, LevelMap.boards,
                                        level_loop_counter).build()
        cell_len_x, cell_len_y = level_controller.get_amount_of_cells()
        pacman = PacMan(self.screen, level_controller, level_loop_counter)

        blinky = RedGhost(self.screen, level_controller, self.RED_GHOST_CELL_COORDINATE,
                          [cell_len_x, 0], pacman)
        inky = BlueGhost(self.screen, level_controller, self.BLUE_GHOST_CELL_COORDINATE,
                         (pacman.pacman_cell_x, pacman.pacman_cell_y), pacman, blinky)
        pinky = PinkGhost(self.screen, level_controller, self.PINK_GHOST_CELL_COORDINATE,
                          (pacman.pacman_cell_x, pacman.pacman_cell_y), pacman)
        clyde = OrangeGhost(self.screen, level_controller, self.ORANGE_GHOST_CELL_COORDINATE,
                            (pacman.pacman_cell_x, pacman.pacman_cell_y), pacman)

        ghosts = [blinky, inky, pinky, clyde]

        running = True

        while running:
          
            clock.tick(self.FPS)

            self.screen.fill(self.background)
    
            if self.ins:
                self.screen.blit(self.background_image, (0, 0))
          
            level_loop_counter.increase()
            level_controller.update()

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
