from copy import deepcopy
from typing import Optional
from .level import Level
from .snake import Snake
from .position import Position
from .enums import LevelOutcome


class LevelState():
    """
    A structure representing current game state during level walkthrough.
    """
    def __init__(
        self,
        level: Level,
        snake: Snake,
        food_position: Position,
        crash_position: Optional[Position],
        level_outcome: LevelOutcome,
        current_score: int
    ):
        self._level = level
        self._snake = deepcopy(snake)
        self._food_position = food_position
        self._crash_position = crash_position
        self._level_outcome = level_outcome
        self._score = current_score

    @property
    def level(self) -> Level:
        return self._level

    @property
    def snake(self) -> Snake:
        return self._snake

    @property
    def food_position(self) -> Optional[Position]:
        return self._food_position

    @property
    def crash_position(self) -> Optional[Position]:
        return self._crash_position

    @property
    def level_out(self) -> Optional[LevelOutcome]:
        return self._level_outcome\

    @property
    def score(self) -> int:
        return self._score
