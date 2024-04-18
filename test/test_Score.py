import pytest
import pygame

from src.Score import PlayerScore


class TestScore:

    def setup_method(self):
        pygame.init()
        self.screen = pygame.surface.Surface((900, 900))
        self.score = PlayerScore(self.screen)

    def test_init(self):
        assert self.score.get_score() == 0
        assert self.score.get_screen == self.screen

    def test_get_score(self, monkeypatch):
        monkeypatch.setattr(self.score, "_PlayerScore__score", 50)
        assert self.score.get_score() == 50

    @pytest.mark.parametrize("amount, value, expected", [
        (50, 50, 100),
        (3, 50, 53),
        (7, 34, 41),
        (9, 99, 108),
    ])
    def test_increase_score(self, monkeypatch, amount, value, expected):
        monkeypatch.setattr(self.score, "_PlayerScore__score", amount)
        self.score.increase_score(value)
        assert self.score.get_score() == expected

    def test_clear_score(self):
        self.score.clear_score()
        assert self.score.get_score() == 0

    def test_draw(self, monkeypatch, mocker):
        mock_draw = mocker.MagicMock()
        monkeypatch.setattr(self.score, "draw", mock_draw)
        self.score.draw(100, 100)
        mock_draw.assert_called_once_with(100, 100)