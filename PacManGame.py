import pygame
import LevelMap
from win32api import GetSystemMetrics
from LevelBuilder import LevelBuilder
from LevelLoopCounter import LevelLoopCounter
from PacMan import PacMan
from EnemiesCreator import RedGhost, OrangeGhost, PinkGhost, BlueGhost
from RunAwayCounter import Run_Away_Counter
from PowerupCounter import Powerup_Counter


class PacManGame:
    pygame.init()
    HEIGHT = GetSystemMetrics(1) - 70
    WIDTH = HEIGHT * 0.95
    FPS = 60

    # blinky_x = 48
    # blinky_y = 40
    # blinky_direction = 0
    # blinky_dead = False
    # blinky_speed = 2
    # powerup = False
    # blinky_box = False
    # blinky_eaten = False
    #
    # clyde_x = int(WIDTH // 2)
    # clyde_y = int(HEIGHT // 2) - 70
    # clyde_direction = 2
    # clyde_dead = False
    # clyde_speed = 2
    # clyde_box = True
    # clyde_eaten = False

    # img_dead = pygame.transform.scale(pygame.image.load("ghosts/dead.png"), (WIDTH*0.05, HEIGHT*0.05))
    img_spooked_blinky = pygame.transform.scale(pygame.image.load("ghosts/powerup.png"), (WIDTH*0.05, HEIGHT*0.05))
    # blinky_img = pygame.transform.scale(pygame.image.load("ghosts/red.png"), (WIDTH*0.05, HEIGHT*0.05))
    clyde_img = pygame.transform.scale(pygame.image.load("ghosts/orange.png"), (WIDTH * 0.05, HEIGHT * 0.05))
    # pacman = pygame.transform.scale(pygame.image.load("pacman/1.png"), (WIDTH*0.05, HEIGHT*0.05))
    img_spooked_clyde = pygame.transform.scale(pygame.image.load("ghosts/powerup.png"), (WIDTH*0.05, HEIGHT*0.05))
    img_spooked_copy = img_spooked_blinky.copy()
    pacman_x = 300
    pacman_y = 530
    pacman_speed = 4
    change_direction_blinky = False
    change_direction_clyde = False
    font = pygame.font.Font("freesansbold.ttf", 20)

    run_away_counter = Run_Away_Counter()
    run_away_counter.increase()

    def start_game(self):
        pygame.init()
        timer = pygame.time.Clock()
        level_loop_counter = LevelLoopCounter()

        powerup_counter = Powerup_Counter()

        screen = pygame.display.set_mode([self.WIDTH, self.HEIGHT])

        level_controller = (LevelBuilder(screen, self.WIDTH, self.HEIGHT, LevelMap.boards, level_loop_counter)
                            .build())
        pacman = PacMan(screen, self.WIDTH, self.HEIGHT, level_controller, level_loop_counter)
        clyde = OrangeGhost(screen, pacman)
        blinky = RedGhost(screen, pacman)
        pinky = PinkGhost(screen, pacman)
        inky = BlueGhost(screen, pacman)

        running = True

        # cell_height = (int(self.HEIGHT - 50)) // len(boards)
        # cell_width = int(self.WIDTH) // len(boards[0])
        while running:
            timer.tick(self.FPS)
            level_loop_counter.increase()

            screen.fill("black")
            level_controller.update()
            pacman.update_position()

            blinky.update()
            clyde.update()
            pinky.update()
            inky.update()

            # score_text = self.font.render(f"Powerup: {powerup_counter.get()}", True, 'white')
            # screen.blit(score_text, (20, 750))

            self.run_away_counter.increase()

            # screen.blit(self.pacman, (self.pacman_x, self.pacman_y))

            pacman_rect = pygame.rect.Rect((self.pacman_x + 10, self.pacman_y + 10), (30, 30))

            # if boards[self.pacman_y // cell_height][self.pacman_x // cell_width] == 2:
            #     self.powerup = True

            # if int(self.WIDTH // 2) - 70 < self.clyde_x < int(self.WIDTH // 2) + 60 \
            #         and int(self.HEIGHT // 2) - 140 < self.clyde_y < int(self.HEIGHT // 2) and not self.powerup:
            #     self.clyde_box = True
            #     target_x_c = int(self.WIDTH // 2)
            #     target_y_c = int(self.HEIGHT // 2) - 140
            # elif not (int(self.WIDTH // 2) - 70 < self.clyde_x < int(self.WIDTH // 2) + 60 \
            #           and int(self.HEIGHT // 2) - 140 < self.clyde_y < int(self.HEIGHT // 2)) and not self.powerup:
            #     self.clyde_box = False
            #     target_x_c = self.pacman_x
            #     target_y_c = self.pacman_y
            #
            # if not self.powerup:
            #     if not self.clyde_box:
            #         target_x_c = self.pacman_x
            #         target_y_c = self.pacman_y
            #     target_x_b = self.pacman_x
            #     target_y_b = self.pacman_y
            #     self.blinky_speed = 2
            #     self.blinky_dead = False
            #     self.blinky_eaten = False
            #     self.change_direction_blinky = False
            #     self.clyde_speed = 2
            #     self.clyde_dead = False
            #     self.clyde_eaten = False
            #     self.change_direction_clyde = False
            #     self.img_spooked_blinky = self.img_spooked_copy
            #     self.img_spooked_clyde = self.img_spooked_copy
            # else:
            #     if not self.clyde_dead and not self.clyde_box:
            #         target_x_c = self.pacman_x
            #         target_y_c = self.pacman_y
            #     if not self.blinky_dead and not self.blinky_box:
            #         target_x_b = self.pacman_x
            #         target_y_b = self.pacman_y
            #     powerup_counter.increase()
            #     if powerup_counter.get() == 799:
            #         self.powerup = False

            # blinky = RedGhost(self.blinky_x, self.blinky_y, self.blinky_direction, self.blinky_img, self.blinky_dead,
            #                   self.blinky_speed, self.powerup, self.blinky_box, self.blinky_eaten, screen, self.img_spooked_blinky,
            #                   48, 40, pacman_rect)
            # blinky.draw_blinky()

            # clyde = OrangeGhost(self.clyde_x, self.clyde_y, self.clyde_direction, self.clyde_img, self.clyde_dead,
            #                     self.clyde_speed, self.powerup, self.clyde_box, self.clyde_eaten, screen, self.img_spooked_clyde,
            #                     self.img_dead, target_x_c, target_y_c, pacman_rect)

            # if self.powerup and not self.blinky_dead and not self.blinky_eaten and not self.change_direction_blinky:  # коли пакмен з'їдає енерджайзер
            #     self.blinky_direction = blinky.spooked()
            #     self.change_direction_blinky = True
            # if self.powerup and not self.clyde_dead and not self.clyde_eaten and not self.change_direction_clyde:
            #     self.clyde_direction = clyde.spooked()
            #     self.change_direction_clyde = True
            #
            # if (self.clyde_box and not self.powerup) or (self.clyde_box and self.powerup):
            #     self.clyde_direction, self.clyde_x, self.clyde_y = clyde.general_movement()
            #
            # if self.powerup and self.blinky_dead and not self.blinky_box:     # змінити ціль для виходу з коробки
            #     target_x_b = int(self.WIDTH//2) - 20
            #     target_y_b = int(self.HEIGHT//2) - 30
            # if self.powerup and self.clyde_dead and not self.clyde_box:
            #     target_x_c = int(self.WIDTH//2) - 20
            #     target_y_c = int(self.HEIGHT//2) - 30
            # if self.run_away_counter.get() > 2000 and not self.powerup:     # режим розбігання
            #     target_x_b, target_y_b = blinky.run_away()
            #     target_x_c, target_y_c = clyde.run_away()
            #
            # if self.powerup and not self.blinky_dead and not self.blinky_eaten:    # перевірка зіткнень з пакменом
            #     self.blinky_dead, self.blinky_eaten, target_x_b, target_y_b, self.blinky_speed = blinky.pacman_collision()
            # if self.powerup and not self.clyde_dead and not self.clyde_eaten:
            #     self.clyde_dead, self.clyde_eaten, target_x_c, target_y_c, self.clyde_speed = clyde.pacman_collision()
            #
            # if self.powerup and self.blinky_eaten and self.blinky_dead and not self.blinky_box:  # якщо зіткнулися з пакменом в режимі енерджайзера
            #     self.blinky_x, self.blinky_y, self.blinky_direction = blinky.return_to_the_box()
            # elif not self.blinky_box:
            #     self.blinky_speed = 2
            # if self.powerup and self.clyde_eaten and self.clyde_dead and not self.clyde_box:
            #     self.clyde_x, self.clyde_y, self.clyde_direction = clyde.return_to_the_box()
            # elif not self.clyde_box:
            #     self.clyde_speed = 2
            #
            # if (not self.powerup and not self.blinky_dead and not self.blinky_eaten) \
            #         or (self.powerup and not self.blinky_dead and not self.blinky_eaten) or not self.blinky_box:
            #     self.blinky_x, self.blinky_y, self.blinky_direction = blinky.move()
            # if (not self.powerup and not self.clyde_dead and not self.clyde_eaten) \
            #         or (self.powerup and not self.clyde_dead and not self.clyde_eaten) or not self.clyde_box:
            #     self.clyde_x, self.clyde_y, self.clyde_direction = clyde.move()
            #
            # if int(self.WIDTH // 2) - 70 < self.blinky_x < int(self.WIDTH // 2) + 60 \
            #         and int(self.HEIGHT // 2) - 100 < self.blinky_y < int(self.HEIGHT // 2) - 50\
            #         and self.powerup and self.blinky_dead and self.blinky_eaten:                    # якщо в коробці :(
            #     print("blinky box")
            #     self.img_spooked_blinky = self.blinky_img
            #     self.blinky_direction, self.blinky_eaten, self.blinky_dead, self.blinky_box, target_x_b, target_y_b = blinky.go_from_box()
            # if int(self.WIDTH // 2) - 70 < self.clyde_x < int(self.WIDTH // 2) + 60 \
            #         and int(self.HEIGHT // 2) - 100 < self.clyde_y < int(self.HEIGHT // 2) - 50 \
            #         and self.powerup and self.clyde_dead:
            #     print("clyde box")
            #     self.img_spooked_clyde = self.clyde_img
            #     self.clyde_direction, self.clyde_eaten, self.clyde_dead, self.clyde_box, target_x_c, target_y_c = clyde.go_from_box()
            # blinky.draw()
            # clyde.draw()
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

