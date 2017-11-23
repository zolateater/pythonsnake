from ..game.get_level_list import get_level_list
from ..game.level import Level
from ..game.difficulty import Difficulty, get_all_difficulties
from typing import Optional, Any, List
from logging import Logger


class App():
    Logger = None # type: Optional[Logger]
    CursesWindow = None # type: Optional[Any]
    CurrentDifficulty = None # type: Optional[Difficulty]
    AllDifficulties = [] # type: List[Difficulty]
    LastLevelIndex = None # type: Optional[int]
    LevelList = [] # type: List[Level]


def init_app() -> None:
    App.LevelList = get_level_list()
    App.AllDifficulties = get_all_difficulties()
    App.CurrentDifficulty = App.AllDifficulties[1] # active