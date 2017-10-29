from typing import List
from .position import Position, Direction


class Snake():
    def __init__(self, initialPositions: List[Position], worldWidth: int, worldHeight: int):
        self.positions = initialPositions
        if len(initialPositions) == 0:
            raise ValueError('Positions can not be null')
        self._fail_if_positions_has_gaps(initialPositions)
        self.worldWidth = worldWidth
        self.worldHeight = worldHeight

    @property
    def head_position(self) -> Position:
        return self.positions[0]

    def move_in_direction(self, direction: Direction) -> None:
        self.prepend_head_in_direction(direction)
        self.positions.pop()

    def prepend_head_in_direction(self, direction: Direction) -> None:
        new_head_position = self.head_position.increment_in_direction(direction)

        # We need to give our snake ability to move through levels without walls
        new_head_position = new_head_position\
            .withX(new_head_position.x % self.worldWidth)\
            .withY(new_head_position.y % self.worldHeight)
        self.positions.insert(0, new_head_position)

    def _fail_if_positions_has_gaps(self, positions: List[Position]):
        previousPosition = positions[0]
        for position in positions[1:]:
            if previousPosition.distance(position) != 1:
                raise ValueError('Check snake positions. It has duplicate cells or gaps in it\'s body')
            previousPosition = position
