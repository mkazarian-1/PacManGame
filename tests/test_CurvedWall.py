import pytest
import pygame
import math

from src.level.LevelEnvironment import CurvedWall


class TestCurvedWall:

    @pytest.mark.parametrize("x, y, position", [(2, 1, 1), (2, 2, 2), (3, 0, 3), (3, 1, 4)])
    def test_init(self, x, y, position, screen, level_builder):
        curved_wall = CurvedWall(screen, x, y, level_builder.cell_width, level_builder.cell_height, position, "blue")
        assert curved_wall.screen == screen
        assert curved_wall.x == x
        assert curved_wall.y == y
        assert curved_wall.cell_width == level_builder.cell_width
        assert curved_wall.cell_height == level_builder.cell_height
        assert curved_wall.position == position
        assert curved_wall.color == "blue"

    @pytest.mark.parametrize("x, y, position", [(2, 1, 1), (2, 2, 2), (3, 0, 3), (3, 1, 4)])
    def test_draw(self, x, y, position, screen, level_builder, monkeypatch, mocker):
        curved_wall = CurvedWall(screen, x, y, level_builder.cell_width, level_builder.cell_height, position, "blue")

        mock_draw_arc = mocker.MagicMock()
        monkeypatch.setattr(pygame.draw, "arc", mock_draw_arc)

        curved_wall.draw()
        if curved_wall.position == 1:
            mock_draw_arc.assert_called_once_with(curved_wall.screen, curved_wall.color,
                                                  [(curved_wall.x * curved_wall.cell_width -
                                                    (curved_wall.cell_width / 2)), (curved_wall.y *
                                                                                    curved_wall.cell_height +
                                                                                    (curved_wall.cell_height / 2)),
                                                   curved_wall.cell_width + 2, curved_wall.cell_height - 2], 0,
                                                  math.pi / 2, 3)
        elif curved_wall.position == 2:
            mock_draw_arc.assert_called_once_with(curved_wall.screen, curved_wall.color,
                                                  [(curved_wall.x * curved_wall.cell_width +
                                                    (curved_wall.cell_width / 2)),
                                                   (curved_wall.y * curved_wall.cell_height +
                                                    (curved_wall.cell_height / 2)),
                                                   curved_wall.cell_width - 2, curved_wall.cell_height - 2],
                                                  math.pi / 2, math.pi, 3)
        elif curved_wall.position == 3:
            mock_draw_arc.assert_called_once_with(curved_wall.screen, curved_wall.color,
                                                  [(curved_wall.x * curved_wall.cell_width +
                                                    (curved_wall.cell_width / 2)), (curved_wall.y *
                                                                                    curved_wall.cell_height -
                                                                                    (curved_wall.cell_height / 2)),
                                                   curved_wall.cell_width - 2, curved_wall.cell_height + 2], -1 *
                                                  math.pi, math.pi * -1 / 2, 3)
        else:
            mock_draw_arc.assert_called_once_with(curved_wall.screen, curved_wall.color,
                                                  [(curved_wall.x * curved_wall.cell_width -
                                                    (curved_wall.cell_width / 2)),
                                                   (curved_wall.y * curved_wall.cell_height -
                                                    (curved_wall.cell_height / 2)),
                                                   curved_wall.cell_width + 2, curved_wall.cell_height + 2],
                                                  math.pi * -1 / 2, 0, 3)
