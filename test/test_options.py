import pygame
import pytest
from src.menu_pg.Options import Options
from src.ScreenSettings import ScreenSettings


def test_options_init():
    screen_settings = ScreenSettings()
    options = Options(screen_settings)
    assert options.screen_settings == screen_settings


def test_options_draw_options_screen():
    screen_settings = ScreenSettings()
    options = Options(screen_settings)
    pygame.init()
    screen = pygame.display.set_mode([800, 600])
    options.draw_options_screen(screen)
    assert options.back_rect is not None
    assert options.insert_rect is not None
    assert options.option_rects is not None
    assert options.col_option_rects is not None

