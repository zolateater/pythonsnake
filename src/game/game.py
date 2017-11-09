from src.game.renderer import Renderer
from .enums import Direction, CellType
from .grid import Grid
from .position import Position
from .snake import Snake
from random import randint

# TODO: Add SRP?
class Game():
    def __init__(self, renderer: Renderer, grid: Grid, tick: float, snake: Snake, initialDirection: Direction):
        self.renderer = renderer
        self.grid = grid
        self.tick = tick
        self.snake = snake
        self._direction = initialDirection
        self._last_used_direction = initialDirection
        self._is_game_over = False
        self.food_position = self.get_random_free_position()
        self.crash_position = None

    @property
    def direction(self) -> Direction:
        return self._direction

    @direction.setter
    def direction(self, direction: Direction) -> None:
        if not self._last_used_direction.isOpposite(direction):
            self._direction = direction

    def is_game_over(self) -> bool:
        return self._is_game_over

    def render_frame(self) -> None:
        self.renderer.render_level(self.snake, self.grid, self.food_position, self.crash_position)

    def get_random_free_position(self) -> Position:
        position_is_free = False
        position = None

        while not position_is_free:
            position = self._get_random_position_in_grid()
            position_free_from_snake = position not in self.snake.positions
            position_is_free = self.grid.getCell(position) == CellType.NONE.value and position_free_from_snake

        return position

    def _get_random_position_in_grid(self) -> Position:
        return Position(randint(0, self.grid.width - 1), randint(0, self.grid.height - 1))

    def make_game_turn(self) -> None:
        self.snake.prepend_head_at_direction(self.direction)
        self._last_used_direction = self.direction
        cell_value = self.grid.getCell(self.snake.head_position)

        if self.snake.head_position == self.food_position:
            self.food_position = self.get_random_free_position()
        elif cell_value == CellType.WALL.value or self.snake.has_self_interceptions():
            self._is_game_over = True
            self.crash_position = self.snake.head_position
        else:
            self.snake.pop_tail()