

from unittest import TestCase
from src.game.snake import Position, Snake, Direction


class TestPosition(TestCase):

    BIG_WIDTH = 1000
    BIG_HEIGHT = 1000

    def test_moves_in_direction(self):
        snake = Snake([
            Position(1, 2),
            Position(1, 1),
            Position(1, 0)
        ], self.BIG_WIDTH, self.BIG_HEIGHT)
        snake.move_in_direction(Direction.DOWN)

        assert snake.positions[0] == Position(1, 3)
        assert snake.positions[1] == Position(1, 2)
        assert snake.positions[2] == Position(1, 1)
