import pytest
import pygame

from src.Health import Health


class TestHealth:

    def setup_method(self):
        self.screen = pygame.surface.Surface((900, 900))
        self.health = Health(self.screen)

    def test_init(self):
        assert self.health.get_health == 3
        assert self.health.get_screen == self.screen

    def test_decrease_health(self):
        self.health.decrease_health()
        assert self.health.get_health == 2

    @pytest.mark.parametrize("value, expected", [(1, True), (2, True), (3, True), (-1, False)])
    def test_is_alive(self, value, expected, monkeypatch):
        monkeypatch.setattr(self.health, "_Health__health", value)
        assert self.health.is_alive() == expected