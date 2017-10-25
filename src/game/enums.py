from enum import Enum, unique

@unique
class CellType(Enum):
    SNAKE = '#'
    WALL = '$'
    NONE = ' '
    FOOD = '!'

    @classmethod
    def cellTypeExists(cls, cell: str) -> bool:
        enum_items = list(cls.__members__.values())
        enum_values = map(lambda e : e.value, enum_items)
        return cell in enum_values

@unique
class Direction(Enum):
    UP = 0
    LEFT = 1
    RIGHT = 2
    DOWN = 3