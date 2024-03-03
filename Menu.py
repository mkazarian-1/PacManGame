import pygame
import sys
from PacManGame import PacManGame
from Options import Options

pygame.init()


def get_font(size, ind):
    return pygame.font.Font("assets/Emulogic-zrEw.ttf", int(size * ind))


class Menu:
    def __init__(self):
        self.options = Options()
        self.current_screen_size = self.options.get_current_screen_size()
        self.background = self.options.get_current_background_color()
        self.set_screen_size()
        self.background_image = self.options.get_background_image()
        self.image_inserted = self.options.image_inserted
        self.play_rect = None
        self.options_rect = None
        self.quit_rect = None

    def set_screen_size(self):
        self.HEIGHT, self.WIDTH = self.options.SCREEN_SIZES[self.current_screen_size]

    def update_screen(self):
        self.background = self.options.get_current_background_color()
        self.current_screen_size = self.options.get_current_screen_size()
        self.background_image = self.options.get_background_image()
        self.image_inserted = self.options.is_image_inserted()
        self.set_screen_size()

    def start(self):
        pygame.display.set_caption("PacMan")
        clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.draw_menu()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    menu_mouse_pos = pygame.mouse.get_pos()
                    print("Mouse button down at position:", menu_mouse_pos)
                    if self.play_rect.collidepoint(menu_mouse_pos):
                        self.play()
                    if self.options_rect.collidepoint(menu_mouse_pos):
                        self.option()
                        self.update_screen()
                    if self.quit_rect.collidepoint(menu_mouse_pos):
                        pygame.quit()

            self.screen.fill(self.background)
            if self.image_inserted:
                self.screen.blit(self.background_image, (0, 0))
            self.draw_menu()
            pygame.display.flip()
            clock.tick(60)

        pygame.quit()

    def draw_menu(self):
        if self.current_screen_size == "Large":
            ind = 1
        elif self.current_screen_size == "Medium":
            ind = 0.7
        elif self.current_screen_size == "Small":
            ind = 0.5

        menu_text = get_font(65, ind).render("MAIN MENU", True, "#f4cd33")
        menu_rect = menu_text.get_rect(center=(self.WIDTH // 2, (self.HEIGHT // 2) - (300 * ind)))

        play_button = get_font(65, ind).render("PLAY", True, (255, 255, 255))
        self.play_rect = play_button.get_rect(center=(self.WIDTH // 2, (self.HEIGHT // 2) - (150 * ind)))
        self.screen.blit(play_button, self.play_rect)

        if self.play_rect.collidepoint(pygame.mouse.get_pos()):
            play_button = get_font(65, ind).render("PLAY", True, (255, 242, 204))
            self.screen.blit(play_button, self.play_rect)

        options_button = get_font(65, ind).render("OPTIONS", True, (255, 255, 255))
        self.options_rect = options_button.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2))
        self.screen.blit(options_button, self.options_rect)

        if self.options_rect.collidepoint(pygame.mouse.get_pos()):
            options_button = get_font(65, ind).render("OPTIONS", True, (255, 242, 204))
            self.screen.blit(options_button, self.options_rect)

        quit_button = get_font(65, ind).render("QUIT", True, (255, 255, 255))
        self.quit_rect = quit_button.get_rect(center=(self.WIDTH // 2, (self.HEIGHT // 2) + (150 * ind)))
        self.screen.blit(quit_button, self.quit_rect)

        if self.quit_rect.collidepoint(pygame.mouse.get_pos()):
            quit_button = get_font(65, ind).render("QUIT", True, (255, 242, 204))
            self.screen.blit(quit_button, self.quit_rect)

        self.screen.blit(menu_text, menu_rect)

    def option(self):
        self.options.start()

    def play(self):
        pacman = PacManGame(self.WIDTH, self.HEIGHT, self.background, self.background_image,
                            self.options.image_inserted)
        pacman.start_game()
