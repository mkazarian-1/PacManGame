import pygame
import pytest
from src.menu_pg.Menu import Menu
from src.ScreenSettings import ScreenSettings


def test_menu_init():
    screen_settings = ScreenSettings()
    menu = Menu(screen_settings)
    assert menu.screen_settings == screen_settings


def test_menu_draw_menu():
    screen_settings = ScreenSettings()
    menu = Menu(screen_settings)
    pygame.init()
    screen = pygame.display.set_mode([800, 600])
    menu.draw_menu(screen)
    assert menu.play_rect is not None
    assert menu.options_rect is not None
    assert menu.quit_rect is not None

