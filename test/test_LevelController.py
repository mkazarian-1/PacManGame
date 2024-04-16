import pytest

from src.level.LevelEnvironment import BlankSpace, Door, Food, Energiser, Wall, CurvedWall


class TestLevelController:

    @pytest.mark.skip
    def test_init(self, level_controller, level_builder, level_map):
        assert [level_controller.level_environment == level_builder._create_level_environment()]
        assert level_controller.cell_width == 900 / len(level_map[0])
        assert level_controller.cell_height == 900 / len(level_map)

    def test_update(self, monkeypatch, level_controller, level_map, mocker):
        mock_draw = mocker.MagicMock()
        [monkeypatch.setattr(level_controller.level_environment[i][j], "draw", mock_draw)
         for i in range(len(level_controller.level_environment[0])) for j in
         range(len(level_controller.level_environment))]
        level_controller.update()
        assert mock_draw.call_count == len(level_map) * len(level_map[0])

    @pytest.mark.parametrize("x, y, expected", [
        (2, 3, Door),
        (0, 0, BlankSpace),
        (0, 1, Food),
        (1, 1, Energiser),
        (2, 1, Wall),
        (0, 2, Wall),
        (1, 2, CurvedWall),
        (2, 2, CurvedWall),
        (0, 3, CurvedWall),
        (1, 3, CurvedWall)
    ])
    def test_get_cell(self, x, y, expected, level_controller):
        actual_result = level_controller.get_cell(x, y)
        assert isinstance(actual_result, expected)

    def test_delete_cell(self, level_controller):
        level_controller.delete_cell(0, 1)
        actual_result = level_controller.level_environment
        assert isinstance(actual_result[1][0], BlankSpace)

    def test_get_amount_of_cells(self, level_controller):
        x, y = level_controller.get_amount_of_cells()
        assert x, y == (4, 4)

    def test_get_width_of_cells(self, level_controller, level_map):
        assert level_controller.get_width_of_cells() == 900 / len(level_map[0])

    def test_get_height_of_cells(self, level_controller, level_map):
        assert level_controller.get_height_of_cells() == 900 / len(level_map)
