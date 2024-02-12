import pygame
import numpy as np
import LevelEnvironment


class LevelBuilder:
    level_color = "blue"

    def __init__(self, screen, width, height, level_map, level_loop_counter):
        self.screen = screen
        self.width = width
        self.height = height
        self.level_map = level_map
        self.level_loop_counter = level_loop_counter

    def build(self):

        cell_height = (self.height - 50) / len(self.level_map)
        cell_width = self.width / len(self.level_map[0])

        level_environment = [[LevelEnvironment.BlankSpace() for _ in range(len(self.level_map[0]))] for _ in range(len(self.level_map))]

        for y in range(len(self.level_map)):
            for x in range(len(self.level_map[0])):
                if self.level_map[y][x] == 1:
                    level_environment[y][x] = (LevelEnvironment
                                               .Food(self.screen, x, y, cell_width, cell_height, "white"))
                elif self.level_map[y][x] == 2:
                    level_environment[y][x] = (LevelEnvironment
                                               .Energiser(self.screen, x, y, cell_width, cell_height,
                                                          self.level_loop_counter, "white"))
                elif self.level_map[y][x] == 3:
                    level_environment[y][x] = (LevelEnvironment
                                               .Wall(self.screen, x, y, cell_width, cell_height, 1, self.level_color))
                elif self.level_map[y][x] == 4:
                    level_environment[y][x] = (LevelEnvironment
                                               .Wall(self.screen, x, y, cell_width, cell_height, 2,self.level_color))
                elif self.level_map[y][x] == 5:
                    level_environment[y][x] = (LevelEnvironment
                                               .CurvedWall(self.screen, x, y, cell_width, cell_height, 1, self.level_color))
                elif self.level_map[y][x] == 6:
                    level_environment[y][x] = (LevelEnvironment
                                               .CurvedWall(self.screen, x, y, cell_width, cell_height, 2, self.level_color))
                elif self.level_map[y][x] == 7:
                    level_environment[y][x] = (LevelEnvironment
                                               .CurvedWall(self.screen, x, y, cell_width, cell_height, 3, self.level_color))
                elif self.level_map[y][x] == 8:
                    level_environment[y][x] = (LevelEnvironment
                                               .CurvedWall(self.screen, x, y, cell_width, cell_height, 4, self.level_color))
                elif self.level_map[y][x] == 9:
                    level_environment[y][x] = (LevelEnvironment
                                               .Wall(self.screen, x, y, cell_width, cell_height, 2,"white"))

        return LevelController(level_environment)


class LevelController:
    def __init__(self, level_environment):
        self.level_environment = level_environment

    def update(self):
        for y in range(len(self.level_environment)):
            for x in range(len(self.level_environment[0])):
                self.level_environment[y][x].draw()

    def get_cell(self,x,y):
        return self.level_environment[y][x]

    def delete_cell(self, x, y):
        self.level_environment[y][x] = LevelEnvironment.BlankSpace()
