from .enums import Direction, CellType
from .grid import Grid
from typing import List
from .utils import Position

# SRP ?
class Game():
    def __init__(self, window, grid: Grid, tick: float, playerPosition: Position, direction: Direction):
        self.window = window
        self.grid = grid
        self.tick = tick
        self.playerPosition = playerPosition
        self.direction = direction

    def renderFrame(self) -> None:
        self.window.erase()
        for line in self.grid.cells:
            self.window.addstr("".join(line))
            self.window.addstr('\n')

    def movePlayer(self) -> None:
        width, height = self.grid.width, self.grid.height
        if self.direction == Direction.UP:
            if self.playerPosition.y > 0:
                newPosition = self.playerPosition.withY(self.playerPosition.y)
                self.grid.swap(self.playerPosition, newPosition)
                self.playerPosition = new_position
        if self.direction == Direction.LEFT:
            self.playerPosition[1] = self.playerPosition[1] - 1 if self.playerPosition[1] > 0 else self.playerPosition[1]
        if self.direction == Direction.RIGHT:
            self.playerPosition[1] = self.playerPosition[1] + 1 if self.playerPosition[1] < width - 1 else self.playerPosition[1]
        if self.direction == Direction.DOWN:
            # TODO: make position class?
            self.grid.cells[self.playerPosition[0]][self.playerPosition[1]] = CellType.NONE.value
            self.playerPosition[0] = self.playerPosition[0] + 1 if self.playerPosition[0] < height - 1 else self.playerPosition[0]
            self.grid.cells[self.playerPosition[0]][self.playerPosition[1]] = CellType.SNAKE.value
