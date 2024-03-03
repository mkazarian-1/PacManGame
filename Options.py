import pygame
from win32api import GetSystemMetrics


def get_font(size, ind):
    return pygame.font.Font("assets/Emulogic-zrEw.ttf", int(size * ind))


class Options:
    SCREEN_SIZES = {
        "Small": (GetSystemMetrics(1) // 2, GetSystemMetrics(1) * 0.95 // 2),
        "Medium": (GetSystemMetrics(1) // 1.5, GetSystemMetrics(1) * 0.95 // 1.5),
        "Large": (GetSystemMetrics(1) - 70, (GetSystemMetrics(1) - 70) * 0.95)
    }
    BACKGROUND_COLORS = {
        "Black": (0, 0, 0),
        "Blue": (97, 146, 178),
        "Brown": (77, 33, 34),
        "Pink": (200, 7, 111)
    }
    FPS = 60

    def __init__(self):
        self.current_screen_size = "Large"
        self.current_background_color = "Black"
        self.background_image = None
        self.image_inserted = False
        self.HEIGHT, self.WIDTH = self.SCREEN_SIZES[self.current_screen_size]
        self.back_rect = None
        self.insert_rect = None
        self.option_rects = None
        self.options = None
        self.col_option_rects = None
        self.col_options = None

    def start(self):
        pygame.init()
        timer = pygame.time.Clock()

        self.HEIGHT, self.WIDTH = self.SCREEN_SIZES[self.current_screen_size]
        screen = pygame.display.set_mode([self.WIDTH, self.HEIGHT])

        running = True

        while running:
            timer.tick(self.FPS)
            background_color = self.get_current_background_color()
            screen.fill(background_color)

            if self.image_inserted:
                screen.blit(self.background_image, (0, 0))

            self.draw_options_screen(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    for option_rect, option in zip(self.option_rects, self.options):
                        if option_rect.collidepoint(mouse_pos):
                            self.set_screen_size(option)
                            self.current_screen_size = option
                            screen = pygame.display.set_mode([self.WIDTH, self.HEIGHT])
                    for color_rect, color in zip(self.col_option_rects, self.col_options):
                        if color_rect.collidepoint(mouse_pos):
                            self.current_background_color = color
                            screen.fill(self.BACKGROUND_COLORS[color])
                            self.image_inserted = False
                    if self.insert_rect.collidepoint(mouse_pos):
                        self.image_inserted = True
                    if self.image_inserted:
                        self.insert_image()
                    if self.back_rect.collidepoint(mouse_pos):
                        return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return

            self.draw_options_screen(screen)
            pygame.display.flip()

        pygame.quit()
        return self.WIDTH, self.HEIGHT, self.get_current_background_color, self.image_inserted

    def draw_options_screen(self, screen):
        if self.current_screen_size == "Large":
            ind = 1
        elif self.current_screen_size == "Medium":
            ind = 0.7
        elif self.current_screen_size == "Small":
            ind = 0.5

        back_text = get_font(20, ind).render("Back to Menu", True, (255, 255, 255))
        self.back_rect = back_text.get_rect(topright=((self.WIDTH - 20), 20))
        screen.blit(back_text, self.back_rect)

        if self.back_rect.collidepoint(pygame.mouse.get_pos()):
            back_text = get_font(20, ind).render("Back to Menu", True, (255, 242, 204))
            screen.blit(back_text, self.back_rect)

        insert_text = get_font(25, ind).render("Image", True, (255, 255, 255))
        self.insert_rect = insert_text.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2 + (210 * ind)))
        screen.blit(insert_text, self.insert_rect)

        if self.insert_rect.collidepoint(pygame.mouse.get_pos()):
            insert_text = get_font(25, ind).render("Image", True, (255, 242, 204))
            screen.blit(insert_text, self.insert_rect)

        text = get_font(20, ind).render("Choose screen size:", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 4))
        screen.blit(text, text_rect)

        self.options = ["Small", "Medium", "Large"]
        self.option_rects = []
        for i, option in enumerate(self.options):
            option_text = get_font(25, ind).render(option, True, (255, 255, 255))
            if i < 2:
                option_rect = option_text.get_rect(
                    center=(self.WIDTH // 2 + i * (170 * ind) - (85 * ind), self.HEIGHT // 3))
            else:
                option_rect = option_text.get_rect(
                    center=(self.WIDTH // 2, self.HEIGHT // 3 + (65 * ind)))
            self.option_rects.append(option_rect)
            screen.blit(option_text, option_rect)

        col_text = get_font(20, ind).render("Choose background color:", True, (255, 255, 255))
        col_text_rect = col_text.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2 + (10 * ind)))
        screen.blit(col_text, col_text_rect)

        self.col_options = ["Black", "Blue", "Brown", "Pink"]
        self.col_option_rects = []
        for i, color in enumerate(self.col_options):
            color_text = get_font(25, ind).render(color, True, (255, 255, 255))
            if i < 2:
                color_rect = color_text.get_rect(
                    center=(self.WIDTH // 2 + i * (150 * ind) - (75 * ind), self.HEIGHT // 2 + (75 * ind)))
            else:
                color_rect = color_text.get_rect(
                    center=(self.WIDTH // 2 + (i - 2) * (150 * ind) - (75 * ind), self.HEIGHT // 2 + (140 * ind)))
            self.col_option_rects.append(color_rect)
            screen.blit(color_text, color_rect)

        mouse_pos = pygame.mouse.get_pos()
        for option_rect, option_text in zip(self.option_rects, self.options):
            if option_rect.collidepoint(mouse_pos):
                option_text = get_font(25, ind).render(option_text, True, (255, 242, 204))
                screen.blit(option_text, option_rect)
        for color_rect, color_text in zip(self.col_option_rects, self.col_options):
            if color_rect.collidepoint(mouse_pos):
                color_text = get_font(25, ind).render(color_text, True, (255, 242, 204))
                screen.blit(color_text, color_rect)

    def set_screen_size(self, option):
        self.HEIGHT, self.WIDTH = self.SCREEN_SIZES[option]

    def get_current_screen_size(self):
        return self.current_screen_size

    def get_current_background_color(self):
        return self.BACKGROUND_COLORS[self.current_background_color]

    def get_background_image(self):
        return self.background_image

    def is_image_inserted(self):
        return self.image_inserted

    def insert_image(self):
        self.background_image = pygame.image.load("assets/cute.png").convert()
        self.background_image = pygame.transform.scale(self.background_image, (self.WIDTH, self.HEIGHT))
