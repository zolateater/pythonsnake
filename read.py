#!/usr/bin/env python3
import sys
import termios
import os
import time
import selectors
from itertools import repeat
from typing import List, Tuple


def getTerminalSize() -> Tuple[int, int]:
    width, height = os.popen('stty size').read().split()
    return (int(width), int(height))


def getCells() -> List[List[str]]:
    rows_count = 10
    columns_count = 20
    row = list(repeat('#', columns_count))
    cells = list(repeat(row, rows_count))
    return cells


def printCells(cells: List[List[str]]) -> None:
    for row in cells:
        for cell in row:
            sys.stdout.write(cell)
        sys.stdout.write('\n')


def getch() -> str:
    return sys.stdin.read(3)

def clearScreen() -> None:
    os.system('clear')

printCells(getCells())

file_descriptor = sys.stdin.fileno()
old_terminal_settings = termios.tcgetattr(file_descriptor)
new_terminal_settings = termios.tcgetattr(file_descriptor)
new_terminal_settings[3] = new_terminal_settings[3] & ~termios.ICANON & ~termios.ECHO  # lflags

selector = selectors.DefaultSelector()
selector.register(sys.stdin.fileno(), selectors.EVENT_READ)


try:
    termios.tcsetattr(file_descriptor, termios.TCSANOW, new_terminal_settings)
    while True:
        # TODO: detect three key presses in a row
        events = selector.select(1)
        print(events)
        for selectorKey, event in events:
            print(selectorKey)
            data = sys.stdin.read(1)
            print(len(data))
        time.sleep(1)
except KeyboardInterrupt:
    print("Ctrl-C pressed")
finally:
    termios.tcsetattr(file_descriptor, termios.TCSANOW, old_terminal_settings)
