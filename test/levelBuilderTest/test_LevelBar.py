import pytest


class TestLevelBar:

    @pytest.mark.skip
    def test_init(self, level_bar, screen, score, health):
        assert level_bar.screen == screen
        assert level_bar.score == score
        assert level_bar.health == health

    def test_update(self, monkeypatch, level_bar, screen, mocker):
        mock_draw_health = mocker.MagicMock()
        mock_draw_score = mocker.MagicMock()
        monkeypatch.setattr(level_bar.health, "draw", mock_draw_health)
        monkeypatch.setattr(level_bar.score, "draw", mock_draw_score)
        level_bar.update()
        mock_draw_health.assert_called_once_with(screen.get_width() * 0.85, 0)
        mock_draw_score.assert_called_once_with(screen.get_width() * 0.05, 0)

    def test_get_score(self, level_bar, score):
        assert level_bar.get_score() == score

    def test_get_health(self, level_bar, health):
        assert level_bar.get_health() == health