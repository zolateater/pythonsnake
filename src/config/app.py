import curses
from ..game.get_level_list import get_level_list
from ..game.level import Level
from ..game.difficulty import Difficulty, get_all_difficulties
from typing import Optional, Any, List
from logging import Logger, getLogger, DEBUG, FileHandler, Formatter


class App():
    # TODO: make singleton
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
    App.CursesWindow = get_curses_window()
    App.Logger = get_logger()


def get_logger() -> Logger:
    logger = getLogger('default')
    logger.setLevel(DEBUG)

    logHandler = FileHandler('./logs/default.log')
    logHandler.setLevel(DEBUG)

    formatter = Formatter('[%(asctime)s] [%(name)s] [%(levelname)s]: %(message)s')
    logHandler.setFormatter(formatter)
    logger.addHandler(logHandler)

    return logger

# TODO: Add typehint for curses window
def get_curses_window() -> Any:
    window = curses.initscr()

    # Usually curses applications turn off automatic echoing of keys to the screen,
    # in order to be able to read keys and only display them under certain circumstances.
    # This requires calling the noecho() function.
    curses.noecho()

    # Applications will also commonly need to react to keys instantly,
    # without requiring the Enter key to be pressed;
    # this is called cbreak mode, as opposed to the usual buffered input mode.
    curses.cbreak()

    # To use color, you must call the start_color() function soon after calling initscr(),
    # to initialize the default color set
    # Once that’s done, the has_colors() function
    # returns TRUE if the terminal in use can actually display color.
    curses.start_color()
    curses.use_default_colors()

    # Terminals usually return special keys, such as the cursor keys or navigation keys such as Page Up and Home,
    # as a multibyte escape sequence.
    # While you could write your application to expect such sequences and process them accordingly,
    # curses can do it for you, returning a special value such as curses.KEY_LEFT.
    # To get curses to do the job, you’ll have to enable keypad mode.
    window.keypad(True)
    window.nodelay(1)

    # If your application doesn’t need a blinking cursor at all, you can call curs_set(False) to make it invisible.
    curses.curs_set(False)

    return window


def shutdown_curses(window: Any):
    # Undo our changes to the terminal
    curses.nocbreak()
    window.keypad(False)
    curses.echo()
    curses.endwin()