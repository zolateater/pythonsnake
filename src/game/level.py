from .enums import Direction
from .grid import Grid
from .snake import Snake


class Level():
    def __init__(self, snake: Snake, grid: Grid, initial_direction: Direction, food_count_to_complete: int) -> None:
        self._snake = snake
        self._initial_direction = initial_direction
        self._grid = grid
        self._food_count_to_complete = food_count_to_complete

    @property
    def snake(self) -> Snake:
        return self._snake

    @property
    def initial_direction(self) -> Direction:
        return self._initial_direction

    @property
    def grid(self) -> Grid:
        return self._grid

    @property
    def food_count_to_complete(self) -> int:
        return self._food_count_to_complete

