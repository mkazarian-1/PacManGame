import pygame
import pytest
from src.ScreenSettings import ScreenSettings


def test_screen_settings_init():
    screen_settings = ScreenSettings()
    assert screen_settings.current_screen_size == "Large"
    assert screen_settings.current_background_color == "Black"
    assert screen_settings.background_image is None
    assert not screen_settings.image_inserted


def test_screen_settings_getters_and_setters():
    screen_settings = ScreenSettings()
    screen_settings.set_screen_size("Small")
    screen_settings.set_background_color("Blue")
    screen_settings.set_image_inserted(True)
    assert screen_settings.get_screen_size() == "Small"
    assert screen_settings.get_background_color() == (97, 146, 178)
    assert screen_settings.is_image_inserted() == True
