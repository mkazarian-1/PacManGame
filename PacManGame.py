import pygame
import LevelMap
from win32api import GetSystemMetrics
from LevelBuilder import LevelBuilder
from LevelLoopCounter import LevelLoopCounter
from Options import Options
from PacMan import PacMan
from EnemiesCreator import RedGhost, OrangeGhost, PinkGhost, BlueGhost


class PacManGame:
    pygame.init()
    HEIGHT = GetSystemMetrics(1) - 70
    WIDTH = HEIGHT * 0.95
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
        
        pacman = PacMan(self.screen, self.WIDTH, self.HEIGHT, level_controller, level_loop_counter)

        clyde = OrangeGhost(self.screen, pacman)
        blinky = RedGhost(self.screen, pacman)
        pinky = PinkGhost(self.screen, pacman)
        inky = BlueGhost(self.screen, pacman)

        running = True

        while running:
            timer.tick(self.FPS)
            
            self.screen.fill(self.background)
            level_loop_counter.increase()
            level_controller.update()
            
            pacman.update_position()
            blinky.update()
            clyde.update()
            pinky.update()
            inky.update()

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

