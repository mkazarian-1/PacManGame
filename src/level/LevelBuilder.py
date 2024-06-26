import pygame

import src.level.LevelEnvironment as LevelEnvironment
from src import Score
from src.Health import Health
from src.level.EndGameController import EndGameController


class LevelBuilder:
    level_color = "blue"

    def __init__(self, screen: pygame.surface.Surface, level_map, score: Score.PlayerScore,
                 end_game_controller: EndGameController):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
        self.level_map = level_map
        self.cell_height = self.height / len(self.level_map)
        self.cell_width = self.width / len(self.level_map[0])
        self.score = score
        self.end_game_controller = end_game_controller

    def build(self):
        level_environment = self._create_level_environment()
        return LevelController(level_environment, self.cell_width, self.cell_height)

    def _create_level_environment(self):
        level_environment = [[LevelEnvironment.BlankSpace() for _ in range(len(self.level_map[0]))]
                             for _ in range(len(self.level_map))]
        for y in range(len(self.level_map)):
            for x in range(len(self.level_map[0])):
                level_environment[y][x] = self._create_environment_element(x, y)
        return level_environment

    def _create_environment_element(self, x, y):
        element_type = self.level_map[y][x]
        if element_type == 1:
            return (LevelEnvironment
                    .Food(self.screen, x, y, self.cell_width, self.cell_height, "white",
                          self.score, self.end_game_controller))
        elif element_type == 2:
            return (LevelEnvironment
                    .Energiser(self.screen, x, y, self.cell_width, self.cell_height,
                               "white", self.end_game_controller))
        elif element_type == 3:
            return (LevelEnvironment
                    .Wall(self.screen, x, y, self.cell_width, self.cell_height, 1,
                          self.level_color))
        elif element_type == 4:
            return (LevelEnvironment
                    .Wall(self.screen, x, y, self.cell_width, self.cell_height, 2,
                          self.level_color))
        elif element_type == 5:
            return (LevelEnvironment
                    .CurvedWall(self.screen, x, y, self.cell_width, self.cell_height, 1,
                                self.level_color))
        elif element_type == 6:
            return (LevelEnvironment
                    .CurvedWall(self.screen, x, y, self.cell_width, self.cell_height, 2,
                                self.level_color))
        elif element_type == 7:
            return (LevelEnvironment
                    .CurvedWall(self.screen, x, y, self.cell_width, self.cell_height, 3,
                                self.level_color))
        elif element_type == 8:
            return (LevelEnvironment
                    .CurvedWall(self.screen, x, y, self.cell_width, self.cell_height, 4,
                                self.level_color))
        elif element_type == 9:
            return (LevelEnvironment
                    .Door(self.screen, x, y, self.cell_width, self.cell_height, 2, "white"))
        return LevelEnvironment.BlankSpace()


class LevelController:
    def __init__(self, level_environment, cell_width, cell_height):
        self.level_environment = level_environment
        self.cell_width = cell_width
        self.cell_height = cell_height

    def update(self):
        for y in range(len(self.level_environment)):
            for x in range(len(self.level_environment[0])):
                self.level_environment[y][x].draw()

    def get_cell(self, x, y):
        return self.level_environment[y][x]

    def delete_cell(self, x, y):
        self.level_environment[y][x] = LevelEnvironment.BlankSpace()

    def get_amount_of_cells(self):
        return [len(self.level_environment[0]), len(self.level_environment)]

    def get_width_of_cells(self):
        return self.cell_width

    def get_height_of_cells(self):
        return self.cell_height


class LevelBar:
    def __init__(self, screen, score: Score.PlayerScore, health: Health):
        self.screen = screen
        self.health = health
        self.score = score

    def update(self):
        self.score.draw(self.screen.get_width() * 0.05, 0)
        self.health.draw(self.screen.get_width() * 0.85, 0)

    def get_score(self):
        return self.score

    def get_health(self):
        return self.health
