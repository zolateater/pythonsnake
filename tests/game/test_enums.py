from src.game.enums import Direction
from unittest import TestCase


class TestDirection(TestCase):

    def test_knows_its_opposite(self):
        assert Direction.UP.isOpposite(Direction.DOWN)
        assert Direction.DOWN.isOpposite(Direction.UP)
        assert Direction.LEFT.isOpposite(Direction.RIGHT)
        assert Direction.RIGHT.isOpposite(Direction.LEFT)

        assert not Direction.RIGHT.isOpposite(Direction.UP)
        assert not Direction.RIGHT.isOpposite(Direction.DOWN)
        assert not Direction.RIGHT.isOpposite(Direction.RIGHT)

        assert not Direction.LEFT.isOpposite(Direction.UP)
        assert not Direction.LEFT.isOpposite(Direction.LEFT)
        assert not Direction.LEFT.isOpposite(Direction.DOWN)

        assert not Direction.UP.isOpposite(Direction.UP)
        assert not Direction.UP.isOpposite(Direction.LEFT)
        assert not Direction.UP.isOpposite(Direction.RIGHT)

        assert not Direction.DOWN.isOpposite(Direction.DOWN)
        assert not Direction.DOWN.isOpposite(Direction.LEFT)
        assert not Direction.DOWN.isOpposite(Direction.RIGHT)
