import pytest
import pygame


class TestFood:

    @pytest.mark.skip
    def test_init(self, food, screen, level_builder, score, endgame_controller):
        assert food.screen == screen
        assert food.x == 1
        assert food.y == 0
        assert food.cell_width == level_builder.cell_width
        assert food.cell_height == level_builder.cell_height
        assert food.color == "white"
        assert food.score == score
        assert food.end_game_controller == endgame_controller

    def test_action(self, monkeypatch, mocker, food):
        mock_increase_score = mocker.MagicMock()
        mock_decrease_amount_dots = mocker.MagicMock()
        monkeypatch.setattr(food.score, "increase_score", mock_increase_score)
        monkeypatch.setattr(food.end_game_controller, "decrease_amount_dots", mock_decrease_amount_dots)
        food.action()
        mock_increase_score.assert_called_once_with(10)
        mock_decrease_amount_dots.assert_called_once_with(1)

    def test_draw(self, monkeypatch, mocker, food):
        mock_draw = mocker.MagicMock()
        monkeypatch.setattr(pygame.draw, "circle", mock_draw)
        food.draw()
        mock_draw.assert_called_once_with(food.screen, food.color,
                                          (food.x * food.cell_width + (food.cell_width / 2),
                                           food.y * food.cell_height + (food.cell_height / 2)), 4)
