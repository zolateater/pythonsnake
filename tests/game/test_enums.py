from src.game.enums import Direction
from unittest import TestCase


class TestDirection(TestCase):

    def test_knows_its_opposite(self):
        assert Direction.UP.is_opposite(Direction.DOWN)
        assert Direction.DOWN.is_opposite(Direction.UP)
        assert Direction.LEFT.is_opposite(Direction.RIGHT)
        assert Direction.RIGHT.is_opposite(Direction.LEFT)

        assert not Direction.RIGHT.is_opposite(Direction.UP)
        assert not Direction.RIGHT.is_opposite(Direction.DOWN)
        assert not Direction.RIGHT.is_opposite(Direction.RIGHT)

        assert not Direction.LEFT.is_opposite(Direction.UP)
        assert not Direction.LEFT.is_opposite(Direction.LEFT)
        assert not Direction.LEFT.is_opposite(Direction.DOWN)

        assert not Direction.UP.is_opposite(Direction.UP)
        assert not Direction.UP.is_opposite(Direction.LEFT)
        assert not Direction.UP.is_opposite(Direction.RIGHT)

        assert not Direction.DOWN.is_opposite(Direction.DOWN)
        assert not Direction.DOWN.is_opposite(Direction.LEFT)
        assert not Direction.DOWN.is_opposite(Direction.RIGHT)
