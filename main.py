from menu_pg.Menu import Menu
from ScreenSettings import ScreenSettings

if __name__ == "__main__":
    screen_settings = ScreenSettings()

    menu = Menu(screen_settings)
    menu.start()


