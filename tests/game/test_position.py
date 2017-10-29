from unittest import TestCase, main
from src.game.position import Position
from src.game.position import Direction

class TestPosition(TestCase):

    def test_returns_new_instance_on_modify(self):
        pos1 = Position(0, 0)
        pos2 = pos1.withX(9)
        pos3 = pos2.withY(2)

        assert (pos1.x, pos1.y) == (0, 0)
        assert (pos2.x, pos2.y) == (9, 0)
        assert (pos3.x, pos3.y) == (9, 2)

    def test_follows_direction(self):
        initialPos = Position(0, 0)

        posUp = initialPos.increment_in_direction(Direction.UP)
        posDown = initialPos.increment_in_direction(Direction.DOWN)
        posLeft = initialPos.increment_in_direction(Direction.LEFT)
        posRight = initialPos.increment_in_direction(Direction.RIGHT)

        assert (posUp.x, posUp.y) == (0, -1)
        assert (posDown.x, posDown.y) == (0, 1)
        assert (posLeft.x, posLeft.y) == (-1, 0)
        assert (posRight.x, posRight.y) == (1, 0)