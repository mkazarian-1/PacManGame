import pygame
from win32api import GetSystemMetrics

class Options:
    HEIGHT = GetSystemMetrics(1) - 70
    WIDTH = HEIGHT * 0.95
    FPS = 60

    def start(self):
        pygame.init()

        timer = pygame.time.Clock()

        screen = pygame.display.set_mode([self.WIDTH, self.HEIGHT])

        running = True

        while running:
            timer.tick(self.FPS)
            screen.fill("black")

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            pygame.display.flip()

        pygame.quit()

