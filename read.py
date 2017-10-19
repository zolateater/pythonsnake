#!/usr/bin/env python3
import sys, termios, os
from itertools import repeat
from typing import List

width, height = os.popen('stty size').read().split()
print(width, height)

file_descriptor = sys.stdin.fileno()
old_terminal_settings = termios.tcgetattr(file_descriptor)
new_terminal_settings = termios.tcgetattr(file_descriptor)
new_terminal_settings[3] = new_terminal_settings[3] & ~termios.ICANON & ~termios.ECHO# lflags 
termios.tcsetattr(file_descriptor, termios.TCSANOW, new_terminal_settings)

def getCells() -> List[List[str]]:
	rows_count = 10
	columns_count = 10
	cells = list(repeat(list(repeat('#', rows_count)), columns_count))
	return cells

def printCells(cells: List[List[str]]):
	for row in cells:
		for cell in row:
			sys.stdout.write(cell)
		sys.stdout.write('\n')

def getch() -> str:
	return sys.stdin.read(3)

printCells(getCells())



#for i in range(10):
#    a = getch()
#    print(len(a), a)
# os.system('clear')
# print("i: {}, symbol: {}, symbol code: {}".format(i, a, ord(a)))
# print(a)

try:
	termios.tcsetattr(file_descriptor, termios.TCSANOW, old_terminal_settings)
	a = getch()
	print(len(a), a)
except KeyboardInterrupt:
	print("Ctrl-C pressed")
finally:
	termios.tcsetattr(file_descriptor, termios.TCSANOW, old_terminal_settings)
