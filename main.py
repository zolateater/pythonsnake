#!/usr/bin/env python3
import curses
from logging import FileHandler, Formatter, getLogger, DEBUG
from time import time, sleep
# TODO: fix __init__ of game package
from src.game.grid import Grid
from src.game.levelrunner import LevelRunner, Level, Direction, Position, Snake, Difficulty
from src.game.difficulty import get_all_difficulties


# Logging facilities
# TODO: move to some application class
from src.game.menu import Menu
from src.game.menu_item import MenuItem
from src.game.renderer import Renderer

logger = getLogger('default')
logger.setLevel(DEBUG)

logHandler = FileHandler('./logs/default.log')
logHandler.setLevel(DEBUG)

formatter = Formatter('[%(asctime)s] [%(name)s] [%(levelname)s]: %(message)s')
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)

# Creating app window
# TODO: Move curses config to separate place
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


renderer = Renderer(window)
playerPosition = Position(0, 0)
grid = Grid([
    ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#',],
    ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#',],
    ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#',],
    ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#',],
    ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#',],
    ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#',],
    ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#',],
    ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#',],
    ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#',],
    ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#',],
])
snake = Snake([Position(1, 3), Position(1, 2), Position(1, 1)], grid.width, grid.height)
level = Level(snake, grid, Direction.DOWN, 10)
level_runner = LevelRunner(renderer, level, get_all_difficulties()[3])


try:

    menu = Menu([MenuItem(1, "Continue"), MenuItem(2, "New Game"), MenuItem(3, "Quit Game")], 1)
    while True:
        renderer.render_menu(menu)
        sleep(1)

    # TODO: Move to game_runner
    lastTickTime = time()
    while not level_runner.is_game_over():
        ch = window.getch()
        level_runner.render_frame()
        if ch == ord('q'):
            break
        if ch == curses.KEY_UP:
            level_runner.direction = Direction.UP
        if ch == curses.KEY_LEFT:
            level_runner.direction = Direction.LEFT
        if ch == curses.KEY_RIGHT:
            level_runner.direction = Direction.RIGHT
        if ch == curses.KEY_DOWN:
            level_runner.direction = Direction.DOWN

        currentTickTime = time()
        if currentTickTime - lastTickTime >= level_runner.difficulty.tick:
            lastTickTime = currentTickTime
            level_runner.make_game_turn()
except Exception as e:
    logger.fatal(str(e))
    raise e
finally:
    level_runner.render_frame()
    sleep(1)
    # Undo our changes to the terminal
    curses.nocbreak()
    window.keypad(False)
    curses.echo()
    curses.endwin()

