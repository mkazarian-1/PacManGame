from abc import ABC, abstractmethod

import numpy as np

from LevelMap import boards
import pygame


class Ghost(ABC):
    def __init__(self, x_pos, y_pos, direction, img, dead, speed, powerup, in_box, eaten, screen, img_spooked,
                 img_dead, target_x, target_y, pacman_rect):
        from PacManGame import PacManGame
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.speed = speed
        self.powerup = powerup
        self.eaten = eaten
        self.dead = dead
        self.screen = screen
        self.in_box = in_box
        self.img = img
        self.direction = direction
        self.img_spooked = img_spooked
        self.img_dead = img_dead
        self.center_x = self.x_pos + 20
        self.center_y = self.y_pos + 20
        self.pacman_rect = pacman_rect
        self.ghost_rect = self.get_rect()
        self.dead = dead
        self.eaten = eaten
        self.pacman_game = PacManGame()
        self.target_x = target_x
        self.target_y = target_y
        self.allowed_turns = self.collisions()

    def draw(self):
        if not self.powerup and not self.dead and not self.eaten \
                or (self.powerup and self.dead and self.eaten and self.in_box):
            self.screen.blit(self.img, (self.x_pos, self.y_pos))
        elif self.powerup and not self.dead and not self.eaten:
            self.screen.blit(self.img_spooked, (self.x_pos, self.y_pos))
        elif self.powerup and self.eaten and self.dead:
            self.screen.blit(self.img_dead, (self.x_pos, self.y_pos))

    def get_rect(self):
        ghost_rect = pygame.rect.Rect((self.center_x, self.center_y), (30, 30))
        return ghost_rect

    def pacman_collision(self):
        if (pygame.Rect.colliderect(self.ghost_rect, self.pacman_rect) and self.powerup and not self.dead
                and not self.eaten):
            self.dead = True
            self.eaten = True
            self.target_x = int(self.pacman_game.WIDTH // 2) - 10
            self.target_y = int(self.pacman_game.HEIGHT // 2) - 100
            self.speed *= 2
        return self.dead, self.eaten, self.target_x, self.target_y, self.speed

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

    def collisions(self):
        cell_height = (int(self.pacman_game.HEIGHT - 50))//len(boards)
        cell_width = int(self.pacman_game.WIDTH)//len(boards[0])
        num1 = cell_width//2
        num2 = cell_height//2
        self.allowed_turns = [False, False, False, False]
        if self.in_box and boards[(self.center_y - num2) // cell_height][self.center_x // cell_width] == 9 or self.in_box:
            self.allowed_turns[2] = True
            self.in_box = False
        elif not self.in_box:
            if boards[self.center_y // cell_height][(self.center_x + num1) // cell_width] < 3 \
                    or boards[self.center_y // cell_height][(self.center_x + num1) // cell_width] == 9:
                self.allowed_turns[0] = True
            if boards[self.center_y // cell_height][(self.center_x - num1) // cell_width] < 3 \
                    or boards[self.center_y // cell_height][(self.center_x - num1) // cell_width] == 9:
                self.allowed_turns[1] = True
            if boards[(self.center_y - num2) // cell_height][self.center_x // cell_width] < 3 \
                    or boards[(self.center_y - num2) // cell_height][self.center_x // cell_width] == 9:
                self.allowed_turns[2] = True
            if boards[(self.center_y + num2) // cell_height][self.center_x // cell_width] < 3 \
                    or boards[(self.center_y + num2) // cell_height][self.center_x // cell_width] == 9:
                self.allowed_turns[3] = True
        return self.allowed_turns

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

    def return_to_the_box(self):
        if self.direction == 0:
            if self.allowed_turns[3] and np.abs((self.y_pos + self.speed) - self.target_y) \
                    < np.abs((self.y_pos - self.speed) - self.target_y):
                self.y_pos += self.speed
                self.direction = 3
            elif self.allowed_turns[2] and np.abs((self.y_pos - self.speed) - self.target_y) \
                    < np.abs((self.y_pos + self.speed) - self.target_y):
                self.y_pos -= self.speed
                self.direction = 2
            elif self.allowed_turns[0] and np.abs((self.x_pos + self.speed) - self.target_x) \
                    < np.abs((self.x_pos - self.speed) - self.target_x):
                self.x_pos += self.speed
                self.direction = 0
            elif not self.allowed_turns[0]:
                if self.allowed_turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.allowed_turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
            elif self.allowed_turns[0]:
                self.direction = 0
                self.x_pos += self.speed
        elif self.direction == 1:
            if self.allowed_turns[3] and np.abs((self.y_pos + self.speed) - self.target_y) \
                    < np.abs((self.y_pos - self.speed) - self.target_y):
                self.y_pos += self.speed
                self.direction = 3
            elif self.allowed_turns[2] and np.abs((self.y_pos - self.speed) - self.target_y) \
                    < np.abs((self.y_pos + self.speed) - self.target_y):
                self.y_pos -= self.speed
                self.direction = 2
            elif self.allowed_turns[1] and np.abs((self.x_pos - self.speed) - self.target_x) \
                    < np.abs((self.x_pos + self.speed) - self.target_x):
                self.direction = 1
                self.x_pos -= self.speed
            elif not self.allowed_turns[1]:
                if self.allowed_turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.allowed_turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
            elif self.allowed_turns[1]:
                self.direction = 1
                self.x_pos -= self.speed
        elif self.direction == 2:
            if self.allowed_turns[2] and np.abs((self.y_pos - self.speed) - self.target_y) \
                    < np.abs((self.y_pos + self.speed) - self.target_y):
                self.direction = 2
                self.y_pos -= self.speed
            elif not self.allowed_turns[2]:
                if self.allowed_turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.allowed_turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.allowed_turns[2]:
                self.direction = 2
                self.y_pos -= self.speed
        elif self.direction == 3:
            if self.allowed_turns[1] and np.abs((self.x_pos - self.speed) - self.target_x) \
                    < np.abs((self.x_pos + self.speed) - self.target_x):
                self.x_pos -= self.speed
                self.direction = 1
            elif self.allowed_turns[0] and np.abs((self.x_pos + self.speed) - self.target_x) \
                    < np.abs((self.x_pos - self.speed) - self.target_x):
                self.x_pos += self.speed
                self.direction = 0
            elif self.allowed_turns[3] and np.abs((self.y_pos + self.speed) - self.target_y) \
                    < np.abs((self.y_pos - self.speed) - self.target_y):
                self.direction = 3
                self.y_pos += self.speed
            elif not self.allowed_turns[3]:
                if self.allowed_turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.allowed_turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.allowed_turns[3]:
                self.direction = 3
                self.y_pos += self.speed
        if self.x_pos < 5:
            self.x_pos = int(self.pacman_game.WIDTH) - int(self.pacman_game.HEIGHT * 0.05) + 1
        if self.x_pos > int(self.pacman_game.WIDTH) - int(self.pacman_game.HEIGHT * 0.05) + 1:
            self.x_pos = 5
        return self.x_pos, self.y_pos, self.direction

    def general_movement(self):
        if self.direction == 0:
            if self.allowed_turns[0] and self.target_x > self.x_pos:
                self.x_pos += self.speed
            elif not self.allowed_turns[0]:
                if self.allowed_turns[3] and self.target_y > self.y_pos:
                    self.y_pos += self.speed
                    self.direction = 3
                elif self.allowed_turns[2] and self.target_y < self.y_pos:
                    self.y_pos -= self.speed
                    self.direction = 2
                elif self.allowed_turns[3]:
                    self.y_pos += self.speed
                    self.direction = 3
                elif self.allowed_turns[2]:
                    self.y_pos -= self.speed
                    self.direction = 2
            elif self.allowed_turns[0]:
                self.x_pos += self.speed
                self.direction = 0
        elif self.direction == 1:
            if self.allowed_turns[1] and self.target_x < self.x_pos:
                self.x_pos -= self.speed
            elif not self.allowed_turns[1]:
                if self.allowed_turns[3] and self.target_y > self.y_pos:
                    self.y_pos += self.speed
                    self.direction = 3
                elif self.allowed_turns[2] and self.target_y < self.y_pos:
                    self.y_pos -= self.speed
                    self.direction = 2
                elif self.allowed_turns[3]:
                    self.y_pos += self.speed
                    self.direction = 3
                elif self.allowed_turns[2]:
                    self.y_pos -= self.speed
                    self.direction = 2
            elif self.allowed_turns[1]:
                self.x_pos -= self.speed
                self.direction = 1
        elif self.direction == 2:
            if self.allowed_turns[2] and self.y_pos > self.target_y:
                self.y_pos -= self.speed
            elif not self.allowed_turns[2]:
                if self.allowed_turns[1] and self.target_x < self.x_pos:
                    self.x_pos -= self.speed
                    self.direction = 1
                elif self.allowed_turns[0] and self.target_x > self.x_pos:
                    self.x_pos += self.speed
                    self.direction = 0
                elif self.allowed_turns[1]:
                    self.x_pos -= self.speed
                    self.direction = 1
                elif self.allowed_turns[0]:
                    self.x_pos += self.speed
                    self.direction = 0
            elif self.allowed_turns[2]:
                self.y_pos -= self.speed
                self.direction = 2
        elif self.direction == 3:
            if self.allowed_turns[3] and self.target_y > self.y_pos:
                self.y_pos += self.speed
            elif not self.allowed_turns[3]:
                if self.allowed_turns[0] and self.target_x > self.x_pos:
                    self.x_pos += self.speed
                    self.direction = 0
                elif self.allowed_turns[1] and self.target_x < self.x_pos:
                    self.x_pos -= self.speed
                    self.direction = 1
                elif self.allowed_turns[0]:
                    self.x_pos += self.speed
                    self.direction = 0
                elif self.allowed_turns[1]:
                    self.x_pos -= self.speed
                    self.direction = 1
            elif self.allowed_turns[3]:
                self.y_pos += self.speed
                self.direction = 3
        if self.x_pos < 5:
            self.x_pos = int(self.pacman_game.WIDTH) - int(self.pacman_game.HEIGHT * 0.05) + 1
        if self.x_pos > int(self.pacman_game.WIDTH) - int(self.pacman_game.HEIGHT * 0.05) + 1:
            self.x_pos = 5
        return self.x_pos, self.y_pos, self.direction

    @abstractmethod
    def move(self):
        ...


class RedGhost(Ghost):

    def run_away(self):
        self.target_x = self.pacman_game.WIDTH
        self.target_y = 0
        return self.target_x, self.target_y

    def move(self):
        return self.general_movement()


class BlueGhost(Ghost):
    def move(self):
        pass


class OrangeGhost(Ghost):

    def run_away(self):
        self.target_x = 0
        self.target_y = self.pacman_game.HEIGHT
        return self.target_x, self.target_y

    def get_target(self):
        cell_height = (int(self.pacman_game.HEIGHT - 50)) // len(boards)
        cell_width = int(self.pacman_game.WIDTH) // len(boards[0])
        ghost_pos = (self.x_pos//cell_width, self.y_pos//cell_height)
        pacman_pos = (self.target_x//cell_width, self.target_y//cell_height)
        count = 0
        # if ghost_pos[0] != pacman_pos[0] and ghost_pos[1] != pacman_pos[1]:
        #     if ghost_pos[0] < pacman_pos[0]:
        #         if boards[ghost_pos[1]][ghost_pos[0] + 1] < 3 and ghost_pos[0] + 1 < len(boards[0]):
        #             ghost_pos = (ghost_pos[0] + 1, ghost_pos[1])
        #             count += 1
        #         elif ghost_pos[1] < pacman_pos[1]:
        #             if boards[ghost_pos[1] + 1][ghost_pos[0]] < 3 and ghost_pos[1] + 1 < len(boards):
        #                 ghost_pos = (ghost_pos[0], ghost_pos[1] + 1)
        #                 count += 1
        #         elif ghost_pos[1] > pacman_pos[1]:
        #             if boards[ghost_pos[1] - 1][ghost_pos[0]] < 3 and ghost_pos[1] - 1 >= 0:
        #                 ghost_pos = (ghost_pos[0], ghost_pos[1] - 1)
        #                 count += 1
        #     elif ghost_pos[0] > pacman_pos[0]:
        #         if boards[ghost_pos[1]][ghost_pos[0] - 1] < 3 and ghost_pos[0] - 1 >= 0:
        #             ghost_pos = (ghost_pos[0] - 1, ghost_pos[1])
        #             count += 1
        #         elif ghost_pos[1] < pacman_pos[1]:
        #             if boards[ghost_pos[1] + 1][ghost_pos[0]] < 3 and ghost_pos[1] + 1 < len(boards):
        #                 ghost_pos = (ghost_pos[0], ghost_pos[1] + 1)
        #                 count += 1
        #         elif ghost_pos[1] > pacman_pos[1]:
        #             if boards[ghost_pos[1] - 1][ghost_pos[0]] < 3 and ghost_pos[1] - 1 >= 0:
        #                 ghost_pos = (ghost_pos[0], ghost_pos[1] - 1)
        #                 count += 1
        #     elif ghost_pos[1] > pacman_pos[1]:
        #         if boards[ghost_pos[1] - 1][ghost_pos[0]] < 3 and ghost_pos[1] - 1 >= 0:
        #             ghost_pos = (ghost_pos[0], ghost_pos[1] - 1)
        #             count += 1
        #         elif ghost_pos[0] < pacman_pos[0]:
        #             if boards[ghost_pos[1]][ghost_pos[0] + 1] < 3 and ghost_pos[0] + 1 < len(boards):
        #                 ghost_pos = (ghost_pos[0] + 1, ghost_pos[1])
        #                 count += 1
        #         elif ghost_pos[0] > pacman_pos[0]:
        #             if boards[ghost_pos[1]][ghost_pos[0] - 1] < 3 and ghost_pos[0] - 1 >= 0:
        #                 ghost_pos = (ghost_pos[0] - 1, ghost_pos[1])
        #                 count += 1
        #     elif ghost_pos[1] < pacman_pos[1]:
        #         if boards[ghost_pos[1] + 1][ghost_pos[0]] < 3 and ghost_pos[1] + 1 < len(boards):
        #             ghost_pos = (ghost_pos[0], ghost_pos[1] + 1)
        #             count += 1
        #         elif ghost_pos[0] < pacman_pos[0]:
        #             if boards[ghost_pos[0]][ghost_pos[1] + 1] < 3 and ghost_pos[1] + 1 < len(boards):
        #                 ghost_pos = (ghost_pos[0], ghost_pos[1] + 1)
        #                 count += 1
        #         elif ghost_pos[0] > pacman_pos[0]:
        #             if boards[pacman_pos[1]][pacman_pos[0] + 1] < 3 and pacman_pos[0] + 1 < len(boards[0]):
        #                 pacman_pos = (pacman_pos[0], pacman_pos[1] + 1)
        #                 count += 1
                    # if ghost_pos[0] == pacman_pos[0]:
                    #     if ghost_pos[1] < pacman_pos[1]:
                    #         if boards[ghost_pos[1] + 1][ghost_pos[0]] < 3 and ghost_pos[1] + 1 < len(boards):
                    #             ghost_pos = (ghost_pos[0], ghost_pos[1] + 1)
                    #             count += 1
                    #     elif ghost_pos[1] > pacman_pos[1]:
                    #         if boards[pacman_pos[1] - 1][pacman_pos[0]] < 3 and pacman_pos[1] - 1 >= 0:
                    #             pacman_pos = (pacman_pos[0], pacman_pos[1] - 1)
                    #             count += 1
                    # if ghost_pos[1] == pacman_pos[1]:
                    #     if ghost_pos[0] < pacman_pos[0]:
                    #         if boards[ghost_pos[1]][ghost_pos[0] + 1] < 3 and ghost_pos[0] + 1 < len(boards[0]):
                    #             ghost_pos = (ghost_pos[0] + 1, ghost_pos[1])
                    #             count += 1
                    #     elif ghost_pos[0] > pacman_pos[0]:
                    #         if boards[pacman_pos[1]][pacman_pos[0] + 1] < 3 and pacman_pos[0] + 1 < len(boards[0]):
                    #             pacman_pos = (pacman_pos[0] + 1, pacman_pos[1])
                    #             count += 1
        return np.abs(ghost_pos[0] - pacman_pos[0]) + np.abs(ghost_pos[1] - pacman_pos[1])

    def move(self):
        # distance = self.get_target()
        # print(distance)
        # if distance <= 8:
        #     self.direction = self.spooked()
        #     self.target_x, self.target_y = self.run_away()
        if self.direction == 0:
            if self.allowed_turns[0] and self.target_x > self.x_pos:
                self.direction = 0
                self.x_pos += self.speed
            elif self.allowed_turns[2] and self.target_y < self.y_pos:
                self.y_pos -= self.speed
                self.direction = 2
            elif self.allowed_turns[3] and self.target_y > self.y_pos:
                self.y_pos += self.speed
                self.direction = 3
            elif not self.allowed_turns[0]:
                if self.allowed_turns[2]:
                    self.y_pos -= self.speed
                    self.direction = 2
                elif self.allowed_turns[3]:
                    self.y_pos += self.speed
                    self.direction = 3
            elif self.allowed_turns[0]:
                self.x_pos += self.speed
                self.direction = 0
        elif self.direction == 1:
            if self.allowed_turns[1] and self.target_x < self.x_pos:
                self.x_pos -= self.speed
                self.direction = 1
            elif self.allowed_turns[2] and self.target_y < self.y_pos:
                self.y_pos -= self.speed
                self.direction = 2
            elif self.allowed_turns[3] and self.target_y > self.y_pos:
                self.y_pos += self.speed
                self.direction = 3
            elif not self.allowed_turns[1]:
                if self.allowed_turns[2]:
                    self.y_pos -= self.speed
                    self.direction = 2
                elif self.allowed_turns[3]:
                    self.y_pos += self.speed
                    self.direction = 3
            elif self.allowed_turns[1]:
                self.x_pos -= self.speed
                self.direction = 1
        elif self.direction == 2:
            if self.allowed_turns[2] and self.y_pos > self.target_y:
                self.y_pos -= self.speed
                self.direction = 2
            elif self.allowed_turns[0] and self.x_pos < self.target_x:
                self.x_pos += self.speed
                self.direction = 0
            elif self.allowed_turns[1] and self.x_pos > self.target_x:
                self.x_pos -= self.speed
                self.direction = 1
            elif not self.allowed_turns[2]:
                if self.allowed_turns[0]:
                    self.x_pos += self.speed
                    self.direction = 0
                elif self.allowed_turns[1]:
                    self.x_pos -= self.speed
                    self.direction = 1
            elif self.allowed_turns[2]:
                self.y_pos -= self.speed
                self.direction = 2
        elif self.direction == 3:
            if self.allowed_turns[3] and self.target_y > self.y_pos:
                self.y_pos += self.speed
                self.direction = 3
            elif self.allowed_turns[0] and self.x_pos < self.target_x:
                self.x_pos += self.speed
                self.direction = 0
            elif self.allowed_turns[1] and self.x_pos > self.target_x:
                self.x_pos -= self.speed
                self.direction = 1
            elif not self.allowed_turns[3]:
                if self.allowed_turns[0]:
                    self.x_pos += self.speed
                    self.direction = 0
                elif self.allowed_turns[1]:
                    self.x_pos -= self.speed
                    self.direction = 1
            elif self.allowed_turns[3]:
                self.y_pos += self.speed
                self.direction = 3
        if self.x_pos < 5:
            self.x_pos = int(self.pacman_game.WIDTH) - int(self.pacman_game.HEIGHT * 0.05) + 1
        if self.x_pos > int(self.pacman_game.WIDTH) - int(self.pacman_game.HEIGHT * 0.05) + 1:
            self.x_pos = 5
        return self.x_pos, self.y_pos, self.direction


class PinkGhost(Ghost):
    def move(self):
        pass



