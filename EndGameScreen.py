import pygame

def get_font(size, ind):
    return pygame.font.Font("assets/Emulogic-zrEw.ttf", int(size * ind))


class EndGameScreen:
    def __init__(self, screen_settings, score, is_win):
        self.screen_settings = screen_settings
        self.current_screen_size = self.screen_settings.get_screen_size()
        self.score = score
        self.is_win = is_win
        self.set_screen_size()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.ind = screen_settings.get_ind()
        self.play_rect = None
        self.menu_rect = None

    def set_screen_size(self):
        self.HEIGHT, self.WIDTH = self.screen_settings.SCREEN_SIZES[self.current_screen_size]

    def show_game_over(self):
        pygame.init()
        clock = pygame.time.Clock()
        screen = self.screen
        self.draw_end(screen)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    menu_mouse_pos = pygame.mouse.get_pos()
                    if self.play_rect.collidepoint(menu_mouse_pos):
                        self.play()
                    if self.menu_rect.collidepoint(menu_mouse_pos):
                        self.back_to_menu()
            self.draw_end(screen)
            pygame.display.flip()
            clock.tick(60)
        pygame.quit()

    def draw_end(self, screen):
        overlay = pygame.Surface(screen.get_size())
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        if self.is_win:
            title = "You win!!!"
            dye = (255, 255, 0)
        else:
            title = "Game over"
            dye = (255, 0, 0)

        text = get_font(65, self.ind).render(title, True, dye)
        text_rect = text.get_rect(center=(self.WIDTH // 2, (self.HEIGHT // 2) - (250 * self.ind)))
        screen.blit(text, text_rect)

        score_text = get_font(30, self.ind).render("Score: " + str(self.score), True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(self.WIDTH // 2, (self.HEIGHT // 2) - (160 * self.ind)))
        screen.blit(score_text, score_rect)

        play_button = get_font(55, self.ind).render("Restart", True, (255, 255, 255))
        self.play_rect = play_button.get_rect(center=(self.WIDTH // 2, (self.HEIGHT // 2) - (35 * self.ind)))
        screen.blit(play_button, self.play_rect)

        if self.play_rect.collidepoint(pygame.mouse.get_pos()):
            play_button = get_font(55, self.ind).render("Restart", True, (255, 242, 204))
            screen.blit(play_button, self.play_rect)

        menu_button = get_font(55, self.ind).render("Back to menu", True, (255, 255, 255))
        self.menu_rect = menu_button.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2 + (105 * self.ind)))
        screen.blit(menu_button, self.menu_rect)

        if self.menu_rect.collidepoint(pygame.mouse.get_pos()):
            menu_button = get_font(55, self.ind).render("Back to menu", True, (255, 242, 204))
            screen.blit(menu_button, self.menu_rect)

    def back_to_menu(self):
        from menu_pg.Menu import Menu
        menu = Menu(self.screen_settings)
        menu.start()

    def play(self):
        from PacManGame import PacManGame
        pacman = PacManGame(self.screen_settings)
        pacman.start_game()

