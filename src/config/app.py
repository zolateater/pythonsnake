from ..game.difficulty import Difficulty
from typing import Optional, Any
from logging import Logger


class App():
    Logger = None # type: Optional[Logger]
    CursesWindow = None # type: Optional[Any]
    CurrentDifficulty = None # type: Optional[Difficulty]
