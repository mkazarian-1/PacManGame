import pytest

from src.level.LevelBuilder import LevelController
from src.level.LevelEnvironment import Wall, Food, Energiser, CurvedWall, Door, BlankSpace


class TestLevelBuilder:

    @pytest.mark.skip
    def test_init(self, screen, score, level_map, level_builder, endgame_controller):
        assert level_builder.screen == screen
        assert level_builder.width == 900
        assert level_builder.height == 900
        assert level_builder.level_map == level_map
        assert level_builder.cell_height == 900 / len(level_map)
        assert level_builder.cell_width == 900 / len(level_map[0])
        assert level_builder.score == score
        assert level_builder.end_game_controller == endgame_controller
        assert level_builder.level_color == "blue"

    @pytest.mark.parametrize("x, y, expected", [
        (0, 0, BlankSpace),
        (1, 0, Food),
        (1, 1, Energiser),
        (1, 2, Wall),
        (2, 0, Wall),
        (2, 1, CurvedWall),
        (2, 2, CurvedWall),
        (3, 0, CurvedWall),
        (3, 1, CurvedWall),
        (3, 2, Door)
    ])
    def test_create_environment_element(self, x, y, expected, level_builder):
        actual_result = level_builder._create_environment_element(y, x)
        assert isinstance(actual_result, expected)

    def test_create_level_environment(self, level_builder, level_map):
        expected = [[BlankSpace, BlankSpace, BlankSpace, BlankSpace],
                    [Food, Energiser, Wall, BlankSpace],
                    [Wall, CurvedWall, CurvedWall, BlankSpace],
                    [CurvedWall, CurvedWall, Door, BlankSpace]]
        assert [[isinstance(level_builder._create_level_environment()[i][j], expected[i][j]) for i in range(
            len(level_map[0]))] for j in range(len(level_map))]

    def test_build(self, level_builder):
        expected = LevelController(level_builder._create_level_environment(), level_builder.cell_width,
                                   level_builder.cell_height)
        assert isinstance(expected, LevelController)
