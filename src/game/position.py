from src.game.enums import Direction

class Position():
    def __init__(self, x: int, y: int):
        self._x = x
        self._y = y
    
    @property 
    def x(self) -> int:
        return self._x

    def withX(self, x: int) -> 'Position':
        return Position(x, self._y)
    
    @property
    def y(self) -> int:
        return self._y

    def distance(self, position: 'Position') -> int:
        return abs(self._x - position._x) + abs(self._y - position._y)

    def withY(self, y: int) -> 'Position':
        """
        Creates new direction
        :param y:
        :return:
        """
        return Position(self._x, y)

    def increment_in_direction(self, direction: Direction) -> 'Position':
        """
        Creates new position by moving at 1 cell at passed direction.
        :param Direction direction:
        :return:
        """
        if direction.value == Direction.UP.value:
            return self.withY(self._y - 1)
        if direction.value == Direction.DOWN.value:
            return self.withY(self._y + 1)
        if direction.value == Direction.LEFT.value:
            return self.withX(self._x - 1)
        if direction.value == Direction.RIGHT.value:
            return self.withX(self._x + 1)

        raise ValueError('Unexpected direction')