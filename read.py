import curses
from typing import List, Iterator
from itertools import repeat

GETCH_TIMEOUT = 0

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


def getEmptyCellArray(width, height) -> List[List[str]]:
    """
    Returns empty cell array for output
    :param width:
    :param height:
    :return:
    """
    table = []
    for i in range(0, height):
        table.append(['.'] * width)
    return table


try:
    playerPosition = [0, 0]
    width, height = 15, 15

    while True:

        cells = getEmptyCellArray(width, height)
        cells[playerPosition[0]][playerPosition[1]] = 'P'
        for line in cells:
            window.addstr("".join(line))
            window.addstr('\n')

        # height, width = window.getmaxyx()
        ch = window.getch()
        window.erase()

        if ch == ord('q'):
            break
        if ch == curses.KEY_UP:
            playerPosition[0] = playerPosition[0] - 1 if playerPosition[0] > 0 else playerPosition[0]
        if ch == curses.KEY_LEFT:
            playerPosition[1] = playerPosition[1] - 1 if playerPosition[1] > 0 else playerPosition[1]
        if ch == curses.KEY_RIGHT:
            playerPosition[1] = playerPosition[1] + 1 if playerPosition[1] < width - 1 else playerPosition[1]
        if ch == curses.KEY_DOWN:
            playerPosition[0] = playerPosition[0] + 1 if playerPosition[0] < height - 1 else playerPosition[0]

finally:
    # Undo our changes to the terminal
    curses.nocbreak()
    window.keypad(False)
    curses.echo()
    curses.endwin()

