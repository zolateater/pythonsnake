from typing import Optional

from ..config.app import App
from .level_state import LevelState
from .difficulty import Difficulty
from .level import Level
from .renderer import Renderer
from .enums import Direction, CellType, LevelOutcome
from .grid import Grid
from copy import deepcopy
from .position import Position
from .snake import Snake
from random import randint


class LevelRunner():
    def __init__(self, level: Level, difficulty: Difficulty, score: int = 0):
        self.level = level
        self.difficulty = difficulty
        self.snake = deepcopy(level.snake)
        self.food_position = self._get_random_free_position()
        self.crash_position = None
        self.difficulty = difficulty
        self.food_eaten = 0
        self.initial_score = score
        self._level_outcome = None # type: Optional[LevelOutcome]
        self._direction = level.initial_direction
        self._last_used_direction = level.initial_direction

    @property
    def direction(self) -> Direction:
        return self._direction

    @property
    def level_outcome(self) -> Optional[LevelOutcome]:
        return self._level_outcome

    def handle_direction_change(self, direction: Direction) -> None:
        if not self._last_used_direction.is_opposite(direction):
            self._direction = direction

    def get_total_score(self) -> int:
        return self.food_eaten * self.difficulty.score_multiplier + self.initial_score

    def get_level_state(self) -> LevelState:
        return LevelState(self.level, self.snake, self.food_position, self.crash_position, self._level_outcome, self.get_total_score())

    def make_game_turn(self) -> None:
        if self._level_outcome is not None:
            raise LevelAlreadyCompletedError()

        self.snake.prepend_head_at_direction(self._direction)
        self._last_used_direction = self._direction
        cell_value = self.level.grid.get_cell_at(self.snake.head_position)

        if self.snake.head_position == self.food_position:
            self.food_eaten += 1
            if not self._is_level_completed():
                self.food_position = self._get_random_free_position()
            else:
                self.food_position = None
                self._level_outcome = LevelOutcome.LEVEL_COMPLETED
        elif cell_value == CellType.WALL.value or self.snake.has_self_interceptions():
            self._level_outcome = LevelOutcome.GAME_OVER
            self.crash_position = self.snake.head_position
        else:
            self.snake.pop_tail()

    def _get_random_free_position(self) -> Position:
        position_is_free = False
        position = None

        while not position_is_free:
            position = self._get_random_position_in_grid()
            position_free_from_snake = position not in self.snake.positions
            position_is_free = self.level.grid.get_cell_at(position) == CellType.NONE.value and position_free_from_snake

        return position

    def _get_random_position_in_grid(self) -> Position:
        return Position(randint(0, self.level.grid.width - 1), randint(0, self.level.grid.height - 1))

    def _is_level_completed(self) -> bool:
        return self.food_eaten == self.level.food_count_to_complete


class LevelAlreadyCompletedError(Exception):
    pass