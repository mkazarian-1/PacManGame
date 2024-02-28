import pygame
import sys
from PacManGame import PacManGame
from win32api import GetSystemMetrics
from Button import Button
from Options import Options

def get_font(size, ind):
    # Повертає шрифт за розміром і індексом
    return pygame.font.Font("assets/Emulogic-zrEw.ttf", int(size * ind))

class Menu:
    def __init__(self):
        self.options = Options()  # Створює об'єкт опцій
        self.current_screen_size = self.options.get_current_screen_size()
        self.background = self.options.get_current_background_color()
        self.set_screen_size()

    def set_screen_size(self):
        # Встановлює розмір екрану залежно від поточних налаштувань
        self.HEIGHT, self.WIDTH = self.options.SCREEN_SIZES[self.current_screen_size]

    def update_screen(self):
        # Оновлює розмір екрану та фоновий колір згідно з поточними налаштуваннями
        self.background = self.options.get_current_background_color()
        self.current_screen_size = self.options.get_current_screen_size()
        self.set_screen_size()

    def start(self):
        pygame.init()
        pygame.display.set_caption("PacMan")
        clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill(self.background)
            self.draw_menu()
            pygame.display.flip()
            clock.tick(60)

        pygame.quit()

    def draw_menu(self):
        # Встановлюємо необхідні індекси відповідно до розміру вікна
        if self.current_screen_size == "Large":
            ind = 1
        elif self.current_screen_size == "Medium":
            ind = 0.7
        elif self.current_screen_size == "Small":
            ind = 0.5

        # Змінюємо розміри кнопок меню відповідно до розміру вікна
        play_b = pygame.image.load("assets/Play Rect.png")
        options_b = pygame.image.load("assets/Options Rect.png")
        quit_b = pygame.image.load("assets/Quit Rect.png")

        play_b = pygame.transform.scale(play_b, (
        int(play_b.get_width() * ind), int(play_b.get_height() * ind)))
        options_b = pygame.transform.scale(options_b, (
        int(options_b.get_width() * ind), int(options_b.get_height() * ind)))
        quit_b = pygame.transform.scale(quit_b, (
        int(quit_b.get_width() * ind), int(quit_b.get_height() * ind)))

        menu_mouse_pos = pygame.mouse.get_pos()

        # текст меню
        menu_text = get_font(65, ind).render("MAIN MENU", True, "#f4cd33")
        menu_rect = menu_text.get_rect(center=(self.WIDTH // 2, 100 * ind))

        # кнопки
        play_button = Button(image=play_b, pos=(self.WIDTH // 2, 250 * ind),
                             text_input="PLAY", font=get_font(65, ind), base_color="#b6d7a8", hovering_color="White")
        options_button = Button(image=options_b, pos=(self.WIDTH // 2, 400 * ind),
                                text_input="OPTIONS", font=get_font(65, ind), base_color="#b6d7a8", hovering_color="White")
        quit_button = Button(image=quit_b, pos=(self.WIDTH // 2, 550 * ind),
                             text_input="QUIT", font=get_font(65, ind), base_color="#b6d7a8", hovering_color="White")

        # зміна кольору кнопки, якщо навели курсор
        self.screen.blit(menu_text, menu_rect)
        for button in [play_button, options_button, quit_button]:
            button.changeColor(menu_mouse_pos)
            button.update(self.screen)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.checkForInput(menu_mouse_pos):
                    self.play()
                if options_button.checkForInput(menu_mouse_pos):
                    self.option()
                    self.update_screen()  # Оновлює розмір екрану при переході до налаштувань
                if quit_button.checkForInput(menu_mouse_pos):
                    pygame.quit()

    def option(self):
        # Відображає меню налаштувань
        self.options.start()

    def play(self):
        # Починає гру
        pacman = PacManGame(self.WIDTH, self.HEIGHT, self.background)
        pacman.start_game()
