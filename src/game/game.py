from .enums import Direction, CellType
from .grid import Grid
from typing import List
from .position import Position
from .snake import Snake
from random import randint

# TODO: Add SRP?
class Game():
    def __init__(self, window, grid: Grid, tick: float, snake: Snake, initialDirection: Direction):
        self.window = window
        self.grid = grid
        self.tick = tick
        self.snake = snake
        self._direction = initialDirection
        self._is_game_over = False
        self.create_food_in_new_position()

    @property
    def direction(self) -> Direction:
        return self._direction

    @direction.setter
    def direction(self, direction: Direction) -> None:
        # TODO: add counter to check count of turns made in direction
        if not self._direction.isOpposite(direction):
            self._direction = direction

    def is_game_over(self) -> bool:
        return self._is_game_over

    def render_frame(self) -> None:
        self.window.erase()
        for snake_position in self.snake.positions:
            self.grid.setCell(snake_position, CellType.SNAKE.value)

        # TODO: add separate class for rendering
        # borders
        border_line_horizontal_upper = "_" * (self.grid.width + 2)
        border_line_horizontal_lower = "‾" * (self.grid.width + 2)
        border_brick_vertical = '|'

        self.window.addstr(border_line_horizontal_upper)
        self.window.addstr('\n')
        for row in self.grid.cells:
            line = border_brick_vertical + "".join(row) + border_brick_vertical
            self.window.addstr(line)
            self.window.addstr('\n')

        self.window.addstr(border_line_horizontal_lower)
        self.window.addstr('\n')


    def create_food_in_new_position(self) -> None:
        position_is_free = False
        position = None

        while not position_is_free:
            position = self._get_random_position_in_grid()
            position_free_from_snake = position not in self.snake.positions
            position_is_free = self.grid.getCell(position) == CellType.NONE.value and position_free_from_snake

        self.window.addstr("{} {}".format(position.x, position.y))
        self.grid.setCell(position, CellType.FOOD.value)

    def _get_random_position_in_grid(self) -> Position:
        return Position(randint(0, self.grid.width - 1), randint(0, self.grid.height - 1))

    def make_game_turn(self) -> None:
        for snake_position in self.snake.positions:
            self.grid.setCell(snake_position, CellType.NONE.value)

        self.snake.move_in_direction(self.direction)
        cell_value = self.grid.getCell(self.snake.head_position)

        if cell_value == CellType.FOOD.value:
            self.snake.prepend_head_in_direction(self._direction)
            self.grid.setCell(self.snake.head_position, CellType.NONE.value)
            self.create_food_in_new_position()
        elif cell_value == CellType.SNAKE.value:
            self._is_game_over = True
        elif cell_value == CellType.SNAKE.value:
            self._is_game_over = True


