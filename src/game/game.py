from .enums import Direction, CellType
from .grid import Grid
from typing import List
from .position import Position
from .snake import Snake

# TODO: Add SRP?
class Game():
    def __init__(self, window, grid: Grid, tick: float, snake: Snake, initialDirection: Direction):
        self.window = window
        self.grid = grid
        self.tick = tick
        self.snake = snake
        self.direction = initialDirection

    def render_frame(self) -> None:
        self.window.erase()
        for snake_position in self.snake.positions:
            self.grid.setCell(snake_position, CellType.SNAKE.value)

        for line in self.grid.cells:
            self.window.addstr("".join(line))
            self.window.addstr('\n')

    def move_snake(self) -> None:
        for snake_position in self.snake.positions:
            self.grid.setCell(snake_position, CellType.NONE.value)

        self.snake.move_in_direction(self.direction)