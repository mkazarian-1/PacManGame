import pygame


class PlayerScore:
    def __init__(self, screen):
        self.__score = 0
        self.__screen = screen

    def get_score(self):
        return self.__score

    def increase_score(self, value):
        self.__score += value

    def clera_score(self):
        self.__score = 0

    def draw_score(self, width, height):
        font = pygame.font.Font("assets/Emulogic-zrEw.ttf", 24)
        score_text = font.render(f'Score:{self.get_score()}', True, (255, 255, 255))
        self.__screen.blit(score_text, (width, height))
