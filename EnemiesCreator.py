import copy
import math
import numpy as np
from abc import ABC, abstractmethod
from enum import Enum, auto
from level import LevelBuilder, LevelEnvironment
import pygame
from queue import PriorityQueue
from level.LevelMap import boards
from PacMan import PacMan


class Ghost(ABC):
    GHOST_SPEED = 2
    OUT_OF_BOX_GOAL = [13, 12]
    BOX_GOAL = [13, 15]

    def __init__(self, screen: pygame.surface.Surface,
                 level_controller: LevelBuilder.LevelController,
                 ghost_cell_coordinates, ghost_base_goal):
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        self.level_controller = level_controller

        self.cell_len_x, self.cell_len_y = level_controller.get_amount_of_cells()

        self.cell_width = level_controller.get_width_of_cells()
        self.cell_height = level_controller.get_height_of_cells()

        self.ghost_width = int(self.screen_height * 0.05)
        self.ghost_height = int(self.screen_height * 0.05)

        self.ghost_cell_x = ghost_cell_coordinates[0]
        self.ghost_cell_y = ghost_cell_coordinates[1]

        self.ghost_center_x = self._get_coordinate_by_cell(self.cell_width, self.ghost_cell_x, 0.5)
        self.ghost_center_y = self._get_coordinate_by_cell(self.cell_height, self.ghost_cell_y, 0.5)

        self.direction = Position.RIGHT

        self.GHOST_BASE_GOAL = ghost_base_goal
        self.ghost_goal = copy.deepcopy(self.GHOST_BASE_GOAL)

        self.rotation_allow = True
        self.is_in_box = True

        # 0-Right 1-Left 2-Up 3-Down
        self.turn_allow = self._turn_allow_update(self.ghost_cell_x, self.ghost_cell_y)

        self.start_timer = pygame.time.get_ticks()
        self.mode_durations = [10000, 60000]
        self.mode_index = 0

        self._make_opposite_access = False

    def update_position(self):

        self._goal_controller()
        self._move()
        self._draw_player()

    def _draw_player(self):
        ghost_image_x = self.ghost_center_x - self.ghost_width / 2
        ghost_image_y = self.ghost_center_y - self.ghost_height / 2

        image = self._get_image(self.ghost_width, self.ghost_height)

        self.screen.blit(image, (ghost_image_x, ghost_image_y))

    def _goal_controller(self):
        if self.is_in_box:
            self.ghost_goal = copy.deepcopy(self.OUT_OF_BOX_GOAL)
            if self.ghost_cell_x == self.ghost_goal[0] and self.ghost_cell_y == self.ghost_goal[1]:
                self.is_in_box = False
            return

        current_time = pygame.time.get_ticks()

        if current_time - self.start_timer >= self.mode_durations[self.mode_index]:
            self.mode_index = (self.mode_index + 1) % len(self.mode_durations)
            self._make_opposite_access = True
            self.start_timer = current_time

        self._make_opposite_direction()

        if self.mode_index == 0:
            self.ghost_goal = copy.deepcopy(self.GHOST_BASE_GOAL)

        elif self.mode_index == 1:
            self.ghost_goal = self._get_angry_goal()

    def _make_opposite_direction(self):
        if self._make_opposite_access:
            if self.direction == Position.RIGHT and self.turn_allow[1]:
                self.direction = Position.LEFT
                self._make_opposite_access = False
            elif self.direction == Position.LEFT and self.turn_allow[0]:
                self.direction = Position.RIGHT
                self._make_opposite_access = False
            elif self.direction == Position.UP and self.turn_allow[3]:
                self.direction = Position.DOWN
                self._make_opposite_access = False
            elif self.direction == Position.DOWN and self.turn_allow[2]:
                self.direction = Position.UP
                self._make_opposite_access = False


    def _move(self):
        self._rotation()
        self._out_of_bound_controller()

        if self.direction == Position.RIGHT and self.turn_allow[0]:  # RIGHT
            if (self.ghost_center_x + self.GHOST_SPEED
                    >= self._get_coordinate_by_cell(self.cell_width, self.ghost_cell_x + 1, 0.5)):

                self.ghost_cell_x = self.ghost_cell_x + 1
                self.turn_allow = self._turn_allow_update(self.ghost_cell_x, self.ghost_cell_y)

                if not self.turn_allow[0]:
                    self.ghost_center_x = self._get_coordinate_by_cell(self.cell_width, self.ghost_cell_x, 0.5)
                self.rotation_allow = True

            else:
                self.ghost_center_x = self.ghost_center_x + self.GHOST_SPEED
                self.rotation_allow = False

        elif self.direction == Position.LEFT and self.turn_allow[1]:  # LEFT
            if (self.ghost_center_x - self.GHOST_SPEED
                    <= self._get_coordinate_by_cell(self.cell_width, self.ghost_cell_x - 1, 0.5)):

                self.ghost_cell_x = self.ghost_cell_x - 1
                self.turn_allow = self._turn_allow_update(self.ghost_cell_x, self.ghost_cell_y)

                if not self.turn_allow[1]:
                    self.ghost_center_x = self._get_coordinate_by_cell(self.cell_width, self.ghost_cell_x, 0.5)

                self.rotation_allow = True

            else:
                self.ghost_center_x = self.ghost_center_x - self.GHOST_SPEED
                self.rotation_allow = False

        elif self.direction == Position.UP and self.turn_allow[2]:  # UP
            if (self.ghost_center_y - self.GHOST_SPEED
                    <= self._get_coordinate_by_cell(self.cell_height, self.ghost_cell_y - 1, 0.5)):

                self.ghost_cell_y = self.ghost_cell_y - 1
                self.turn_allow = self._turn_allow_update(self.ghost_cell_x, self.ghost_cell_y)

                if not self.turn_allow[2]:
                    self.ghost_center_y = self._get_coordinate_by_cell(self.cell_height, self.ghost_cell_y, 0.5)

                self.rotation_allow = True

            else:
                self.ghost_center_y = self.ghost_center_y - self.GHOST_SPEED
                self.rotation_allow = False

        elif self.direction == Position.DOWN and self.turn_allow[3]:  # DOWN
            if (self.ghost_center_y + self.GHOST_SPEED
                    >= self._get_coordinate_by_cell(self.cell_height, self.ghost_cell_y + 1, 0.5)):

                self.ghost_cell_y = self.ghost_cell_y + 1
                self.turn_allow = self._turn_allow_update(self.ghost_cell_x, self.ghost_cell_y)

                if not self.turn_allow[3]:
                    self.ghost_center_y = self._get_coordinate_by_cell(self.cell_height, self.ghost_cell_y, 0.5)

                self.rotation_allow = True

            else:
                self.ghost_center_y = self.ghost_center_y + self.GHOST_SPEED
                self.rotation_allow = False

    def _rotation(self):
        if self.rotation_allow:
            right_length = self._get_vector_distance_between_cell(self.ghost_cell_x + 1, self.ghost_cell_y,
                                                                  self.ghost_goal[0], self.ghost_goal[1])
            left_length = self._get_vector_distance_between_cell(self.ghost_cell_x - 1, self.ghost_cell_y,
                                                                 self.ghost_goal[0], self.ghost_goal[1])
            up_length = self._get_vector_distance_between_cell(self.ghost_cell_x, self.ghost_cell_y - 1,
                                                               self.ghost_goal[0], self.ghost_goal[1])
            down_length = self._get_vector_distance_between_cell(self.ghost_cell_x, self.ghost_cell_y + 1,
                                                                 self.ghost_goal[0], self.ghost_goal[1])

            data = {'right': right_length, 'left': left_length, 'up': up_length, "down": down_length}

            sorted_data = sorted(data.items(), key=lambda x: x[1], reverse=False)

            # 0-Right 1-Left 2-Up 3-Down
            for key, value in sorted_data:
                if self.turn_allow[0] and key == 'right':
                    if not self.direction == Position.LEFT:
                        self.direction = Position.RIGHT
                        return
                elif self.turn_allow[1] and key == 'left':
                    if not self.direction == Position.RIGHT:
                        self.direction = Position.LEFT
                        return
                elif self.turn_allow[2] and key == 'up':
                    if not self.direction == Position.DOWN:
                        self.direction = Position.UP
                        return
                elif self.turn_allow[3] and key == 'down':
                    if not self.direction == Position.UP:
                        self.direction = Position.DOWN
                        return

            if self.turn_allow[0] and self.direction == Position.LEFT:
                self.direction = Position.RIGHT
            elif self.turn_allow[1] and self.direction == Position.RIGHT:
                self.direction = Position.LEFT
            elif self.turn_allow[2] and self.direction == Position.DOWN:
                self.direction = Position.UP
            elif self.turn_allow[3] and self.direction == Position.UP:
                self.direction = Position.DOWN

    def _out_of_bound_controller(self):
        if self.direction == Position.RIGHT and self.ghost_cell_x + 1 == (self.cell_len_x - 1):
            self.ghost_cell_x = 0
            self.ghost_center_x = 0

        elif self.direction == Position.LEFT and self.ghost_cell_x == 0:
            self.ghost_cell_x = self.cell_len_x - 2
            self.ghost_center_x = self._get_coordinate_by_cell(self.cell_width, self.ghost_cell_x, 1)

        elif self.direction == Position.UP and self.ghost_cell_y + 1 == (self.cell_len_y - 1):
            self.ghost_cell_y = 0
            self.ghost_center_y = 0

        elif self.direction == Position.DOWN and self.ghost_cell_y == 0:
            self.ghost_cell_y = self.cell_len_y - 2
            self.ghost_center_y = self._get_coordinate_by_cell(self.cell_height, self.ghost_cell_y, 1)

    def _turn_allow_update(self, cell_x, cell_y):
        # 0-Right 1-Left 2-Up 3-Down

        return [not self._is_cell_wall(self.level_controller.get_cell(cell_x + 1, cell_y)),
                not self._is_cell_wall(self.level_controller.get_cell(cell_x - 1, cell_y)),
                not self._is_cell_wall(self.level_controller.get_cell(cell_x, cell_y - 1)),
                not self._is_cell_wall(self.level_controller.get_cell(cell_x, cell_y + 1))]

    # def draw(self, img, x_pos, y_pos):
    #     if not self.powerup and not self.dead and not self.eaten \
    #             or (self.powerup and self.dead and self.eaten and self.in_box):
    #         self.screen.blit(img, (x_pos, y_pos))
    #     elif self.powerup and not self.dead and not self.eaten:
    #         self.screen.blit(self.img_spooked, (x_pos, y_pos))
    #     elif self.powerup and self.eaten and self.dead:
    #         self.screen.blit(self.img_dead, (x_pos, y_pos))
    #
    # def get_rect(self):
    #     ghost_rect = pygame.rect.Rect((self.center_x, self.center_y), (self.ghost_width, self.ghost_height))
    #     return ghost_rect

    def _is_cell_wall(self, cell):
        if self.is_in_box and type(cell) is LevelEnvironment.Door:
            return False
        return issubclass(type(cell), LevelEnvironment.IWallAble)

    @abstractmethod
    def _get_image(self, width, height):
        pass

    @abstractmethod
    def _get_angry_goal(self):
        pass

    @staticmethod
    def _get_coordinate_by_cell(cell_size, cell_coordinate, offset):
        return cell_size * (cell_coordinate + offset)

    @staticmethod
    def _get_vector_distance_between_cell(cell_first_x, cell_first_y, cell_second_x, cell_second_y):
        return math.sqrt((cell_second_x - cell_first_x) ** 2 + (cell_second_y - cell_first_y) ** 2)
    # def pacman_collision(self, dead, eaten, target_x, target_y, powerup, speed, ghost_rect):
    #     if (pygame.Rect.colliderect(ghost_rect, self.pacman_rect) and powerup and not dead
    #             and not eaten):
    #         dead = True
    #         eaten = True
    #         target_x = int(self.pacman_game.WIDTH // 2) - 10
    #         target_y = int(self.pacman_game.HEIGHT // 2) - 100
    #         speed *= 2
    #     return dead, eaten, target_x, target_y, speed


class RedGhost(Ghost):
    IMAGE_PASS = 'ghosts/red.png'

    def __init__(self, screen: pygame.surface.Surface, level_controller: LevelBuilder.LevelController,
                 ghost_cell_coordinates, ghost_base_goal, pacman: PacMan):
        super().__init__(screen, level_controller, ghost_cell_coordinates, ghost_base_goal)
        self.pacman = pacman

    def _get_image(self, width, height):
        image = pygame.image.load(self.IMAGE_PASS)
        scaled_image = pygame.transform.scale(image, (width, height))
        return scaled_image

    def _get_angry_goal(self):
        return self.pacman.get_cell_coordinates()


class BlueGhost(Ghost):
    IMAGE_PASS = 'ghosts/blue.png'

    def __init__(self, screen: pygame.surface.Surface, level_controller: LevelBuilder.LevelController,
                 ghost_cell_coordinates, ghost_base_goal, pacman: PacMan, blinky: RedGhost):
        super().__init__(screen, level_controller, ghost_cell_coordinates, ghost_base_goal)
        self.pacman = pacman
        self.blinky = blinky

    def _get_image(self, width, height):
        image = pygame.image.load(self.IMAGE_PASS)
        scaled_image = pygame.transform.scale(image, (width, height))
        return scaled_image

    def _get_angry_goal(self):

        target_x_before_blinky = 0
        target_y_before_blinky = 0

        if (self.pacman.direction == 2 or self.pacman.direction == 1) and self.pacman.pacman_cell_x > 2:
            target_x_before_blinky = self.pacman.pacman_cell_x - 2
            target_y_before_blinky = self.pacman.pacman_cell_y

        elif self.pacman.direction == 0 and (self.pacman.pacman_cell_x + 2) < len(boards[0]):
            target_x_before_blinky = self.pacman.pacman_cell_x + 2
            target_y_before_blinky = self.pacman.pacman_cell_y

        elif self.pacman.direction == 3 and (self.pacman.pacman_cell_y + 2) < len(boards):
            target_x_before_blinky = self.pacman.pacman_cell_x
            target_y_before_blinky = self.pacman.pacman_cell_y + 2

        target_x = 2 * np.abs(self.blinky.ghost_cell_x - target_x_before_blinky)
        target_y = 2 * np.abs(self.blinky.ghost_cell_y - target_y_before_blinky)

        return target_x, target_y


class OrangeGhost(Ghost):
    IMAGE_PASS = 'ghosts/orange.png'

    def __init__(self, screen: pygame.surface.Surface, level_controller: LevelBuilder.LevelController,
                 ghost_cell_coordinates, ghost_base_goal, pacman: PacMan):
        super().__init__(screen, level_controller, ghost_cell_coordinates, ghost_base_goal)
        self.pacman = pacman

    def _get_image(self, width, height):
        image = pygame.image.load(self.IMAGE_PASS)
        scaled_image = pygame.transform.scale(image, (width, height))
        return scaled_image

    def get_distance_between_cells(self, x1, x2, y1, y2):
        return np.abs(x1 - x2) + np.abs(y1 - y2)

    def _get_angry_goal(self):
        start = (self.ghost_cell_x, self.ghost_cell_y)
        goal = (self.pacman.pacman_cell_x, self.pacman.pacman_cell_y)
        g_score = {(x, y): np.inf for x, row in enumerate(boards) for y, _ in enumerate(row)}
        g_score[start] = 0
        f_score = {(x, y): np.inf for x, row in enumerate(boards) for y, _ in enumerate(row)}
        f_score[start] = self.get_distance_between_cells(self.ghost_cell_x, goal[0],
                                                         self.ghost_cell_y, goal[1])
        pqueue = PriorityQueue()
        allowed_path = {}
        pqueue.put((f_score[start], start))
        next_cell = ()
        curr_cell = start

        while not pqueue.empty():
            item = pqueue.get()

            if isinstance(item, tuple):
                curr_cell = item[1]

            if curr_cell == goal:
                break

            if 0 <= curr_cell[0] - 1 < len(boards[0]) and 0 <= curr_cell[0] + 1 < len(boards[0]) and\
                    0 <= curr_cell[1] - 1 < len(boards) and 0 <= curr_cell[1] + 1 < len(boards):
                allowed_turns = self._turn_allow_update(curr_cell[0], curr_cell[0])

            for i in range(len(allowed_turns)):
                if i == 0:
                    next_cell = (curr_cell[0] + 1, curr_cell[1])
                if i == 1:
                    next_cell = (curr_cell[0] - 1, curr_cell[1])
                if i == 2:
                    next_cell = (curr_cell[0], curr_cell[1] - 1)
                if i == 3:
                    next_cell = (curr_cell[0], curr_cell[1] + 1)

                temp_g_score = g_score[curr_cell] + 1
                temp_f_score = temp_g_score + self.get_distance_between_cells(next_cell[0], next_cell[1], goal[0], goal[1])

                if temp_f_score < f_score.get(next_cell, np.inf):
                    allowed_path[next_cell] = curr_cell
                    g_score[next_cell] = temp_g_score
                    f_score[next_cell] = temp_f_score
                    pqueue.put((temp_f_score, next_cell))

        final_path = {}
        current = goal

        while current != start:
            final_path[allowed_path[current]] = current
            current = allowed_path[current]

        if len(final_path) < 8:
            self.ghost_goal = (0, self.screen_height)

        return self.ghost_goal


class PinkGhost(Ghost):
    IMAGE_PASS = 'ghosts/pink.png'

    def __init__(self, screen: pygame.surface.Surface, level_controller: LevelBuilder.LevelController,
                 ghost_cell_coordinates, ghost_base_goal, pacman: PacMan):
        super().__init__(screen, level_controller, ghost_cell_coordinates, ghost_base_goal)
        self.pacman = pacman
        self.get_target = False

    def _get_image(self, width, height):
        image = pygame.image.load(self.IMAGE_PASS)
        scaled_image = pygame.transform.scale(image, (width, height))
        return scaled_image

    def get_direction(self):
        if ((self.direction == 0 and self.pacman.direction == 1) or
                (self.direction == 1 and self.pacman.direction == 0)):

            if self.turn_allow[2]:
                self.direction = 2
                self.get_target = False

            elif self.turn_allow[3]:
                self.direction = 3
                self.get_target = False

            elif self.turn_allow[0] and not self.pacman.direction == 0:
                self.direction = 0
                self.get_target = False

            elif self.turn_allow[1] and not self.pacman.direction == 1:
                self.direction = 1
                self.get_target = False

        elif ((self.direction == 2 and self.pacman.direction == 3) or
              (self.direction == 3 and self.pacman.direction == 2)):

            if self.turn_allow[0]:
                self.direction = 0
                self.get_target = False

            elif self.turn_allow[1]:
                self.direction = 1
                self.get_target = False

            elif self.turn_allow[2] and not self.pacman.direction == 2:
                self.direction = 2
                self.get_target = False

            elif self.turn_allow[3] and not self.pacman.direction == 3:
                self.direction = 3
                self.get_target = False

    def _get_angry_goal(self):
        target_x, target_y = (self.pacman.pacman_cell_x, self.pacman.pacman_cell_y)
        level_x = len(boards[0])
        level_y = len(boards)

        if self.pacman.direction == 0 and (self.pacman.pacman_cell_x + 4) < level_x:
            target_x = self.pacman.pacman_cell_x + 4
            target_y = self.pacman.pacman_cell_y

        elif self.pacman.direction == 1 and self.pacman.pacman_cell_x > 4:
            target_x = self.pacman.pacman_cell_x - 4
            target_y = self.pacman.pacman_cell_y

        elif self.pacman.direction == 3 and (self.pacman.pacman_cell_y + 4) < level_y:
            target_x = self.pacman.pacman_cell_x
            target_y = self.pacman.pacman_cell_y + 4

        elif self.pacman.direction == 2 and self.pacman.pacman_cell_x > 4 and self.pacman.pacman_cell_y > 4:
            target_x = self.pacman.pacman_cell_x - 4
            target_y = self.pacman.pacman_cell_y - 4

        if (np.abs(self.ghost_cell_x - self.pacman.pacman_cell_x) < 4 and self.ghost_cell_y == self.pacman.pacman_cell_y)\
                or (np.abs(self.ghost_cell_y - self.pacman.pacman_cell_y) < 4 and self.ghost_cell_x == self.pacman.pacman_cell_x):
            self.get_target = True

        if self.get_target:
            self.get_direction()

        return target_x, target_y


class Position(Enum):
    RIGHT = auto()
    LEFT = auto()
    UP = auto()
    DOWN = auto()
    NOT_DEFINED = auto()
