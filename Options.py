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
        "Green": (59, 143, 110)
    }
    FPS = 60

    # Встановлюємо чорний колір фону і великий розмір екрану за замовчуванням
    def __init__(self):
        self.current_screen_size = "Large"
        self.current_background_color = "Black"

    def start(self):
        pygame.init()

        timer = pygame.time.Clock()

        # Отримуємо розміри екрану для поточної опції
        self.HEIGHT, self.WIDTH = self.SCREEN_SIZES[self.current_screen_size]
        screen = pygame.display.set_mode([self.WIDTH, self.HEIGHT])  # Створюємо вікно з відповідними розмірами

        running = True
        show_options = False
        show_colors = False

        while running:
            timer.tick(self.FPS)
            background_color = self.get_current_background_color()
            screen.fill(background_color)

            if self.current_screen_size == "Large":
                ind = 1
            elif self.current_screen_size == "Medium":
                ind = 0.7
            elif self.current_screen_size == "Small":
                ind = 0.5

            # Відображення кнопки "Повернутися до меню" у кутку екрану
            back_text = get_font(20, ind).render("Back to Menu", True, (255, 255, 255))
            back_rect = back_text.get_rect(topright=(self.WIDTH - 20, 20))
            screen.blit(back_text, back_rect)

            # Відображення тексту та кнопки для спадного списку розмірів екрану
            text = get_font(20, ind).render("Choose screen size:", True, (255, 255, 255))
            text_rect = text.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 4))
            screen.blit(text, text_rect)

            # Відображення спадного списку розмірів екрану
            options = ["Small", "Medium", "Large"]
            option_rects = []
            for i, option in enumerate(options):
                option_text = get_font(25, ind).render(option, True, (255, 255, 255))
                option_rect = option_text.get_rect(
                    center=(self.WIDTH // 2 + i * (170 * ind) - (170 * ind), self.HEIGHT // 3))
                option_rects.append(option_rect)
                if show_options:
                    screen.blit(option_text, option_rect)

            # Відображення тексту та кнопки для спадного списку кольорів
            col_text = get_font(20, ind).render("Choose background color:", True, (255, 255, 255))
            col_text_rect = col_text.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2))
            screen.blit(col_text, col_text_rect)

            # Відображення спадного списку кольорів
            col_options = ["Black", "Blue", "Brown", "Green"]
            col_option_rects = []
            for i, color in enumerate(col_options):
                color_text = get_font(25, ind).render(color, True, (255, 255, 255))
                if i < 2:  # Перші дві кнопки
                    color_rect = color_text.get_rect(
                        center=(self.WIDTH // 2 + i * (150 * ind) - (75 * ind), self.HEIGHT // 2 + (50 * ind)))
                else:  # Наступні дві кнопки
                    color_rect = color_text.get_rect(
                        center=(self.WIDTH // 2 + (i - 2) * (150 * ind) - (75 * ind), self.HEIGHT // 2 + (120 * ind)))
                col_option_rects.append(color_rect)
                if show_colors:
                    screen.blit(color_text, color_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if text_rect.collidepoint(mouse_pos):
                        show_options = not show_options
                        show_colors = False  # При показі розмірів екрану приховуємо спадне меню кольорів
                    elif col_text_rect.collidepoint(mouse_pos):
                        show_colors = not show_colors
                        show_options = False
                    if show_options:
                        for option_rect, option in zip(option_rects, options):
                            if option_rect.collidepoint(mouse_pos):
                                self.set_screen_size(option)
                                self.current_screen_size = option
                                show_options = False
                                screen = pygame.display.set_mode([self.WIDTH, self.HEIGHT])
                    if show_colors:
                        for color_rect, color in zip(col_option_rects, col_options):
                            if color_rect.collidepoint(mouse_pos):
                                self.current_background_color = color
                                show_colors = False
                                screen.fill(self.BACKGROUND_COLORS[color])
                    if back_rect.collidepoint(mouse_pos):
                        return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return

            pygame.display.flip()

        pygame.quit()
        return self.WIDTH, self.HEIGHT, self.get_current_background_color

    def set_screen_size(self, option):
        # Встановлення розміру вікна
        self.HEIGHT, self.WIDTH = self.SCREEN_SIZES[option]

    def get_current_screen_size(self):
        # Отримання поточного розміру вікна
        return self.current_screen_size

    def get_current_background_color(self):
        # Отримання поточного кольору фону
        return self.BACKGROUND_COLORS[self.current_background_color]
