from abc import ABC, abstractmethod
import numpy as np
from LevelMap import boards
import pygame


class Ghost:
    def __init__(self, screen, pacman, dead, eaten, powerup, in_box, ghost_width, ghost_height,
                 pacman_game, cell_width, cell_height):

        self.pacman_game = pacman_game
        self.screen = screen
        self.pacman = pacman
        self.dead = dead
        self.eaten = eaten
        self.powerup = powerup
        self.in_box = in_box
        self.ghost_width = ghost_width
        self.ghost_height = ghost_height
        self.cell_height = cell_height
        self.cell_width = cell_width
        self.img_spooked = pygame.transform.scale(pygame.image.load("ghosts/powerup.png"), (self.ghost_width,
                                                                                            self.ghost_height))
        self.img_dead = pygame.transform.scale(pygame.image.load("ghosts/dead.png"), (self.ghost_width,
                                                                                      self.ghost_height))

    def draw(self, img, x_pos, y_pos):
        if not self.powerup and not self.dead and not self.eaten \
                or (self.powerup and self.dead and self.eaten and self.in_box):
            self.screen.blit(img, (x_pos, y_pos))
        elif self.powerup and not self.dead and not self.eaten:
            self.screen.blit(self.img_spooked, (x_pos, y_pos))
        elif self.powerup and self.eaten and self.dead:
            self.screen.blit(self.img_dead, (x_pos, y_pos))

    def get_rect(self):
        ghost_rect = pygame.rect.Rect((self.center_x, self.center_y), (self.ghost_width, self.ghost_height))
        return ghost_rect

    # def pacman_collision(self, dead, eaten, target_x, target_y, powerup, speed, ghost_rect):
    #     if (pygame.Rect.colliderect(ghost_rect, self.pacman_rect) and powerup and not dead
    #             and not eaten):
    #         dead = True
    #         eaten = True
    #         target_x = int(self.pacman_game.WIDTH // 2) - 10
    #         target_y = int(self.pacman_game.HEIGHT // 2) - 100
    #         speed *= 2
    #     return dead, eaten, target_x, target_y, speed

    def spooked(self):
        if self.direction == 0:
            self.direction = 1
        elif self.direction == 1:
            self.direction = 0
        elif self.direction == 2:
            self.direction = 3
        elif self.direction == 3:
            self.direction = 2
        return self.direction

    def collisions(self, x_pos, y_pos):
        num1 = self.cell_width//2
        num2 = self.cell_height//2
        allowed_turns = [False, False, False, False]
        if self.in_box and boards[(y_pos - num2) // self.cell_height][x_pos // self.cell_width] == 9\
                or self.in_box:
            allowed_turns[2] = True
            self.in_box = False
        elif not self.in_box:
            if boards[y_pos // self.cell_height][(x_pos + num1) // self.cell_width] < 3 \
                    or boards[y_pos // self.cell_height][(x_pos + num1) // self.cell_width] == 9:
                allowed_turns[0] = True
            if boards[y_pos // self.cell_height][(x_pos - num1) // self.cell_width] < 3 \
                    or boards[y_pos // self.cell_height][(x_pos - num1) // self.cell_width] == 9:
                allowed_turns[1] = True
            if boards[(y_pos - num2) // self.cell_height][x_pos // self.cell_width] < 3 \
                    or boards[(y_pos - num2) // self.cell_height][x_pos // self.cell_width] == 9:
                allowed_turns[2] = True
            if boards[(y_pos + num2) // self.cell_height][x_pos // self.cell_width] < 3 \
                    or boards[(y_pos + num2) // self.cell_height][x_pos // self.cell_width] == 9:
                allowed_turns[3] = True
        return allowed_turns

    def go_from_box(self):
        if int(self.pacman_game.WIDTH // 2) - 70 < self.x_pos < int(self.pacman_game.WIDTH // 2) + 60 \
                and int(self.pacman_game.HEIGHT // 2) - 100 < self.y_pos < int(self.pacman_game.HEIGHT // 2) - 50:
            self.direction = 2
            self.eaten = False
            self.dead = False
            self.target_x = int(self.pacman_game.WIDTH // 2)
            self.target_y = int(self.pacman_game.HEIGHT // 2) - 140
        elif not(int(self.pacman_game.WIDTH // 2) - 70 < self.x_pos < int(self.pacman_game.WIDTH // 2) + 60 \
                 and int(self.pacman_game.HEIGHT // 2) - 100 < self.y_pos < int(self.pacman_game.HEIGHT // 2) - 50):
            self.in_box = False
        return self.direction, self.eaten, self.dead, self.in_box, self.target_x, self.target_y

    def return_to_the_box(self, allowed_turns, x_pos, y_pos, direction, target_x, target_y, speed):
        if direction == 0:
            if allowed_turns[3] and np.abs((y_pos + speed) - target_y) \
                    < np.abs((y_pos - speed) - target_y):
                y_pos += speed
                direction = 3
            elif allowed_turns[2] and np.abs((y_pos - speed) - target_y) \
                    < np.abs((y_pos + speed) - target_y):
                y_pos -= speed
                direction = 2
            elif allowed_turns[0] and np.abs((x_pos + speed) - target_x) \
                    < np.abs((x_pos - speed) - target_x):
                x_pos += speed
                direction = 0
            elif not allowed_turns[0]:
                if allowed_turns[3]:
                    direction = 3
                    y_pos += speed
                elif allowed_turns[2]:
                    direction = 2
                    y_pos -= speed
            elif allowed_turns[0]:
                direction = 0
                x_pos += speed
        elif direction == 1:
            if allowed_turns[3] and np.abs((y_pos + speed) - target_y) \
                    < np.abs((y_pos - speed) - target_y):
                y_pos += speed
                direction = 3
            elif allowed_turns[2] and np.abs((y_pos - speed) - target_y) \
                    < np.abs((y_pos + speed) - target_y):
                y_pos -= speed
                direction = 2
            elif allowed_turns[1] and np.abs((x_pos - speed) - target_x) \
                    < np.abs((x_pos + speed) - target_x):
                direction = 1
                x_pos -= speed
            elif not allowed_turns[1]:
                if allowed_turns[3]:
                    direction = 3
                    y_pos += speed
                if allowed_turns[2]:
                    direction = 2
                    y_pos -= speed
            elif allowed_turns[1]:
                direction = 1
                x_pos -= speed
        elif direction == 2:
            if allowed_turns[2] and np.abs((y_pos - speed) - target_y) \
                    < np.abs((y_pos + speed) - target_y):
                direction = 2
                y_pos -= speed
            elif not allowed_turns[2]:
                if allowed_turns[0]:
                    direction = 0
                    x_pos += speed
                elif allowed_turns[1]:
                    direction = 1
                    x_pos -= speed
            elif allowed_turns[2]:
                direction = 2
                y_pos -= speed
        elif direction == 3:
            if allowed_turns[1] and np.abs((x_pos - speed) - target_x) \
                    < np.abs((x_pos + speed) - target_x):
                x_pos -= speed
                direction = 1
            elif allowed_turns[0] and np.abs((x_pos + speed) - target_x) \
                    < np.abs((x_pos - speed) - target_x):
                x_pos += speed
                direction = 0
            elif allowed_turns[3] and np.abs((y_pos + speed) - target_y) \
                    < np.abs((y_pos - speed) - target_y):
                direction = 3
                y_pos += speed
            elif not allowed_turns[3]:
                if allowed_turns[0]:
                    direction = 0
                    x_pos += speed
                elif allowed_turns[1]:
                    direction = 1
                    x_pos -= speed
            elif allowed_turns[3]:
                direction = 3
                y_pos += speed
        if x_pos < 5:
            x_pos = int(self.pacman_game.WIDTH) - self.ghost_height + 1
        if x_pos > int(self.pacman_game.WIDTH) - self.ghost_height + 1:
            x_pos = 5
        return x_pos, y_pos, direction

    def general_movement(self, allowed_turns, direction, x_pos, y_pos, target_x, target_y, speed):
        if x_pos//self.cell_width == target_x//self.cell_width and y_pos//self.cell_height == target_y//self.cell_height:
            if direction == 0 or direction == 1:
                if allowed_turns[3]:
                    direction = 3
                elif allowed_turns[2]:
                    direction = 2
            elif direction == 2 or direction == 3:
                if allowed_turns[0]:
                    direction = 0
                elif allowed_turns[1]:
                    direction = 1
        if direction == 0:
            if allowed_turns[0] and target_x > x_pos or allowed_turns[0]:
                direction = 0
                x_pos += speed
            elif allowed_turns[2] and target_y < y_pos:
                y_pos -= speed
                direction = 2
            elif allowed_turns[3] and target_y > y_pos:
                y_pos += speed
                direction = 3
            elif not allowed_turns[0]:
                if allowed_turns[2]:
                    y_pos -= speed
                    direction = 2
                elif allowed_turns[3]:
                    y_pos += speed
                    direction = 3
            elif allowed_turns[0]:
                x_pos += speed
                direction = 0
        elif direction == 1:
            if allowed_turns[1] and target_x < x_pos or allowed_turns[1]:
                x_pos -= speed
                direction = 1
            elif allowed_turns[2] and target_y < y_pos:
                y_pos -= speed
                direction = 2
            elif allowed_turns[3] and target_y > y_pos:
                y_pos += speed
                direction = 3
            elif not allowed_turns[1]:
                if allowed_turns[2]:
                    y_pos -= speed
                    direction = 2
                elif allowed_turns[3]:
                    y_pos += speed
                    direction = 3
            elif allowed_turns[1]:
                x_pos -= speed
                direction = 1
        elif direction == 2:
            if allowed_turns[2] and y_pos > target_y or allowed_turns[2]:
                y_pos -= speed
                direction = 2
            elif allowed_turns[1] and x_pos > target_x:
                x_pos -= speed
                direction = 1
            elif allowed_turns[0] and x_pos < target_x:
                x_pos += speed
                direction = 0
            elif not allowed_turns[2]:
                if allowed_turns[0]:
                    x_pos += speed
                    direction = 0
                elif allowed_turns[1]:
                    x_pos -= speed
                    direction = 1
            elif allowed_turns[2]:
                y_pos -= speed
                direction = 2
        elif direction == 3:
            if allowed_turns[3] and target_y > y_pos or allowed_turns[3]:
                y_pos += speed
                direction = 3
            elif allowed_turns[1] and x_pos > target_x:
                x_pos -= speed
                direction = 1
            elif allowed_turns[0] and x_pos < target_x:
                x_pos += speed
                direction = 0
            elif not allowed_turns[3]:
                if allowed_turns[0]:
                    x_pos += speed
                    direction = 0
                elif allowed_turns[1]:
                    x_pos -= speed
                    direction = 1
            elif allowed_turns[3]:
                y_pos += speed
                direction = 3
        if x_pos < 5:
            x_pos = int(self.pacman_game.WIDTH) - self.ghost_height + 1
        if x_pos > int(self.pacman_game.WIDTH) - self.ghost_height + 1:
            x_pos = 5
        return x_pos, y_pos, direction


class RedGhost(Ghost):

    def __init__(self, screen, pacman):
        from PacManGame import PacManGame
        self.pacman_game = PacManGame()
        self.x_cell = 2
        self.y_cell = 2
        self.cell_height = (int(self.pacman_game.HEIGHT - 50)) // len(boards)
        self.cell_width = int(self.pacman_game.WIDTH) // len(boards[0])
        self.x_pos = self.x_cell*self.cell_width
        self.y_pos = self.y_cell*self.cell_height - self.cell_height//2
        self.direction = 0
        self.speed = 2
        self.dead = False
        self.powerup = False
        self.in_box = False
        self.eaten = False
        self.screen = screen
        self.pacman = pacman
        self.ghost_width = int(self.pacman_game.WIDTH * 0.05)
        self.ghost_height = int(self.pacman_game.HEIGHT * 0.05)
        self.center_x = self.x_pos + self.ghost_width//2
        self.center_y = self.y_pos + self.ghost_height//2
        self.target_x, self.target_y = self.run_away()
        self.img = pygame.transform.scale(pygame.image.load("ghosts/red.png"),
                                          (self.ghost_width, self.ghost_height))
        super().__init__(self.screen, self.pacman, self.dead, self.eaten,
                         self.powerup, self.in_box, self.ghost_width, self.ghost_height,
                         self.pacman_game, self.cell_width, self.cell_height)
        self.blinky_rect = self.get_rect()

    def run_away(self):
        self.target_x = self.pacman_game.WIDTH
        self.target_y = 0
        return self.target_x, self.target_y

    def update(self):
        self.center_x = self.x_pos + self.ghost_width // 2
        self.center_y = self.y_pos + self.ghost_height // 2
        allowed_turns = self.collisions(self.center_x, self.center_y)
        self.x_pos, self.y_pos, self.direction = self.general_movement(allowed_turns, self.direction,
                                                self.x_pos, self.y_pos, self.target_x, self.target_y, self.speed)
        self.draw(self.img, self.x_pos, self.y_pos)


class BlueGhost(Ghost):
    def __init__(self, screen, pacman):
        from PacManGame import PacManGame
        self.pacman_game = PacManGame()
        self.screen = screen
        self.cell_height = (int(self.pacman_game.HEIGHT - 50)) // len(boards)
        self.cell_width = int(self.pacman_game.WIDTH) // len(boards[0])
        self.x_pos = int(self.pacman_game.WIDTH // 2) + self.cell_width*2
        self.y_pos = int(self.pacman_game.HEIGHT // 2) - self.cell_height*3
        self.direction = 2
        self.speed = 2
        self.dead = False
        self.in_box = True
        self.eaten = False
        self.powerup = False
        self.pacman = pacman
        self.ghost_width = int(self.pacman_game.WIDTH * 0.05)
        self.ghost_height = int(self.pacman_game.HEIGHT * 0.05)
        self.center_x = self.x_pos + self.ghost_width // 2
        self.center_y = self.y_pos + self.ghost_height // 2
        self.blinky_rect = self.get_rect()
        self.target_x, self.target_y = self.run_away()
        self.img = pygame.transform.scale(pygame.image.load("ghosts/blue.png"),
                                          (self.ghost_width, self.ghost_height))
        super().__init__(self.screen, self.pacman, self.dead, self.eaten,
                         self.powerup, self.in_box, self.ghost_width, self.ghost_height,
                         self.pacman_game, self.cell_width, self.cell_height)
        self.is_get_target = False

    def run_away(self):
        self.target_x = 27 * self.cell_width
        self.target_y = 30 * self.cell_height
        return self.target_x, self.target_y

    def exit_from_box(self, center_x, center_y):
        if (int(self.pacman_game.WIDTH // 2) - self.cell_width * 3 < center_x < int(self.pacman_game.WIDTH // 2)
                + self.cell_width * 2 and int(self.pacman_game.HEIGHT // 2) - self.cell_height * 5 < center_y \
                 < int(self.pacman_game.HEIGHT // 2) - self.cell_height * 2):
            self.direction = 2
            self.eaten = False
            self.dead = False
            self.target_x = int(self.pacman_game.WIDTH // 2)
            self.target_y = int(self.pacman_game.HEIGHT // 2) - self.cell_height * 7
        elif not (int(self.pacman_game.WIDTH // 2) - self.cell_width * 3 < center_x < int(self.pacman_game.WIDTH // 2)
                  + self.cell_width * 2 and int(self.pacman_game.HEIGHT // 2) - self.cell_height * 5 < center_y \
                  < int(self.pacman_game.HEIGHT // 2) - self.cell_height * 2):
            self.in_box = False
            self.target_x, self.target_y = self.run_away()
        return self.direction, self.eaten, self.dead, self.in_box, self.target_x, self.target_y

    def update(self):
        self.center_x = self.x_pos + self.ghost_width // 2
        self.center_y = self.y_pos + self.ghost_height // 2
        allowed_turns = self.collisions(self.center_x, self.center_y)
        self.direction, self.eaten, self.dead, self.in_box, self.target_x, self.target_y \
            = self.exit_from_box(self.center_x, self.center_y)
        self.x_pos, self.y_pos, self.direction, self.is_get_target, self.target_x, self.target_y \
            = self.get_target(self.x_pos, self.y_pos, self.target_x, self.target_y, self.direction, self.is_get_target)
        self.x_pos, self.y_pos, self.direction = self.general_movement(allowed_turns, self.direction,
                                                                       self.x_pos, self.y_pos, self.target_x,
                                                                       self.target_y, self.speed)
        self.draw(self.img, self.x_pos, self.y_pos)

    def get_target(self, x_pos, y_pos, target_x, target_y, direction, is_get_target):
        print(x_pos, target_x)
        if not is_get_target:
            if (x_pos + self.cell_width//5) // self.cell_width == target_x // self.cell_width and (
                    y_pos + self.cell_height // 3) // self.cell_height == target_y // self.cell_height:
                is_get_target = True
                target_x, target_y = self.run_away()
        if is_get_target:
            if ((x_pos + self.cell_width // 3) // self.cell_width == 15 and (
                    y_pos + self.cell_height // 3) // self.cell_height == target_y // self.cell_height):
                direction = 2
            target_x = 19 * self.cell_width
            target_y = 24 * self.cell_height
            if ((x_pos + self.cell_height // 3) // self.cell_width == target_x // self.cell_width and y_pos //
                    self.cell_height == target_y // self.cell_height):
                is_get_target = False
        return x_pos, y_pos, direction, is_get_target, target_x, target_y

    def move(self):
        pass


class OrangeGhost(Ghost):

    def __init__(self, screen, pacman):
        from PacManGame import PacManGame
        self.pacman_game = PacManGame()
        self.screen = screen
        self.cell_height = (int(self.pacman_game.HEIGHT - 50)) // len(boards)
        self.cell_width = int(self.pacman_game.WIDTH) // len(boards[0])
        self.x_pos = int(self.pacman_game.WIDTH // 2)
        self.y_pos = int(self.pacman_game.HEIGHT // 2) - self.cell_height*3
        self.direction = 2
        self.speed = 2
        self.dead = False
        self.in_box = True
        self.eaten = False
        self.powerup = False
        self.pacman = pacman
        self.ghost_width = int(self.pacman_game.WIDTH * 0.05)
        self.ghost_height = int(self.pacman_game.HEIGHT * 0.05)
        self.center_x = self.x_pos + self.ghost_width // 2
        self.center_y = self.y_pos + self.ghost_height // 2
        self.blinky_rect = self.get_rect()
        self.target_x, self.target_y = (100, 220)
        self.img = pygame.transform.scale(pygame.image.load("ghosts/orange.png"),
                                          (self.ghost_width, self.ghost_height))
        super().__init__(self.screen, self.pacman, self.dead, self.eaten,
                         self.powerup, self.in_box, self.ghost_width, self.ghost_height,
                         self.pacman_game, self.cell_width, self.cell_height)
        self.is_get_target = False

    def run_away(self):
        self.target_x = 2 * self.cell_width
        self.target_y = 30 * self.cell_height
        return self.target_x, self.target_y

    def exit_from_box(self, center_x, center_y):
        if (int(self.pacman_game.WIDTH // 2) - self.cell_width * 3 < center_x < int(self.pacman_game.WIDTH // 2)
                + self.cell_width * 2 and int(self.pacman_game.HEIGHT // 2) - self.cell_height*5 < center_y \
                < int(self.pacman_game.HEIGHT // 2) - self.cell_height*2):
            self.direction = 2
            self.eaten = False
            self.dead = False
            self.target_x = int(self.pacman_game.WIDTH // 2)
            self.target_y = int(self.pacman_game.HEIGHT // 2) - self.cell_height*7
        elif not (int(self.pacman_game.WIDTH // 2) - self.cell_width * 3 < center_x < int(self.pacman_game.WIDTH // 2)
                  + self.cell_width * 2 and int(self.pacman_game.HEIGHT // 2) - self.cell_height*5 < center_y \
                  < int(self.pacman_game.HEIGHT // 2) - self.cell_height*2):
            self.in_box = False
            self.target_x, self.target_y = self.run_away()
        return self.direction, self.eaten, self.dead, self.in_box, self.target_x, self.target_y

    def update(self):
        self.center_x = self.x_pos + self.ghost_width // 2
        self.center_y = self.y_pos + self.ghost_height // 2
        allowed_turns = self.collisions(self.center_x, self.center_y)
        self.direction, self.eaten, self.dead, self.in_box, self.target_x, self.target_y\
            = self.exit_from_box(self.center_x, self.center_y)
        self.x_pos, self.y_pos, self.direction, self.is_get_target, self.target_x, self.target_y \
            = self.get_target(self.x_pos, self.y_pos, self.target_x, self.target_y, self.direction, self.is_get_target)
        self.x_pos, self.y_pos, self.direction = self.general_movement(allowed_turns, self.direction,
                                                                       self.x_pos, self.y_pos, self.target_x,
                                                                       self.target_y, self.speed)
        self.draw(self.img, self.x_pos, self.y_pos)

    def get_target(self, x_pos, y_pos, target_x, target_y, direction, is_get_target):
        if not is_get_target:
            if x_pos // self.cell_width == target_x // self.cell_width and (
                    y_pos + self.cell_height // 3) // self.cell_height == target_y // self.cell_height:
                is_get_target = True
                target_x, target_y = self.run_away()
        if is_get_target:
            if ((x_pos + self.cell_width//3)//self.cell_width == 13 and (y_pos + self.cell_height//3)//self.cell_height
                    == target_y//self.cell_height):
                direction = 2
            target_x = 10 * self.cell_width
            target_y = 24 * self.cell_height
            if ((x_pos + self.cell_height//3)//self.cell_width == target_x//self.cell_width and y_pos//self.cell_height
                    == target_y//self.cell_height):
                is_get_target = False
        return x_pos, y_pos, direction, is_get_target, target_x, target_y


class PinkGhost(Ghost):
    def __init__(self, screen, pacman):
        from PacManGame import PacManGame
        self.pacman_game = PacManGame()
        self.screen = screen
        self.cell_height = (int(self.pacman_game.HEIGHT - 50)) // len(boards)
        self.cell_width = int(self.pacman_game.WIDTH) // len(boards[0])
        self.x_pos = int(self.pacman_game.WIDTH // 2) - self.cell_width*2
        self.y_pos = int(self.pacman_game.HEIGHT // 2) - self.cell_height*3
        self.direction = 2
        self.speed = 2
        self.dead = False
        self.in_box = True
        self.eaten = False
        self.powerup = False
        self.pacman = pacman
        self.ghost_width = int(self.pacman_game.WIDTH * 0.05)
        self.ghost_height = int(self.pacman_game.HEIGHT * 0.05)
        self.center_x = self.x_pos + self.ghost_width // 2
        self.center_y = self.y_pos + self.ghost_height // 2
        self.blinky_rect = self.get_rect()
        self.target_x, self.target_y = self.run_away()
        self.img = pygame.transform.scale(pygame.image.load("ghosts/pink.png"),
                                          (self.ghost_width, self.ghost_height))
        super().__init__(self.screen, self.pacman, self.dead, self.eaten,
                         self.powerup, self.in_box, self.ghost_width, self.ghost_height,
                         self.pacman_game, self.cell_width, self.cell_height)
        self.is_get_target = False

    def run_away(self):
        self.target_x = 2*self.cell_width
        self.target_y = 2*self.cell_height
        return self.target_x, self.target_y

    def exit_from_box(self, center_x, center_y):
        if (int(self.pacman_game.WIDTH // 2) - self.cell_width * 3 < center_x < int(self.pacman_game.WIDTH // 2)
                + self.cell_width * 2 and int(self.pacman_game.HEIGHT // 2) - self.cell_height*5 < center_y \
                < int(self.pacman_game.HEIGHT // 2) - self.cell_height*2):
            self.direction = 2
            self.eaten = False
            self.dead = False
            self.target_x = int(self.pacman_game.WIDTH // 2)
            self.target_y = int(self.pacman_game.HEIGHT // 2) - self.cell_height*7
        elif not (int(self.pacman_game.WIDTH // 2) - self.cell_width * 3 < center_x < int(self.pacman_game.WIDTH // 2)
                  + self.cell_width * 2 and int(self.pacman_game.HEIGHT // 2) - self.cell_height*5 < center_y \
                  < int(self.pacman_game.HEIGHT // 2) - self.cell_height*2):
            self.in_box = False
            self.target_x, self.target_y = self.run_away()
        return self.direction, self.eaten, self.dead, self.in_box, self.target_x, self.target_y

    def update(self):
        self.center_x = self.x_pos + self.ghost_width // 2
        self.center_y = self.y_pos + self.ghost_height // 2
        allowed_turns = self.collisions(self.center_x, self.center_y)
        self.direction, self.eaten, self.dead, self.in_box, self.target_x, self.target_y \
            = self.exit_from_box(self.center_x, self.center_y)
        self.x_pos, self.y_pos, self.direction = self.general_movement(allowed_turns, self.direction,
                                                self.x_pos, self.y_pos, self.target_x, self.target_y, self.speed)
        self.draw(self.img, self.x_pos, self.y_pos)

    def move(self):
        pass



