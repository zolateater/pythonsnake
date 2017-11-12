from enum import Enum, unique

@unique
class CellType(Enum):
    WALL = '#'
    NONE = ' '

    @classmethod
    def exists(cls, cell: str) -> bool:
        enum_items = list(cls.__members__.values())
        enum_values = map(lambda e : e.value, enum_items)
        return cell in enum_values

@unique
class Direction(Enum):
    UP = 0
    LEFT = 1
    RIGHT = 2
    DOWN = 3

    def is_opposite(self, direction: 'Direction') -> bool:
        oppositePairs = [
            [self.UP.value, self.DOWN.value],
            [self.LEFT.value, self.RIGHT.value],
        ]

        currentPair = [self.value, direction.value]
        currentPair.sort()

        return currentPair in oppositePairs

@unique
class LevelStatus(Enum):
    GAME_OVER = 0
    VICTORY = 1