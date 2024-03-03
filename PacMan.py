import pygame
import LevelBuilder
import LevelEnvironment
import LevelLoopCounter
from enum import Enum, auto


class PacMan:
    PACMAN_SPEED = 2.5

    def __init__(self, screen: pygame.surface.Surface,
                 level_controller: LevelBuilder.LevelController,
                 level_loop_counter: LevelLoopCounter.LevelLoopCounter):

        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        self.level_controller = level_controller
        self.level_loop_counter = level_loop_counter

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
        self.turn_allow = self.__turn_allow_update(self.pacman_cell_x,self.pacman_cell_y)

        self.pacman_images = self.__set_pacman_image(self.pacman_width, self.pacman_height)

    def update_position(self):
        self.__pacman_move()
        self.__pacman_action()
        self.__draw_player()

    def set_turn_right(self):
        self.turn = Position.RIGHT

    def set_turn_left(self):
        self.turn = Position.LEFT

    def set_turn_up(self):
        self.turn = Position.UP

    def set_turn_down(self):
        self.turn = Position.DOWN

    def get_cell_coordinates(self):
        return [self.pacman_cell_x, self.pacman_cell_y]

    def __draw_player(self):
        pacman_x = self.pacman_center_x - self.pacman_width / 2
        pacman_y = self.pacman_center_y - self.pacman_height / 2

        image_index = self.level_loop_counter.get() // 6
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

    def __pacman_move(self):
        self.__pacman_rotation()
        self.__out_of_bound_controller()

        if self.direction == Position.RIGHT and self.turn_allow[0]:  # RIGHT
            if (self.pacman_center_x + self.PACMAN_SPEED
                    >= self.__get_coordinate_by_cell(self.cell_width, self.pacman_cell_x + 1, 0.5)):

                self.pacman_cell_x = self.pacman_cell_x + 1
                self.turn_allow = self.__turn_allow_update(self.pacman_cell_x, self.pacman_cell_y)

                if not self.turn_allow[0]:
                    self.pacman_center_x = self.__get_coordinate_by_cell(self.cell_width, self.pacman_cell_x, 0.5)
                self.rotation_allow = True

            else:
                self.pacman_center_x = self.pacman_center_x + self.PACMAN_SPEED
                self.rotation_allow = False

        elif self.direction == Position.LEFT and self.turn_allow[1]:  # LEFT
            if (self.pacman_center_x - self.PACMAN_SPEED
                    <= self.__get_coordinate_by_cell(self.cell_width, self.pacman_cell_x - 1, 0.5)):

                self.pacman_cell_x = self.pacman_cell_x - 1
                self.turn_allow = self.__turn_allow_update(self.pacman_cell_x, self.pacman_cell_y)

                if not self.turn_allow[1]:
                    self.pacman_center_x = self.__get_coordinate_by_cell(self.cell_width, self.pacman_cell_x, 0.5)

                self.rotation_allow = True

            else:
                self.pacman_center_x = self.pacman_center_x - self.PACMAN_SPEED
                self.rotation_allow = False

        elif self.direction == Position.UP and self.turn_allow[2]:  # UP
            if (self.pacman_center_y - self.PACMAN_SPEED
                    <= self.__get_coordinate_by_cell(self.cell_height, self.pacman_cell_y - 1, 0.5)):

                self.pacman_cell_y = self.pacman_cell_y - 1
                self.turn_allow = self.__turn_allow_update(self.pacman_cell_x, self.pacman_cell_y)

                if not self.turn_allow[2]:
                    self.pacman_center_y = self.__get_coordinate_by_cell(self.cell_height, self.pacman_cell_y, 0.5)

                self.rotation_allow = True

            else:
                self.pacman_center_y = self.pacman_center_y - self.PACMAN_SPEED
                self.rotation_allow = False

        elif self.direction == Position.DOWN and self.turn_allow[3]:  # DOWN
            if (self.pacman_center_y + self.PACMAN_SPEED
                    >= self.__get_coordinate_by_cell(self.cell_height, self.pacman_cell_y + 1, 0.5)):

                self.pacman_cell_y = self.pacman_cell_y + 1
                self.turn_allow = self.__turn_allow_update(self.pacman_cell_x, self.pacman_cell_y)

                if not self.turn_allow[3]:
                    self.pacman_center_y = self.__get_coordinate_by_cell(self.cell_height, self.pacman_cell_y, 0.5)

                self.rotation_allow = True

            else:
                self.pacman_center_y = self.pacman_center_y + self.PACMAN_SPEED
                self.rotation_allow = False

    def __pacman_rotation(self):

        if self.turn == Position.RIGHT and self.turn_allow[0]:
            if self.direction == Position.LEFT:
                self.direction = Position.RIGHT
                self.turn = Position.NOT_DEFINED
            elif self.rotation_allow:
                self.direction = Position.RIGHT
                self.turn = Position.NOT_DEFINED
                self.pacman_center_x = self.__get_coordinate_by_cell(self.cell_width, self.pacman_cell_x, 0.5)

        elif self.turn == Position.LEFT and self.turn_allow[1]:
            if self.direction == Position.RIGHT:
                self.direction = Position.LEFT
                self.turn = Position.NOT_DEFINED
            elif self.rotation_allow:
                self.direction = Position.LEFT
                self.turn = Position.NOT_DEFINED
                self.pacman_center_x = self.__get_coordinate_by_cell(self.cell_width, self.pacman_cell_x, 0.5)

        elif self.turn == Position.UP and self.turn_allow[2]:
            if self.direction == Position.DOWN:
                self.direction = Position.UP
                self.turn = Position.NOT_DEFINED
            elif self.rotation_allow:
                self.direction = Position.UP
                self.turn = Position.NOT_DEFINED
                self.pacman_center_y = self.__get_coordinate_by_cell(self.cell_height, self.pacman_cell_y, 0.5)

        elif self.turn == Position.DOWN and self.turn_allow[3]:
            if self.direction == Position.UP:
                self.direction = Position.DOWN
                self.turn = Position.NOT_DEFINED
            elif self.rotation_allow:
                self.direction = Position.DOWN
                self.turn = Position.NOT_DEFINED
                self.pacman_center_y = self.__get_coordinate_by_cell(self.cell_height, self.pacman_cell_y, 0.5)

    def __pacman_action(self):
        level_element = self.level_controller.get_cell(self.pacman_cell_x, self.pacman_cell_y)

        if self.__is_cell_action(level_element):
            level_element.action()
            self.level_controller.delete_cell(self.pacman_cell_x, self.pacman_cell_y)

    def __out_of_bound_controller(self):
        if self.direction == Position.RIGHT and self.pacman_cell_x + 1 == (self.cell_len_x - 1):
            self.pacman_cell_x = 0
            self.pacman_center_x = 0

        elif self.direction == Position.LEFT and self.pacman_cell_x == 0:
            self.pacman_cell_x = self.cell_len_x - 2
            self.pacman_center_x = self.__get_coordinate_by_cell(self.cell_width, self.pacman_cell_x, 1)

        elif self.direction == Position.UP and self.pacman_cell_y + 1 == (self.cell_len_y - 1):
            self.pacman_cell_y = 0
            self.pacman_center_y = 0

        elif self.direction == Position.DOWN and self.pacman_cell_y == 0:
            self.pacman_cell_y = self.cell_len_y - 2
            self.pacman_center_y = self.__get_coordinate_by_cell(self.cell_height, self.pacman_cell_y, 1)

    def __turn_allow_update(self, cell_x, cell_y):
        cell_right = self.level_controller.get_cell(cell_x + 1, cell_y)
        cell_left = self.level_controller.get_cell(cell_x - 1, cell_y)
        cell_up = self.level_controller.get_cell(cell_x, cell_y - 1)
        cell_down = self.level_controller.get_cell(cell_x, cell_y + 1)

        return [not self.__is_cell_wall(cell_right),
                not self.__is_cell_wall(cell_left),
                not self.__is_cell_wall(cell_up),
                not self.__is_cell_wall(cell_down)]

    def __is_cell_wall(self, cell):
        return issubclass(type(cell), LevelEnvironment.IWallAble)

    def __is_cell_action(self, cell):
        return issubclass(type(cell), LevelEnvironment.IActionable)

    @staticmethod
    def __set_pacman_image(width, height):
        images = []
        for i in range(1, 5):
            image = pygame.image.load(f'characters/pacman_images/{i}.png')
            scaled_image = pygame.transform.scale(image, (width, height))
            images.append(scaled_image)

        return images

    @staticmethod
    def __get_coordinate_by_cell(cell_size, cell_coordinate, offset):
        return cell_size * (cell_coordinate + offset)


class Position(Enum):
    RIGHT = auto()
    LEFT = auto()
    UP = auto()
    DOWN = auto()
    NOT_DEFINED = auto()
