from src.menu_pg.Menu import Menu
from src.ScreenSettings import ScreenSettings

if __name__ == "__main__":
    screen_settings = ScreenSettings()

    menu = Menu(screen_settings)
    menu.start()


