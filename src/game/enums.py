from enum import Enum, unique

@unique
class CellType(Enum):
    WALL = '#'
    NONE = ' '

    @classmethod
    def exists(cls, cell: str) -> bool:
        """
        Defines if string representation of CellType exists
        :param str cell:
        :return:
        """
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

@unique
class ControllerEvent(Enum):
    """
    All in-game input events
    """
    MENU_EXIT = 'MENU_EXIT'
    MENU_CHOOSE = 'MENU_CHOOSE'
    MENU_UP = 'MENU_UP'
    MENU_DOWN = 'MENU_DOWN'

    GAME_QUIT = 'GAME_QUIT'
    GAME_MENU = 'GAME_MENU'
    GAME_UP = 'GAME_UP'
    GAME_DOWN = 'GAME_DOWN'
    GAME_LEFT = 'GAME_LEFT'
    GAME_RIGHT = 'GAME_RIGHT'

@unique
class LevelOutcome(Enum):
    """
    All possible outcomes of a level walkthrough
    """
    GAME_OVER = 1
    LEVEL_COMPLETED = 2