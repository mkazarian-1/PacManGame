import pygame
import pytest

from src import Score
from src.Health import Health
from src.PacMan import PacMan
from src.level import LevelMap, LevelBuilder, LevelEnvironment
from src.level.EndGameController import EndGameController


@pytest.fixture
def pacman():
    screen_width = 800
    screen_height = 1200
    screen = pygame.Surface((screen_width, screen_height))

    score = Score.PlayerScore(pygame.Surface((screen_width, screen_height)))

    endGameController = EndGameController()
    level_controller = LevelBuilder.LevelBuilder(screen, LevelMap.boards,
                                                 score, endGameController).build()

    return PacMan(screen, level_controller)


def test_pacman_star_position(pacman):
    assert pacman.pacman_cell_x == 15 and pacman.pacman_cell_y == 18


def test_is_cell_action_with_food(pacman):
    cell = LevelEnvironment.Food(None, None, None, None, None, None,
                                 Score.PlayerScore(pygame.Surface((10, 10))), EndGameController())
    assert pacman.is_cell_action(cell) is True


def test_is_cell_action_with_energiser(pacman):
    cell = LevelEnvironment.Energiser(None, None, None, None, None, None,
                                      EndGameController())

    assert pacman.is_cell_action(cell) is True

def test_is_cell_action_with_non_actionable_cell(pacman):
    cell = LevelEnvironment.Wall(None, None, None, None, None, None,None)

    assert pacman.is_cell_action(cell) is False

# def test_is_cell_action_with_energiser(pacman_instance):
#     # Перевірка, чи правильно визначається дія для клітинки з енергійними стимуляторами
#     energiser_cell = Energiser()
#     assert pacman_instance.is_cell_action(energiser_cell) is True
#
# def test_is_cell_action_with_non_actionable_cell(pacman_instance):
#     # Перевірка, чи правильно визначається відсутність дії для клітинки без дійових об'єктів
#     class Wall:
#         pass
#     wall_cell = Wall()
#     assert pacman_instance.is_cell_action(wall_cell) is False
