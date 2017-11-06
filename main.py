#!/usr/bin/env python3
import curses
from logging import FileHandler, Formatter, getLogger, DEBUG
from time import time
# TODO: fix __init__ of game package
from src.game.grid import Grid
from src.game.game import Game, Direction, Position, Snake


# Logging facilities
# TODO: move to some application class
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

snake = Snake([Position(0, 0), Position(0, 1), Position(0, 2), Position(0, 3)], grid.width, grid.height)
game = Game(renderer, grid, 0.2, snake, Direction.DOWN)


try:
    lastTickTime = time()
    while True:
        # TODO: add checks for rendering
        ch = window.getch()

        if ch == ord('q'):
            break
        if ch == curses.KEY_UP:
            game.direction = Direction.UP
        if ch == curses.KEY_LEFT:
            game.direction = Direction.LEFT
        if ch == curses.KEY_RIGHT:
            game.direction = Direction.RIGHT
        if ch == curses.KEY_DOWN:
            game.direction = Direction.DOWN


        currentTickTime = time()
        if currentTickTime - lastTickTime >= game.tick:
            lastTickTime = currentTickTime
            game.make_game_turn()
            game.render_frame()
except Exception as e:
    logger.fatal(str(e))
    raise e
finally:
    # Undo our changes to the terminal
    curses.nocbreak()
    window.keypad(False)
    curses.echo()
    curses.endwin()

