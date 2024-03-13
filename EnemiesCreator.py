import copy
import math
import random
from abc import ABC, abstractmethod
from enum import Enum, auto

import Health
import Mode_Counter
import GhostStartGameCounter
import Score
from Observer import IObserver
from Position import Position
from level import LevelBuilder, LevelEnvironment
import pygame

from PacMan import PacMan


class GhostCount:
    eaten_ghosts_count = 0
    ghost_price = 0


class Ghost(IObserver, ABC):
    GHOST_SPEED = 2
    OUT_OF_BOX_GOAL = [13, 12]
    BOX_GOAL = [13, 15]
    ESCAPE_IMAGE = "ghosts/powerup.png"
    DEAD_IMAGE = "ghosts/dead.png"

    MODE_DURATION_1 = [0, 420]
    MODE_DURATION_2 = [420, 1620]
    MODE_DURATION_3 = [1620, 2040]
    MODE_DURATION_4 = [2040, 3240]
    MODE_DURATION_5 = [3240, 3540]
    MODE_DURATION_6 = [3540, 4740]
    MODE_DURATION_7 = [4740, 5040]
    MODE_DURATION_8 = [5040, None]

    def __init__(self, screen: pygame.surface.Surface,
                 level_controller: LevelBuilder.LevelController, player_health: Health.Health, pacman: PacMan,
                 ghost_cell_coordinates, ghost_base_goal, mode_counter, score, ghost_start_game_counter):
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        self.level_controller = level_controller
        self.health = player_health
        self.pacman = pacman

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
        self.mode_durations = [7000, 20000]

        self.mode_index = 0
        self.mode_durations = [
            self.MODE_DURATION_1,
            self.MODE_DURATION_2,
            self.MODE_DURATION_3,
            self.MODE_DURATION_4,
            self.MODE_DURATION_5,
            self.MODE_DURATION_6,
            self.MODE_DURATION_7,
            self.MODE_DURATION_8
        ]
        # self.ghost_img_copy = copy.deepcopy(ghost_img)

        self.ghost_rect = self.get_ghost_rect()

        self._is_ghost_dead = False

        self.usual_speed = self.GHOST_SPEED
        self.update_speed = self.GHOST_SPEED * 3

        self.is_run = True

        self.mode_counter = mode_counter
        self.ghost_start_game_counter = ghost_start_game_counter
        self.score = score

        self._is_make_opposite_access = False

        self._is_escape_mode_active = False
        self.escape_mode_duration = 7000
        self.start_escape_timer = 0

        pacman.add_observer(self)

    def update_observer(self, event):
        self._is_escape_mode_active = True
        self.start_escape_timer = pygame.time.get_ticks()
        GhostCount.eaten_ghosts_count = 0

    def update_position(self):
        self.ghost_rect = self.get_ghost_rect()
        self.collision_controller()
        self.is_ghost_in_box()

        self._goal_controller()
        self._rotation()
        self._out_of_bound_controller()
        self._move()
        self._draw_ghost()

    def _draw_ghost(self):
        ghost_image_x = self.ghost_center_x - self.ghost_width / 2
        ghost_image_y = self.ghost_center_y - self.ghost_height / 2

        image = self._get_image(self.ghost_width, self.ghost_height, self._get_ghost_base_img_pass())

        current_time = pygame.time.get_ticks()

        if self._is_ghost_dead:
            image = self._get_image(self.ghost_width, self.ghost_height, self.DEAD_IMAGE)

        elif self._is_escape_mode_active and (
                ((current_time - self.start_escape_timer) < self.escape_mode_duration * 0.8)
                or (self.start_escape_timer - current_time) % 300 > 150):
            image = self._get_image(self.ghost_width, self.ghost_height, self.ESCAPE_IMAGE)

        self.screen.blit(image, (ghost_image_x, ghost_image_y))

    def _get_escape_mode_goal(self):
        pacman_x, pacman_y = self.pacman.get_cell_coordinates()
        ghost_x, ghost_y = self.ghost_cell_x, self.ghost_cell_y

        target_x = ghost_x
        target_y = ghost_y

        vector_x = target_x - pacman_x
        vector_y = target_y - pacman_y

        target_x = pacman_x + 1.3 * vector_x
        target_y = pacman_y + 1.3 * vector_y

        random_side = random.randint(1, 5)
        if random_side == 1:
            target_x += 4
        elif random_side == 2:
            target_x -= 4
        elif random_side == 3:
            target_y += 4
        elif random_side == 4:
            target_y -= 4

        return [target_x, target_y]

    def _goal_controller(self):
        if self.is_in_box:
            self.ghost_goal = copy.deepcopy(self.OUT_OF_BOX_GOAL)
            if self.ghost_cell_x == self.ghost_goal[0] and self.ghost_cell_y == self.ghost_goal[1]:
                self.is_in_box = False
                # self.mode_index = 0
            return

        if self._is_ghost_dead:
            self.ghost_goal = self.BOX_GOAL
            self._is_escape_mode_active = False
            self.mode_counter.reset()
            self.mode_index = 0
            return

        if self._is_escape_mode_active:
            current_time = pygame.time.get_ticks()

            if current_time - self.start_escape_timer >= self.escape_mode_duration:
                self._is_escape_mode_active = False
                self.mode_index = 0
                self.mode_counter.reset()
            else:
                self.ghost_goal = self._get_escape_mode_goal()

            return

        if (self.mode_index < len(self.mode_durations) and self.mode_counter.get()
                == self.mode_durations[self.mode_index][1]):
            self.mode_index += 1
            self._is_make_opposite_access = True

        self._make_opposite_direction()

        if self.mode_index % 2 == 0 and self.mode_index < len(self.mode_durations):
            self.ghost_goal = copy.deepcopy(self.GHOST_BASE_GOAL)

        else:
            self.ghost_goal = self._get_angry_goal()

    def _make_opposite_direction(self):
        if self._is_make_opposite_access:
            if self.direction == Position.RIGHT and self.turn_allow[1]:
                self.direction = Position.LEFT
                self._is_make_opposite_access = False
            elif self.direction == Position.LEFT and self.turn_allow[0]:
                self.direction = Position.RIGHT
                self._is_make_opposite_access = False
            elif self.direction == Position.UP and self.turn_allow[3]:
                self.direction = Position.DOWN
                self._is_make_opposite_access = False
            elif self.direction == Position.DOWN and self.turn_allow[2]:
                self.direction = Position.UP
                self._is_make_opposite_access = False

    def _move(self):
        if self.direction == Position.RIGHT and self.turn_allow[0]:  # RIGHT
            if (self.ghost_center_x + self.usual_speed
                    >= self._get_coordinate_by_cell(self.cell_width, self.ghost_cell_x + 1, 0.5)):

                self.ghost_cell_x = self.ghost_cell_x + 1
                self.turn_allow = self._turn_allow_update(self.ghost_cell_x, self.ghost_cell_y)

                if not self.turn_allow[0]:
                    self.ghost_center_x = self._get_coordinate_by_cell(self.cell_width, self.ghost_cell_x, 0.5)
                self.rotation_allow = True

            else:
                self.ghost_center_x = self.ghost_center_x + self.usual_speed
                self.rotation_allow = False

        elif self.direction == Position.LEFT and self.turn_allow[1]:  # LEFT
            if (self.ghost_center_x - self.usual_speed
                    <= self._get_coordinate_by_cell(self.cell_width, self.ghost_cell_x - 1, 0.5)):

                self.ghost_cell_x = self.ghost_cell_x - 1
                self.turn_allow = self._turn_allow_update(self.ghost_cell_x, self.ghost_cell_y)

                if not self.turn_allow[1]:
                    self.ghost_center_x = self._get_coordinate_by_cell(self.cell_width, self.ghost_cell_x, 0.5)

                self.rotation_allow = True

            else:
                self.ghost_center_x = self.ghost_center_x - self.usual_speed
                self.rotation_allow = False

        elif self.direction == Position.UP and self.turn_allow[2]:  # UP
            if (self.ghost_center_y - self.usual_speed
                    <= self._get_coordinate_by_cell(self.cell_height, self.ghost_cell_y - 1, 0.5)):

                self.ghost_cell_y = self.ghost_cell_y - 1
                self.turn_allow = self._turn_allow_update(self.ghost_cell_x, self.ghost_cell_y)

                if not self.turn_allow[2]:
                    self.ghost_center_y = self._get_coordinate_by_cell(self.cell_height, self.ghost_cell_y, 0.5)

                self.rotation_allow = True

            else:
                self.ghost_center_y = self.ghost_center_y - self.usual_speed
                self.rotation_allow = False

        elif self.direction == Position.DOWN and self.turn_allow[3]:  # DOWN
            if (self.ghost_center_y + self.usual_speed
                    >= self._get_coordinate_by_cell(self.cell_height, self.ghost_cell_y + 1, 0.5)):

                self.ghost_cell_y = self.ghost_cell_y + 1
                self.turn_allow = self._turn_allow_update(self.ghost_cell_x, self.ghost_cell_y)

                if not self.turn_allow[3]:
                    self.ghost_center_y = self._get_coordinate_by_cell(self.cell_height, self.ghost_cell_y, 0.5)

                self.rotation_allow = True

            else:
                self.ghost_center_y = self.ghost_center_y + self.usual_speed
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

    def _is_cell_wall(self, cell):
        if (self.is_in_box or self._is_ghost_dead) and type(cell) is LevelEnvironment.Door\
                and ((self.ghost_start_game_counter.get() >= 120 and type(self) is PinkGhost)
                     or (self.ghost_start_game_counter.get() >= 250 and type(self) is BlueGhost) or
                     (self.ghost_start_game_counter.get() == 500 and type(self) is OrangeGhost)):
            return False
        return issubclass(type(cell), LevelEnvironment.IWallAble)

    def _get_image(self, width, height, img_path):
        image = pygame.image.load(img_path)
        scaled_image = pygame.transform.scale(image, (width, height))
        return scaled_image

    @abstractmethod
    def _get_angry_goal(self):
        pass

    @abstractmethod
    def _get_ghost_base_img_pass(self):
        pass

    @staticmethod
    def _get_coordinate_by_cell(cell_size, cell_coordinate, offset):
        return cell_size * (cell_coordinate + offset)

    @staticmethod
    def _get_vector_distance_between_cell(cell_first_x, cell_first_y, cell_second_x, cell_second_y):
        return math.sqrt((cell_second_x - cell_first_x) ** 2 + (cell_second_y - cell_first_y) ** 2)

    def get_ghost_rect(self):
        ghost_rect = pygame.rect.Rect(
            (self.ghost_center_x - self.ghost_width//5, self.ghost_center_y - self.ghost_height//6),
            (self.ghost_width//2, self.ghost_height//2))

        return ghost_rect

    def is_collision(self):
        return pygame.Rect.colliderect(self.ghost_rect, self.pacman.pacman_rect)

    def collision_controller(self):
        if self.is_collision() and not self._is_ghost_dead:
            if self._is_escape_mode_active:
                self._is_ghost_dead = True
                self.change_score()
                self.usual_speed = self.update_speed
            else:
                self.health.decrease_health()

    def change_score(self):
        GhostCount.eaten_ghosts_count += 1
        GhostCount.ghost_price = 100 * (2 ** GhostCount.eaten_ghosts_count)
        self.score.increase_score(GhostCount.ghost_price)

    def is_ghost_in_box(self):
        if 12 <= self.ghost_cell_x <= 17 and 14 <= self.ghost_cell_y <= 16:
            self._is_ghost_dead = False
            self.is_in_box = True
            self.usual_speed = self.GHOST_SPEED


class RedGhost(Ghost):
    IMAGE_PASS_RED = 'ghosts/red.png'

    def _get_ghost_base_img_pass(self):
        return self.IMAGE_PASS_RED

    def _get_angry_goal(self):
        return self.pacman.get_cell_coordinates()


class PinkGhost(Ghost):
    IMAGE_PASS_PINK = 'ghosts/pink.png'

    def _get_ghost_base_img_pass(self):
        return self.IMAGE_PASS_PINK

    def _get_angry_goal(self):
        direction = self.pacman.get_direction()
        new_goal = copy.deepcopy(self.pacman.get_cell_coordinates())

        if direction == Position.RIGHT:
            new_goal[0] += 4
        elif direction == Position.LEFT:
            new_goal[0] -= 4
        elif direction == Position.UP:
            new_goal[1] -= 4
        elif direction == Position.DOWN:
            new_goal[1] += 4

        return new_goal


class OrangeGhost(Ghost):
    IMAGE_PASS_ORANGE = 'ghosts/orange.png'

    def _get_ghost_base_img_pass(self):
        return self.IMAGE_PASS_ORANGE

    def _get_angry_goal(self):
        goal = copy.deepcopy(self.pacman.get_cell_coordinates())
        distant = self._get_vector_distance_between_cell(self.ghost_cell_x, self.ghost_cell_y, goal[0], goal[1])
        if distant >= 8:
            return goal
        return copy.deepcopy(self.GHOST_BASE_GOAL)


class BlueGhost(Ghost):
    IMAGE_PASS_BLUE = 'ghosts/blue.png'

    def _get_ghost_base_img_pass(self):
        return self.IMAGE_PASS_BLUE

    def __init__(self, screen: pygame.surface.Surface, level_controller: LevelBuilder.LevelController,
                 player_health: Health.Health, pacman: PacMan, ghost_cell_coordinates, ghost_base_goal, ghost: Ghost,
                 mode_counter, score, ghost_start_game_counter):
        super().__init__(screen, level_controller, player_health, pacman, ghost_cell_coordinates, ghost_base_goal,
                         mode_counter, score, ghost_start_game_counter)
        self.ghost = ghost

    def _get_angry_goal(self):

        direction = self.pacman.get_direction()
        pacman_x, pacman_y = self.pacman.get_cell_coordinates()
        blinky_x, blinky_y = self.ghost.ghost_cell_x, self.ghost.ghost_cell_y

        if direction == Position.RIGHT:
            target_x = pacman_x + 2
            target_y = pacman_y
        elif direction == Position.LEFT:
            target_x = pacman_x - 2
            target_y = pacman_y
        elif direction == Position.DOWN:
            target_x = pacman_x
            target_y = pacman_y + 2
        else:
            target_x = pacman_x
            target_y = pacman_y - 2

        vector_x = target_x - blinky_x
        vector_y = target_y - blinky_y

        target_x = blinky_x + 2 * vector_x
        target_y = blinky_y + 2 * vector_y

        return [target_x, target_y]
