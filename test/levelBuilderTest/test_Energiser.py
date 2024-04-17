import pytest
import pygame


class TestEnergiser:

    @pytest.mark.skip
    def test_init(self, energiser, screen, level_builder, endgame_controller):
        assert energiser.screen == screen
        assert energiser.x == 1
        assert energiser.y == 1
        assert energiser.cell_width == level_builder.cell_width
        assert energiser.cell_height == level_builder.cell_height
        assert energiser.color == "white"
        assert energiser.end_game_controller == endgame_controller

    def test_action(self, energiser, monkeypatch, mocker):
        mock_decrease_amount_dots = mocker.MagicMock()
        monkeypatch.setattr(energiser.end_game_controller, "decrease_amount_dots", mock_decrease_amount_dots)
        energiser.action()
        mock_decrease_amount_dots.assert_called_once_with(1)

    def test_draw(self, energiser, monkeypatch, mocker):
        mock_draw = mocker.MagicMock()

        def get_ticks():
            return 1100

        monkeypatch.setattr(pygame.draw, "circle", mock_draw)
        monkeypatch.setattr(pygame.time, "get_ticks", get_ticks)
        energiser.draw()
        mock_draw.assert_called_once_with(energiser.screen, energiser.color,
                                          (energiser.x * energiser.cell_width + (energiser.cell_width / 2),
                                           energiser.y * energiser.cell_height + (energiser.cell_height / 2)), 8)
