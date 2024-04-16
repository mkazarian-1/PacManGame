import pygame
import sys

pygame.init()


def get_font(size, ind):
    return pygame.font.Font("assets/Emulogic-zrEw.ttf", int(size * ind))


class Menu:
    def __init__(self, screen_settings):
        self.screen_settings = screen_settings
        self.play_rect = None
        self.options_rect = None
        self.quit_rect = None
        self.ind = screen_settings.get_ind()
        self.WIDTH = None
        self.HEIGHT = None

    def start(self):
        pygame.display.set_caption("PacMan")
        clock = pygame.time.Clock()

        screen_size = self.screen_settings.get_screen_size()
        self.HEIGHT, self.WIDTH = self.screen_settings.SCREEN_SIZES[screen_size]
        screen = pygame.display.set_mode([self.WIDTH, self.HEIGHT])

        self.draw_menu(screen)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    menu_mouse_pos = pygame.mouse.get_pos()
                    if self.play_rect.collidepoint(menu_mouse_pos):
                        self.play()
                    if self.options_rect.collidepoint(menu_mouse_pos):
                        self.option()
                    if self.quit_rect.collidepoint(menu_mouse_pos):
                        pygame.quit()

            screen.fill(self.screen_settings.get_background_color())
            if self.screen_settings.is_image_inserted():
                screen.blit(self.screen_settings.get_background_image(), (0, 0))
            self.draw_menu(screen)
            pygame.display.flip()
            clock.tick(60)

        pygame.quit()

    def draw_menu(self, screen):
        self.WIDTH, self.HEIGHT = screen.get_size()  # Отримання розміру екрану
        menu_text = get_font(65, self.ind).render("MAIN MENU", True, "#f4cd33")
        menu_rect = menu_text.get_rect(center=(self.WIDTH // 2, (self.HEIGHT // 2) - (300 * self.ind)))
        screen.blit(menu_text, menu_rect)

        play_button = get_font(65, self.ind).render("PLAY", True, (255, 255, 255))
        self.play_rect = play_button.get_rect(center=(self.WIDTH // 2, (self.HEIGHT // 2) - (150 * self.ind)))
        screen.blit(play_button, self.play_rect)

        if self.play_rect.collidepoint(pygame.mouse.get_pos()):
            play_button = get_font(65, self.ind).render("PLAY", True, (255, 242, 204))
            screen.blit(play_button, self.play_rect)

        options_button = get_font(65, self.ind).render("OPTIONS", True, (255, 255, 255))
        self.options_rect = options_button.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2))
        screen.blit(options_button, self.options_rect)

        if self.options_rect.collidepoint(pygame.mouse.get_pos()):
            options_button = get_font(65, self.ind).render("OPTIONS", True, (255, 242, 204))
            screen.blit(options_button, self.options_rect)

        quit_button = get_font(65, self.ind).render("QUIT", True, (255, 255, 255))
        self.quit_rect = quit_button.get_rect(center=(self.WIDTH // 2, (self.HEIGHT // 2) + (150 * self.ind)))
        screen.blit(quit_button, self.quit_rect)

        if self.quit_rect.collidepoint(pygame.mouse.get_pos()):
            quit_button = get_font(65, self.ind).render("QUIT", True, (255, 242, 204))
            screen.blit(quit_button, self.quit_rect)

    def option(self):
        from src.menu_pg.Options import Options
        options_screen = Options(self.screen_settings)
        options_screen.start()

    def play(self):
        from src.PacManGame import PacManGame
        pacman = PacManGame(self.screen_settings)
        pacman.start_game()

