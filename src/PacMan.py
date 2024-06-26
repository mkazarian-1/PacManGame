import pygame

from src.Observer import Observable
from src.Position import Position
from src.level import LevelBuilder, LevelEnvironment
from src.level.LevelBuilder import LevelController


class PacMan(Observable):
    PACMAN_SPEED = 2.5

    def __init__(self, screen: pygame.surface.Surface, level_controller: LevelBuilder.LevelController):

        super().__init__()
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        self.level_controller = level_controller

        self.cell_len_x, self.cell_len_y = level_controller.get_amount_of_cells()

        self.cell_width = level_controller.get_width_of_cells()
        self.cell_height = level_controller.get_height_of_cells()

        self.pacman_width = int(self.screen_height * 0.05)
        self.pacman_height = int(self.screen_height * 0.05)

        self.pacman_cell_x = 15
        self.pacman_cell_y = 18

        self.pacman_center_x = self.pacman_cell_x * self.cell_width + self.cell_width / 2
        self.pacman_center_y = self.pacman_cell_y * self.cell_height + self.cell_height / 2

        self.direction = Position.UP
        self.turn = Position.NOT_DEFINED
        self.rotation_allow = True

        # 0-Right 1-Left 2-Up 3-Down
        self.turn_allow = self.turn_allow_update(self.pacman_cell_x, self.pacman_cell_y)

        self.pacman_images = self.set_pacman_image(self.pacman_width, self.pacman_height)

        self.pacman_rect = self.get_pacman_rect()

        self.pacman_dead = False

    def set_turn_right(self):
        self.turn = Position.RIGHT

    def set_turn_left(self):
        self.turn = Position.LEFT

    def set_turn_up(self):
        self.turn = Position.UP

    def set_turn_down(self):
        self.turn = Position.DOWN

    def get_direction(self):
        return self.direction

    def get_cell_coordinates(self):
        return [self.pacman_cell_x, self.pacman_cell_y]

    def draw_player(self):
        pacman_x = self.pacman_center_x - self.pacman_width / 2
        pacman_y = self.pacman_center_y - self.pacman_height / 2

        current_time = pygame.time.get_ticks()

        image_index = int((current_time % 400) * 0.01)

        if 0 <= image_index < len(self.pacman_images):
            if self.direction == Position.RIGHT:
                self.screen.blit(pygame.transform.rotate(self.pacman_images[image_index], 0),
                                 (pacman_x, pacman_y))
            elif self.direction == Position.LEFT:
                self.screen.blit(pygame.transform.rotate(self.pacman_images[image_index], 180),
                                 (pacman_x, pacman_y))
            elif self.direction == Position.UP:
                self.screen.blit(pygame.transform.rotate(self.pacman_images[image_index], 90),
                                 (pacman_x, pacman_y))
            elif self.direction == Position.DOWN:
                self.screen.blit(pygame.transform.rotate(self.pacman_images[image_index], 270),
                                 (pacman_x, pacman_y))
        else:
            pass

    def update_position(self):
        if self.rotation_allow and not self.turn_allow[self.direction.value - 1]:
            self.pacman_center_x = self.get_coordinate_by_cell(self.cell_width, self.pacman_cell_x, 0.5)
            self.pacman_center_y = self.get_coordinate_by_cell(self.cell_height, self.pacman_cell_y, 0.5)

        self.direction = self.pacman_rotation(self.direction, self.turn_allow)

        if self.is_out_of_bounds(self.direction, self.pacman_cell_x, self.pacman_cell_y):
            self.pacman_cell_x, self.pacman_cell_y = self.out_of_bound_controller(self.direction,
                                                                                  self.pacman_cell_x,
                                                                                  self.pacman_cell_y)
            self.pacman_center_x = self.get_coordinate_by_cell(self.cell_width, self.pacman_cell_x, 0.5)
            self.pacman_center_y = self.get_coordinate_by_cell(self.cell_height, self.pacman_cell_y, 0.5)

        self.pacman_move()

        self.pacman_action(self.pacman_cell_x, self.pacman_cell_y)
        self.draw_player()
        self.pacman_rect = self.get_pacman_rect()

    def pacman_move(self):
        if self.direction == Position.RIGHT and self.turn_allow[0]:  # RIGHT
            if (self.pacman_center_x + self.PACMAN_SPEED
                    >= self.get_coordinate_by_cell(self.cell_width, self.pacman_cell_x + 1, 0.5)):

                self.pacman_cell_x = self.pacman_cell_x + 1
                self.turn_allow = self.turn_allow_update(self.pacman_cell_x, self.pacman_cell_y)

                self.rotation_allow = True

            else:
                self.pacman_center_x = self.pacman_center_x + self.PACMAN_SPEED
                self.rotation_allow = False

        elif self.direction == Position.LEFT and self.turn_allow[1]:  # LEFT
            if (self.pacman_center_x - self.PACMAN_SPEED
                    <= self.get_coordinate_by_cell(self.cell_width, self.pacman_cell_x - 1, 0.5)):

                self.pacman_cell_x = self.pacman_cell_x - 1
                self.turn_allow = self.turn_allow_update(self.pacman_cell_x, self.pacman_cell_y)

                self.rotation_allow = True

            else:
                self.pacman_center_x = self.pacman_center_x - self.PACMAN_SPEED
                self.rotation_allow = False

        elif self.direction == Position.UP and self.turn_allow[2]:  # UP
            if (self.pacman_center_y - self.PACMAN_SPEED
                    <= self.get_coordinate_by_cell(self.cell_height, self.pacman_cell_y - 1, 0.5)):

                self.pacman_cell_y = self.pacman_cell_y - 1
                self.turn_allow = self.turn_allow_update(self.pacman_cell_x, self.pacman_cell_y)
                self.rotation_allow = True

            else:
                self.pacman_center_y = self.pacman_center_y - self.PACMAN_SPEED
                self.rotation_allow = False

        elif self.direction == Position.DOWN and self.turn_allow[3]:  # DOWN
            if (self.pacman_center_y + self.PACMAN_SPEED
                    >= self.get_coordinate_by_cell(self.cell_height, self.pacman_cell_y + 1, 0.5)):

                self.pacman_cell_y = self.pacman_cell_y + 1
                self.turn_allow = self.turn_allow_update(self.pacman_cell_x, self.pacman_cell_y)

                self.rotation_allow = True

            else:
                self.pacman_center_y = self.pacman_center_y + self.PACMAN_SPEED
                self.rotation_allow = False

    def pacman_rotation(self, direction, turn_allow):
        if self.turn == Position.RIGHT and turn_allow[0]:
            if direction == Position.LEFT:
                direction = Position.RIGHT
                self.turn = Position.NOT_DEFINED

            elif self.rotation_allow:
                direction = Position.RIGHT
                self.turn = Position.NOT_DEFINED

        elif self.turn == Position.LEFT and turn_allow[1]:
            if direction == Position.RIGHT:
                direction = Position.LEFT
                self.turn = Position.NOT_DEFINED
            elif self.rotation_allow:
                direction = Position.LEFT
                self.turn = Position.NOT_DEFINED

        elif self.turn == Position.UP and turn_allow[2]:
            if direction == Position.DOWN:
                direction = Position.UP
                self.turn = Position.NOT_DEFINED
            elif self.rotation_allow:
                direction = Position.UP
                self.turn = Position.NOT_DEFINED

        elif self.turn == Position.DOWN and turn_allow[3]:
            if direction == Position.UP:
                direction = Position.DOWN
                self.turn = Position.NOT_DEFINED
            elif self.rotation_allow:
                direction = Position.DOWN
                self.turn = Position.NOT_DEFINED

        return direction

    def pacman_action(self, pacman_cell_x, pacman_cell_y):
        level_element = self.level_controller.get_cell(pacman_cell_x, pacman_cell_y)

        if self.is_cell_action(level_element):
            level_element.action()
            self.level_controller.delete_cell(pacman_cell_x, pacman_cell_y)
            if type(level_element) is LevelEnvironment.Energiser:
                self.notify_observers("power_pellet_eaten")

    def out_of_bound_controller(self, direction, pacman_cell_x, pacman_cell_y):
        if direction == Position.RIGHT and pacman_cell_x + 1 == (self.cell_len_x - 1):
            pacman_cell_x = 0

        elif direction == Position.LEFT and pacman_cell_x == 0:
            pacman_cell_x = self.cell_len_x - 2

        elif direction == Position.UP and pacman_cell_y + 1 == (self.cell_len_y - 1):
            pacman_cell_y = 0

        elif direction == Position.DOWN and pacman_cell_y == 0:
            pacman_cell_y = self.cell_len_y - 2

        return pacman_cell_x, pacman_cell_y

    def is_out_of_bounds(self, direction, pacman_cell_x, pacman_cell_y):
        return ((direction == Position.RIGHT and pacman_cell_x + 1 == (self.cell_len_x - 1))
                or (direction == Position.LEFT and pacman_cell_x == 0)
                or (direction == Position.UP and pacman_cell_y + 1 == (self.cell_len_y - 1))
                or (direction == Position.DOWN and pacman_cell_y == 0))

    # --- level_controller
    def turn_allow_update(self, cell_x, cell_y):
        cell_right = self.level_controller.get_cell(cell_x + 1, cell_y)
        cell_left = self.level_controller.get_cell(cell_x - 1, cell_y)
        cell_up = self.level_controller.get_cell(cell_x, cell_y - 1)
        cell_down = self.level_controller.get_cell(cell_x, cell_y + 1)

        return [not self.is_cell_wall(cell_right),
                not self.is_cell_wall(cell_left),
                not self.is_cell_wall(cell_up),
                not self.is_cell_wall(cell_down)]

    # --- know
    def is_cell_wall(self, cell):
        return issubclass(type(cell), LevelEnvironment.IWallAble)

    # --- know
    def is_cell_action(self, cell):
        return issubclass(type(cell), LevelEnvironment.IActionable)

    @staticmethod
    def set_pacman_image(width, height):
        images = []
        for i in range(1, 5):
            image = pygame.image.load(f'characters/pacman_images/{i}.png')
            scaled_image = pygame.transform.scale(image, (width, height))
            images.append(scaled_image)

        return images

    @staticmethod
    def get_coordinate_by_cell(cell_size, cell_coordinate, offset):
        return cell_size * (cell_coordinate + offset)

    def get_pacman_rect(self):
        pacman_rect = pygame.rect.Rect(
            (self.pacman_center_x - self.pacman_width // 5, self.pacman_center_y - self.pacman_height // 5),
            (self.pacman_width // 2, self.pacman_height // 2))
        return pacman_rect
