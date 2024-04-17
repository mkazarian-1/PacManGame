import pytest
import pygame

from src.level.LevelEnvironment import Wall


class TestWall:

    @pytest.mark.parametrize("x, y, position", [(1, 2, 1), (2, 0, 0)])
    def test_init(self, screen, x, y, position, level_builder):
        wall = Wall(screen, x, y, level_builder.cell_width, level_builder.cell_height, position, "blue")
        assert wall.screen == screen
        assert wall.x == x
        assert wall.y == y
        assert wall.cell_width == level_builder.cell_width
        assert wall.cell_height == level_builder.cell_height
        assert wall.position == position
        assert wall.color == "blue"

    @pytest.mark.parametrize("x, y, position", [(1, 2, 1), (2, 0, 0)])
    def test_draw(self, screen, x, y, position, level_builder, monkeypatch, mocker):
        wall = Wall(screen, x, y, level_builder.cell_width, level_builder.cell_height, position, "blue")
        mock_draw_line = mocker.MagicMock()
        monkeypatch.setattr(pygame.draw, "line", mock_draw_line)
        wall.draw()
        if wall.position:
            mock_draw_line.assert_called_once_with(wall.screen, wall.color,
                                                   (wall.x * wall.cell_width + (wall.cell_width / 2),
                                                    wall.y * wall.cell_height),
                                                   (wall.x * wall.cell_width + (wall.cell_width / 2),
                                                    (wall.y + 1) * wall.cell_height), 3)
        else:
            mock_draw_line.assert_called_once_with(wall.screen, wall.color,
                                                   (wall.x * wall.cell_width, wall.y * wall.cell_height +
                                                    (wall.cell_height / 2)),
                                                   ((wall.x + 1) * wall.cell_width, wall.y * wall.cell_height +
                                                    (wall.cell_height / 2)), 3)
