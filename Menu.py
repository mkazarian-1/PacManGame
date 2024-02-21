import pygame
import sys
from PacManGame import PacManGame
from win32api import GetSystemMetrics
from Button import Button
from Options import Options

def get_font(size):
    return pygame.font.Font("assets/Emulogic-zrEw.ttf", size)


class Menu:
    def __init__(self):
        self.HEIGHT = GetSystemMetrics(1) - 85
        self.WIDTH = int(self.HEIGHT * 0.95)
        self.HalfWidth = self.WIDTH // 2
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

    def start(self):
        pygame.init()

        pygame.display.set_caption("PacMan")

        clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill((0, 0, 0))
            self.draw_menu()
            pygame.display.flip()
            clock.tick(60)

        pygame.quit()

    def draw_menu(self):
        menu_mouse_pos = pygame.mouse.get_pos()

        menu_text = get_font(65).render("MAIN MENU", True, "#b68f40")
        menu_rect = menu_text.get_rect(center=(self.HalfWidth, 100))

        play_button = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(self.HalfWidth, 250),
                             text_input="PLAY", font=get_font(65), base_color="#d7fcd4", hovering_color="White")
        options_button = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(self.HalfWidth, 400),
                                text_input="OPTIONS", font=get_font(65), base_color="#d7fcd4", hovering_color="White")
        quit_button = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(self.HalfWidth, 550),
                             text_input="QUIT", font=get_font(65), base_color="#d7fcd4", hovering_color="White")

        self.screen.blit(menu_text, menu_rect)
        for button in [play_button, options_button, quit_button]:
            button.changeColor(menu_mouse_pos)
            button.update(self.screen)


        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.checkForInput(menu_mouse_pos):
                    self.play()
                if options_button.checkForInput(menu_mouse_pos):
                    self.options()
                if quit_button.checkForInput(menu_mouse_pos):
                    pygame.quit()

    def options(self):
        options = Options()
        options.start()


    def play(self):
        pacman = PacManGame()
        pacman.start_game()

