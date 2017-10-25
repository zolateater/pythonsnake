#!/usr/bin/env python3
import curses
from logging import FileHandler, Formatter, getLogger, DEBUG
from time import time
# TODO: fix __init__ of game package
from src.game.grid import Grid
from src.game.game import Game, Direction


# Logging facilities
# TODO: move to some application class
logger = getLogger('default')
logger.setLevel(DEBUG)

logHandler = FileHandler('./logs/default.log')
logHandler.setLevel(DEBUG)

formatter = Formatter('[%(asctime)s] [%(name)s] [%(levelname)s]: %(message)s')
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)

# Creating app window
window = curses.initscr()

# Usually curses applications turn off automatic echoing of keys to the screen,
# in order to be able to read keys and only display them under certain circumstances.
# This requires calling the noecho() function.
curses.noecho()

# Applications will also commonly need to react to keys instantly,
# without requiring the Enter key to be pressed;
# this is called cbreak mode, as opposed to the usual buffered input mode.
curses.cbreak()

# Terminals usually return special keys, such as the cursor keys or navigation keys such as Page Up and Home,
# as a multibyte escape sequence.
# While you could write your application to expect such sequences and process them accordingly,
# curses can do it for you, returning a special value such as curses.KEY_LEFT.
# To get curses to do the job, you’ll have to enable keypad mode.
window.keypad(True)
window.nodelay(1)

playerPosition = [0, 0]

try:
    grid = Grid([
        ['#', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' '],
    ])
    game = Game(window, grid, 1, playerPosition, Direction.DOWN)
    # TODO: add separated controller and
    lastTickTime = time()
    while True:


        # TODO: add checks for rendering
        # height, width = window.getmaxyx()
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
            game.movePlayer()
            game.renderFrame()
except Exception as e:
    logger.fatal(str(e))
    raise e
finally:
    # Undo our changes to the terminal
    curses.nocbreak()
    window.keypad(False)
    curses.echo()
    curses.endwin()

