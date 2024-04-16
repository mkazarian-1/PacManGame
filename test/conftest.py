import pygame
import pytest

import src.Score as Score
import src.Health as Health
import src.level.EndGameController as EndGameController
from src.level.LevelBuilder import LevelBuilder, LevelController, LevelBar
from src.level.LevelEnvironment import Food, Energiser


@pytest.fixture
def screen():
    return pygame.surface.Surface((900, 900))


@pytest.fixture
def level_map():
    return [[0, 0, 0, 0],
            [1, 2, 3, 0],
            [4, 5, 6, 0],
            [7, 8, 9, 0]]


@pytest.fixture
def score(screen):
    return Score.PlayerScore(screen)


@pytest.fixture
def endgame_controller():
    return EndGameController.EndGameController()


@pytest.fixture
def level_builder(screen, level_map, score, endgame_controller):
    return LevelBuilder(screen, level_map, score, endgame_controller)


@pytest.fixture
def level_controller(level_builder):
    return LevelController(level_builder._create_level_environment(), level_builder.cell_width,
                           level_builder.cell_height)


@pytest.fixture
def health(screen):
    return Health.Health(screen)


@pytest.fixture
def level_bar(screen, score, health):
    return LevelBar(screen, score, health)


@pytest.fixture
def food(screen, level_builder, score, endgame_controller):
    return Food(screen, 1, 0, level_builder.cell_width, level_builder.cell_height, "white", score, endgame_controller)


@pytest.fixture
def energiser(screen, level_builder, endgame_controller):
    return Energiser(screen, 1, 1, level_builder.cell_width, level_builder.cell_height, "white", endgame_controller)
