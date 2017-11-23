from src.config.app import App
from .difficulty import Difficulty
from .level import Level
from .renderer import Renderer
from .enums import Direction, CellType
from .grid import Grid
from copy import deepcopy
from .position import Position
from .snake import Snake
from random import randint


class LevelRunner():
    def __init__(self, renderer: Renderer, level: Level, difficulty: Difficulty, score: int = 0):
        self.renderer = renderer
        self.grid = level.grid
        self.difficulty = difficulty
        self.snake = deepcopy(level.snake)
        self._direction = level.initial_direction
        self._last_used_direction = level.initial_direction
        self._is_game_over = False
        self.food_position = self._get_random_free_position()
        self.crash_position = None
        self.difficulty = difficulty
        self.food_eaten = 0
        self.initial_score = score
        self.food_count_to_complete = level.food_count_to_complete

    @property
    def direction(self) -> Direction:
        return self._direction

    def set_new_direction(self, direction: Direction) -> None:
        if not self._last_used_direction.is_opposite(direction):
            self._direction = direction

    def is_game_over(self) -> bool:
        return self._is_game_over

    def is_level_completed(self) -> bool:
        return self.food_eaten == self.food_count_to_complete

    def get_total_score(self) -> int:
        return self.food_eaten * self.difficulty.score_multiplier + self.initial_score

    def render_frame(self) -> None:
        self.renderer.render_level(self.snake, self.grid, self.food_position, self.crash_position)

    def _get_random_free_position(self) -> Position:
        position_is_free = False
        position = None

        while not position_is_free:
            position = self._get_random_position_in_grid()
            position_free_from_snake = position not in self.snake.positions
            position_is_free = self.grid.get_cell_at(position) == CellType.NONE.value and position_free_from_snake

        return position

    def _get_random_position_in_grid(self) -> Position:
        return Position(randint(0, self.grid.width - 1), randint(0, self.grid.height - 1))

    def make_game_turn(self) -> None:
        self.snake.prepend_head_at_direction(self._direction)
        self._last_used_direction = self._direction
        cell_value = self.grid.get_cell_at(self.snake.head_position)

        App.Logger.debug("Food eaten = {}, to complete = {}".format(self.food_eaten, self.food_count_to_complete))

        if self.snake.head_position == self.food_position:
            self.food_eaten += 1
            if not self.is_level_completed():
                self.food_position = self._get_random_free_position()
            else:
                self.food_position = None
        elif cell_value == CellType.WALL.value or self.snake.has_self_interceptions():
            self._is_game_over = True
            self.crash_position = self.snake.head_position
        else:
            self.snake.pop_tail()