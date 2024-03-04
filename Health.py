import pygame


class Health:
    BASE_HEALTH = 3
    IMAGE_PASS = "characters/pacman_images/1.png"

    def __init__(self, screen: pygame.surface.Surface):
        self.__screen = screen
        self.__health = self.BASE_HEALTH

    def decrease_health(self):
        self.__health -= 1
        if self.__health <= 0:
            print("Game over")

    def draw(self, width, height):
        image = pygame.image.load(self.IMAGE_PASS)
        image_width = self.__screen.get_width() * 0.04
        image_height = self.__screen.get_width() * 0.04
        scaled_image = pygame.transform.scale(image, (image_width, image_height))

        for i in range(self.__health):
            self.__screen.blit(scaled_image, (width + (i * image_width), height ))
