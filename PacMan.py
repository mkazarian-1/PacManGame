import pygame


class PacMan:
    def __init__(self, screen_width, screen_height, level):
        self.screen_width = screen_width
        self.screen_height = screen_height
        # розмір пакмана робиться відповідно до розміра вікна, треба перевірити, чи на всіх екранах все співпадає
        self.pacman_width = int(screen_height * 0.05)
        self.pacman_height = int(screen_height * 0.05)
        self.pacman_halfWidth = self.pacman_width // 2
        self.pacman_halfHeight = self.pacman_height // 2
        self.level = level
        self.pacman_speed = 2

        self.pacman_images = []
        for i in range(1, 5):
            image = pygame.image.load(f'characters/pacman_images/{i}.png')
            scaled_image = pygame.transform.scale(image, (self.pacman_width, self.pacman_height))
            self.pacman_images.append(scaled_image)

        self.player_x = screen_width // 2
        self.player_y = screen_height // 2
        self.direction = 0
        self.center_x = self.player_x + self.pacman_halfWidth
        self.center_y = self.player_y + self.pacman_halfHeight

    def draw_player(self, screen, counter):
        # 0-RIGHT, 1-LEFT, 2-UP, 3-DOWN
        image_index = counter // 6
        if 0 <= image_index < len(self.pacman_images):
            if self.direction == 0:
                screen.blit(self.pacman_images[image_index], (self.player_x, self.player_y))
            elif self.direction == 1:
                screen.blit(pygame.transform.flip(self.pacman_images[image_index], True, False),
                            (self.player_x, self.player_y))
            elif self.direction == 2:
                screen.blit(pygame.transform.rotate(self.pacman_images[image_index], 90),
                            (self.player_x, self.player_y))
            elif self.direction == 3:
                screen.blit(pygame.transform.rotate(self.pacman_images[image_index], 270),
                            (self.player_x, self.player_y))
        else:
            pass

    def can_move(self, direction):
        next_x, next_y = self.player_x, self.player_y
        if direction == 0:  # RIGHT
            next_x += self.pacman_speed
        elif direction == 1:  # LEFT
            next_x -= self.pacman_speed
        elif direction == 2:  # UP
            next_y -= self.pacman_speed
        elif direction == 3:  # DOWN
            next_y += self.pacman_speed

        # Check if next position is within bounds and not a wall
        if (0 <= next_x < self.screen_width - self.pacman_width and
                0 <= next_y < self.screen_height - self.pacman_height and
                self.level[int(next_y // self.pacman_height)][int(next_x // self.pacman_width)] < 3):
            return True
        return False

    def update_position(self):
        if self.direction == 0:  # RIGHT
            self.player_x += self.pacman_speed
        elif self.direction == 1:  # LEFT
            self.player_x -= self.pacman_speed
        elif self.direction == 2:  # UP
            self.player_y -= self.pacman_speed
        elif self.direction == 3:  # DOWN
            self.player_y += self.pacman_speed

        self.center_x = self.player_x + self.pacman_halfWidth
        self.center_y = self.player_y + self.pacman_halfHeight
