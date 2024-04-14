import pytest


class TestEndGameController:

    def test_init(self, endgame_controller):
        assert endgame_controller.get_dots == 0
        assert endgame_controller.get_is_win is False

    @pytest.mark.parametrize("amount, expected", [(1, 1), (10, 10), (20, 20), (30, 30), (40, 40)])
    def test_increase_amount_dots(self, endgame_controller, amount, expected):
        endgame_controller.increase_amount_dots(amount)
        assert endgame_controller.get_dots == expected

    @pytest.mark.parametrize("amount, rest, expected",
                             [(1, 99, False), (10, 90, False), (20, 80, False),
                              (30, 70, False), (40, 60, False), (200, -100, True)])
    def test_decrease_amount_dots(self, amount, endgame_controller, rest, expected, monkeypatch):
        monkeypatch.setattr(endgame_controller, "_EndGameController__dots", 100)
        endgame_controller.decrease_amount_dots(amount)
        assert endgame_controller.get_dots == rest
        assert endgame_controller.get_is_win == expected

    @pytest.mark.parametrize("amount, expected", [(10, True), (3, False), (20, True)])
    def test_is_win_changed(self, endgame_controller, amount, expected, monkeypatch):
        monkeypatch.setattr(endgame_controller, "_EndGameController__dots", 10)
        endgame_controller.decrease_amount_dots(amount)
        assert endgame_controller.is_win() == expected
