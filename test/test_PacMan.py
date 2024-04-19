import pygame
import pytest

from src import Score
from src.Health import Health
from src.PacMan import PacMan
from src.Position import Position
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
    cell = LevelEnvironment.Wall(None, None, None, None, None, None, None)

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


@pytest.mark.parametrize("x, y, expected", [
    (28, 0, [False, False, False, True]),
    (10, 5, [False, False, False, True])
])
def test_turn_allow_update(pacman, x, y, expected):
    pacman.turn_allow_update(x, y)
    assert pacman.turn_allow_update(27, 1) == expected

def test_pacman_rotation_turn_right(pacman):
    pacman.turn = Position.RIGHT
    direction = pacman.pacman_rotation(Position.LEFT, [True, False, False, False])
    assert direction == Position.RIGHT


def test_pacman_rotation_turn_left(pacman):
    pacman.turn = Position.LEFT
    direction = pacman.pacman_rotation(Position.RIGHT, [False, True, False, False])
    assert direction == Position.LEFT


def test_pacman_rotation_turn_up(pacman):
    pacman.turn = Position.UP
    direction = pacman.pacman_rotation(Position.DOWN, [False, False, True, False])
    assert direction == Position.UP


def test_pacman_rotation_turn_down(pacman):
    pacman.turn = Position.DOWN
    direction = pacman.pacman_rotation(Position.UP, [False, False, False, True])
    assert direction == Position.DOWN


def test_pacman_rotation_no_turn(pacman):
    pacman.turn = Position.UP
    direction = pacman.pacman_rotation(Position.DOWN, [False, False, False, False])
    assert direction == Position.DOWN


def test_out_of_bound_controller_right_boundary(pacman):
    direction = Position.RIGHT
    pacman_cell_x = pacman.cell_len_x - 2
    pacman_cell_y = 5
    new_x, new_y = pacman.out_of_bound_controller(direction, pacman_cell_x, pacman_cell_y)
    assert new_x == 0


def test_out_of_bound_controller_left_boundary(pacman):
    direction = Position.LEFT
    pacman_cell_x = 0
    pacman_cell_y = 5
    new_x, new_y = pacman.out_of_bound_controller(direction, pacman_cell_x, pacman_cell_y)
    assert new_x == pacman.cell_len_x - 2


def test_out_of_bound_controller_top_boundary(pacman):
    direction = Position.UP
    pacman_cell_x = 5
    pacman_cell_y = pacman.cell_len_y - 2
    new_x, new_y = pacman.out_of_bound_controller(direction, pacman_cell_x, pacman_cell_y)
    assert new_y == 0


def test_out_of_bound_controller_bottom_boundary(pacman):
    direction = Position.DOWN
    pacman_cell_x = 5
    pacman_cell_y = 0
    new_x, new_y = pacman.out_of_bound_controller(direction, pacman_cell_x, pacman_cell_y)
    assert new_y == pacman.cell_len_y - 2


def test_out_of_bound_controller_no_change(pacman):
    direction = Position.RIGHT
    pacman_cell_x = 5
    pacman_cell_y = 5
    new_x, new_y = pacman.out_of_bound_controller(direction, pacman_cell_x, pacman_cell_y)
    assert new_x == pacman_cell_x
    assert new_y == pacman_cell_y


def test_is_out_of_bounds_right_boundary(pacman):
    direction = Position.RIGHT
    pacman_cell_x = pacman.cell_len_x - 2
    pacman_cell_y = 5
    assert pacman.is_out_of_bounds(direction, pacman_cell_x, pacman_cell_y) is True


def test_is_out_of_bounds_left_boundary(pacman):
    direction = Position.LEFT
    pacman_cell_x = 0
    pacman_cell_y = 5
    assert pacman.is_out_of_bounds(direction, pacman_cell_x, pacman_cell_y) is True


def test_is_out_of_bounds_top_boundary(pacman):
    direction = Position.UP
    pacman_cell_x = 5
    pacman_cell_y = pacman.cell_len_y - 2
    assert pacman.is_out_of_bounds(direction, pacman_cell_x, pacman_cell_y) is True


def test_is_out_of_bounds_bottom_boundary(pacman):
    direction = Position.DOWN
    pacman_cell_x = 5
    pacman_cell_y = 0
    assert pacman.is_out_of_bounds(direction, pacman_cell_x, pacman_cell_y) is True


def test_is_out_of_bounds_no_boundary(pacman):
    direction = Position.RIGHT
    pacman_cell_x = 5
    pacman_cell_y = 5
    assert pacman.is_out_of_bounds(direction, pacman_cell_x, pacman_cell_y) is False
    
def test_is_cell_wall(pacman):
    cell = LevelEnvironment.Wall(None, None, None, None, None, None, None)

    assert pacman.is_cell_wall(cell) is True


def test_get_coordinate_by_cell(pacman):
    cell_size = 10
    cell_coordinate = 5
    offset = 2

    expected_value = cell_size * (cell_coordinate + offset)

    result = PacMan.get_coordinate_by_cell(cell_size, cell_coordinate, offset)

    assert result == expected_value


