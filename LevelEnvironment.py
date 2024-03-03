import math
from abc import ABC, abstractmethod
import pygame

import Score


class IDrawAble(ABC):
    @abstractmethod
    def draw(self):
        ...


class IActionable(ABC):
    @abstractmethod
    def action(self):
        ...


class IWallAble(ABC):
    pass


class Food(IDrawAble, IActionable):

    def __init__(self, screen, x, y, cell_width, cell_height, color, score: Score.PlayerScore):
        self.screen = screen
        self.x = x
        self.y = y
        self.cell_width = cell_width
        self.cell_height = cell_height
        self.color = color
        self.score = score

    def action(self):
        self.score.increase_score(10)

    def draw(self):
        pygame.draw.circle(self.screen, self.color,
                           (self.x * self.cell_width + (self.cell_width / 2),
                            self.y * self.cell_height + (self.cell_height / 2)), 4)


class Energiser(IDrawAble, IActionable):
    def __init__(self, screen, x, y, cell_width, cell_height, level_loop_counter, color, score: Score.PlayerScore):
        self.screen = screen
        self.x = x
        self.y = y
        self.cell_width = cell_width
        self.cell_height = cell_height
        self.level_loop_counter = level_loop_counter
        self.color = color
        self.score = score

    def action(self):
        self.score.increase_score(100)

    def draw(self):
        if self.level_loop_counter.get() > 10:
            pygame.draw.circle(self.screen, self.color,
                               (self.x * self.cell_width + (self.cell_width / 2),
                                self.y * self.cell_height + (self.cell_height / 2)), 8)


class Wall(IDrawAble, IWallAble):
    def __init__(self, screen, x, y, cell_width, cell_height, position, color):
        self.screen = screen
        self.x = x
        self.y = y
        self.cell_width = cell_width
        self.cell_height = cell_height
        self.position = position
        self.color = color

    def draw(self):
        if self.position == 1:
            pygame.draw.line(self.screen, self.color,
                             (self.x * self.cell_width + (self.cell_width / 2), self.y * self.cell_height),
                             (self.x * self.cell_width + (self.cell_width / 2), (self.y + 1) * self.cell_height), 3)

        else:
            pygame.draw.line(self.screen, self.color,
                             (self.x * self.cell_width, self.y * self.cell_height + (self.cell_height / 2)),
                             ((self.x + 1) * self.cell_width, self.y * self.cell_height + (self.cell_height / 2)), 3)


class Door(Wall):
    pass


class CurvedWall(IDrawAble,IWallAble):

    def __init__(self, screen, x, y, cell_width, cell_height, position, color):
        self.screen = screen
        self.x = x
        self.y = y
        self.cell_width = cell_width
        self.cell_height = cell_height
        self.position = position
        self.color = color

    def draw(self):
        retreat = 2
        if self.position == 1:
            pygame.draw.arc(self.screen, self.color, [(self.x * self.cell_width - (self.cell_width / 2)),
                                                      (self.y * self.cell_height + (self.cell_height / 2)),
                                                      self.cell_width + retreat, self.cell_height - retreat], 0,
                            math.pi / 2, 3)
        elif self.position == 2:
            pygame.draw.arc(self.screen, self.color, [(self.x * self.cell_width + (self.cell_width / 2)),
                                                      (self.y * self.cell_height + (self.cell_height / 2)),
                                                      self.cell_width - retreat, self.cell_height - retreat],
                            math.pi / 2, math.pi, 3)
        elif self.position == 3:
            pygame.draw.arc(self.screen, self.color, [(self.x * self.cell_width + (self.cell_width / 2)),
                                                      (self.y * self.cell_height - (self.cell_height / 2)),
                                                      self.cell_width - retreat, self.cell_height + retreat],
                            -1 * math.pi, math.pi * -1 / 2, 3)
        else:
            pygame.draw.arc(self.screen, self.color, [(self.x * self.cell_width - (self.cell_width / 2)),
                                                      (self.y * self.cell_height - (self.cell_height / 2)),
                                                      self.cell_width + retreat, self.cell_height + retreat],
                            math.pi * -1 / 2, 0, 3)


class BlankSpace(IDrawAble):
    def draw(self):
        pass
