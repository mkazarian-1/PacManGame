from abc import ABC, abstractmethod
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
        #if not self.powerup and not self.dead or (self.eaten and self.powerup and self.dead):
        if not self.powerup and not self.dead:
            self.screen.blit(self.img, (self.x_pos, self.y_pos))
        elif self.powerup and not self.dead and not self.eaten:
            self.screen.blit(self.img_spooked, (self.x_pos, self.y_pos))
        elif self.powerup and self.eaten and self.dead:
            self.screen.blit(self.img_dead, (self.x_pos, self.y_pos))

    def get_rect(self):
        ghost_rect = pygame.rect.Rect((self.center_x, self.center_y), (30, 30))
        return ghost_rect

    def pacman_collision(self):
        if pygame.Rect.colliderect(self.ghost_rect, self.pacman_rect) and self.powerup and not self.dead:
            self.dead = True
            self.eaten = True
            self.target_x = 300
            self.target_y = 350
            self.speed = 4
        return self.dead, self.eaten, self.target_x, self.target_y, self.speed

    def collisions(self):
        cell_height = (int(self.pacman_game.HEIGHT - 50))//len(boards)
        cell_width = int(self.pacman_game.WIDTH)//len(boards[0])
        num1 = cell_width//2
        num2 = cell_height//2
        self.allowed_turns = [False, False, False, False]
        if self.in_box and boards[(self.center_y - num2) // cell_height][self.center_x // cell_width] == 9:
            self.allowed_turns[2] = True
            self.in_box = False
        else:
            if boards[(self.center_y - num2) // cell_height][self.center_x // cell_width] < 3 \
                    or boards[(self.center_y - num2) // cell_height][self.center_x // cell_width] == 9:
                self.allowed_turns[2] = True
            if boards[self.center_y // cell_height][(self.center_x - num1) // cell_width] < 3 \
                    or boards[self.center_y // cell_height][(self.center_x - num1) // cell_width] == 9:
                self.allowed_turns[1] = True
            if boards[(self.center_y + num2) // cell_height][self.center_x // cell_width] < 3 \
                    or boards[(self.center_y + num2) // cell_height][self.center_x // cell_width] == 9:
                self.allowed_turns[3] = True
            if boards[self.center_y // cell_height][(self.center_x + num1) // cell_width] < 3 \
                    or boards[self.center_y // cell_height][(self.center_x + num1) // cell_width] == 9:
                self.allowed_turns[0] = True
        return self.allowed_turns

    @abstractmethod
    def move(self):
        ...


class RedGhost(Ghost):
    def move(self):
        if self.direction == 0:
            if self.allowed_turns[0] and self.target_x > self.x_pos:
                self.x_pos += self.speed
            elif self.allowed_turns[0]:
                self.x_pos += self.speed
                self.direction = 0
            elif not self.allowed_turns[0]:
                if self.allowed_turns[3] and self.target_y > self.y_pos:
                    self.y_pos += self.speed
                    self.direction = 3
                elif self.allowed_turns[2] and self.target_y < self.y_pos:
                    self.y_pos -= self.speed
                    self.direction = 2
                elif self.allowed_turns[1] and self.target_x < self.x_pos:
                    self.x_pos -= self.speed
                    self.direction = 1
                elif self.allowed_turns[3]:
                    self.y_pos += self.speed
                    self.direction = 3
                elif self.allowed_turns[2]:
                    self.y_pos -= self.speed
                    self.direction = 2
                elif self.allowed_turns[1]:
                    self.x_pos -= self.speed
                    self.direction = 1
        elif self.direction == 1:
            if self.allowed_turns[1] and self.target_x < self.x_pos:
                self.x_pos -= self.speed
            elif self.allowed_turns[1]:
                self.x_pos -= self.speed
                self.direction = 1
            elif not self.allowed_turns[1]:
                if self.allowed_turns[3] and self.target_y > self.y_pos:
                    self.y_pos += self.speed
                    self.direction = 3
                elif self.allowed_turns[2] and self.target_y < self.y_pos:
                    self.y_pos -= self.speed
                    self.direction = 2
                elif self.allowed_turns[0] and self.target_x > self.x_pos:
                    self.x_pos += self.speed
                    self.direction = 0
                elif self.allowed_turns[3]:
                    self.y_pos += self.speed
                    self.direction = 3
                elif self.allowed_turns[2]:
                    self.y_pos -= self.speed
                    self.direction = 2
                elif self.allowed_turns[0]:
                    self.x_pos += self.speed
                    self.direction = 0
        elif self.direction == 2:
            if self.allowed_turns[2] and self.target_y < self.y_pos:
                self.y_pos -= self.speed
            elif self.allowed_turns[2]:
                self.y_pos -= self.speed
                self.direction = 2
            elif not self.allowed_turns[2]:
                if self.allowed_turns[1] and self.target_x < self.x_pos:
                    self.x_pos -= self.speed
                    self.direction = 1
                elif self.allowed_turns[0] and self.target_x > self.x_pos:
                    self.x_pos += self.speed
                    self.direction = 0
                elif self.allowed_turns[3] and self.target_y > self.y_pos:
                    self.y_pos += self.speed
                    self.direction = 3
                elif self.allowed_turns[1]:
                    self.x_pos -= self.speed
                    self.direction = 1
                elif self.allowed_turns[0]:
                    self.x_pos += self.speed
                    self.direction = 0
                elif self.allowed_turns[3]:
                    self.y_pos += self.speed
                    self.direction = 3
        elif self.direction == 3:
            if self.allowed_turns[3] and self.target_y > self.y_pos:
                self.y_pos += self.speed
            elif self.allowed_turns[3]:
                self.y_pos += self.speed
                self.direction = 3
            elif not self.allowed_turns[3]:
                if self.allowed_turns[0] and self.target_x > self.x_pos:
                    self.x_pos += self.speed
                    self.direction = 0
                elif self.allowed_turns[1] and self.target_x < self.x_pos:
                    self.x_pos -= self.speed
                    self.direction = 1
                elif self.allowed_turns[2] and self.target_y < self.y_pos:
                    self.y_pos -= self.speed
                    self.direction = 2
                elif self.allowed_turns[0]:
                    self.x_pos += self.speed
                    self.direction = 0
                elif self.allowed_turns[1]:
                    self.x_pos -= self.speed
                    self.direction = 1
                elif self.allowed_turns[2]:
                    self.y_pos -= self.speed
                    self.direction = 2
        if self.x_pos < 10:
            self.x_pos = self.pacman_game.WIDTH + 10
        elif self.x_pos > self.pacman_game.WIDTH + 10:
            self.x_pos = -10
        return self.x_pos, self.y_pos, self.direction


class BlueGhost(Ghost):
    def move(self):
        pass


class OrangeGhost(Ghost):
    def move(self):
        pass


class PinkGhost(Ghost):
    def move(self):
        pass
