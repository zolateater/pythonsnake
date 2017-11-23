from typing import Any, Optional
from .enums import CellType
from .grid import Grid
from .menu import Menu
from .position import Position
from .snake import Snake
import curses


"""
For window methods please look at the
https://docs.python.org/3/library/curses.html#window-objects
"""
class Renderer():
    SYMBOL_WALL = "█"
    SYMBOL_BORDER = "░"
    SYMBOL_SNAKE_BODY = '#'
    SYMBOL_SNAKE_HEAD = '#'
    SYMBOL_CRASH_SITE = '█'
    SYMBOL_FOOD = 'O'

    COLOR_PAIR_HEAD_SNAKE = 1
    COLOR_PAIR_FOOD = 2
    COLOR_PAIR_CRASH_SITE = 3
    COLOR_PAIR_MENU_ITEM = 4
    COLOR_PAIR_MENU_ITEM_ACTIVE = 5

    OFFSET_FOR_BORDER = 2

    def __init__(self, window: Any):
        self.window = window
        self._init_curses_colors()

    def _init_curses_colors(self):
        curses.init_pair(self.COLOR_PAIR_HEAD_SNAKE, curses.COLOR_BLUE, -1)
        curses.init_pair(self.COLOR_PAIR_FOOD, curses.COLOR_GREEN, -1)
        curses.init_pair(self.COLOR_PAIR_CRASH_SITE, curses.COLOR_RED, -1)
        curses.init_pair(self.COLOR_PAIR_MENU_ITEM, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(self.COLOR_PAIR_MENU_ITEM_ACTIVE, curses.COLOR_BLACK, curses.COLOR_WHITE)

    def render_level(self, snake: Snake, grid: Grid, food_position: Position, crash_position: Optional[Position]):
        self.window.erase()
        subwindow = self._get_grid_subwindow(grid)

        self._draw_borders(subwindow, grid)
        self._draw_grid(subwindow, grid)
        self._draw_snake(subwindow, snake)
        self._draw_food(subwindow, food_position)
        if crash_position:
            self._draw_crash_position(subwindow, crash_position)
        # self._draw_ui(subwindow, 123)

        self.window.refresh()

    def render_menu(self, menu: Menu) -> None:
        self.window.erase()

        menu_length = len(menu.items)
        menu_window_height = menu_length + (menu_length - 1)
        max_item_length = max(map(lambda x: len(x.text), menu.items))
        menu_window_width = max_item_length + self.OFFSET_FOR_BORDER + 5
        menu_subwindow = self._get_subwindow_in_center(menu_window_width, menu_window_height)

        offset = 0
        for i, item in enumerate(menu.items):
            length_diff = menu_window_width - len(item.text)
            rjust_length = menu_window_width - (length_diff // 2)
            space_padded_text = item.text.rjust(rjust_length, ' ').ljust(menu_window_width, ' ')
            color = self.COLOR_PAIR_MENU_ITEM_ACTIVE if i == menu._active_index else self.COLOR_PAIR_MENU_ITEM
            self._draw_line_at_with_trimming(menu_subwindow, space_padded_text, Position(0, offset), color)
            offset += 2

        self.window.refresh()

    def _get_grid_subwindow(self, grid: Grid) -> Any:
        grid_width_bordered = grid.width + self.OFFSET_FOR_BORDER
        grid_height_bordered = grid.height + self.OFFSET_FOR_BORDER

        return self._get_subwindow_in_center(grid_width_bordered, grid_height_bordered)

    def _get_subwindow_in_center(self, width: int, height: int) -> Any:
        window_height, window_width = self.window.getmaxyx()

        offset_x, offset_y = 0, 0
        width_sub_window, height_sub_window = window_width, window_height

        if window_width > width:
            offset_x = (window_width - width) // 2
            width_sub_window = width

        if window_height > height:
            offset_y = (window_height - height) // 2
            height_sub_window = height

        return self.window.subwin(height_sub_window, width_sub_window, offset_y, offset_x)

    def _draw_line_at_with_trimming(self, window, line: str, pos: Position, color_pair_number: Optional[int] = None):
        height, width = window.getmaxyx()
        if height <= pos.y or width <= pos.x:
            return

        line_trimmed = line[:width - pos.x]
        if not line_trimmed:
            return

        arguments = [pos.y, pos.x, line_trimmed]
        if color_pair_number is not None:
            arguments.append(curses.color_pair(color_pair_number))

        # There is a bug is curses implementation.
        # Last line should NOT be drawn with addstr method.
        # https://bugs.python.org/msg218985
        if height - 1 == pos.y:
            window.insstr(*arguments)
        else:
            window.addstr(*arguments)

    def _draw_borders(self, subwindow, grid: Grid):
        border_line_length = grid.width + self.OFFSET_FOR_BORDER
        border_line = self.SYMBOL_BORDER * border_line_length

        for i in range(0, grid.height + self.OFFSET_FOR_BORDER):
            self._draw_line_at_with_trimming(subwindow, border_line, Position(0, i))

    def _draw_grid(self, subwindow, grid: Grid):
        for i in range(0, grid.height):
            grid_line = "".join(grid.cells[i]).replace(CellType.WALL.value, self.SYMBOL_WALL)
            self._draw_line_at_with_trimming(subwindow, grid_line, self._to_level_coordinates(Position(0, i)))

    def _draw_snake(self, subwindow, snake: Snake):
        self._draw_line_at_with_trimming(subwindow, self.SYMBOL_SNAKE_HEAD, self._to_level_coordinates(snake.head_position), self.COLOR_PAIR_HEAD_SNAKE)
        for position in snake.positions[1:]:
            self._draw_line_at_with_trimming(subwindow, self.SYMBOL_SNAKE_BODY, self._to_level_coordinates(position))

    def _draw_food(self, subwindow, food_position: Position):
        self._draw_line_at_with_trimming(subwindow, self.SYMBOL_FOOD, self._to_level_coordinates(food_position), self.COLOR_PAIR_FOOD)

    def _draw_crash_position(self, subwindow, crash_position: Position):
        self._draw_line_at_with_trimming(subwindow, self.SYMBOL_CRASH_SITE, self._to_level_coordinates(crash_position), self.COLOR_PAIR_CRASH_SITE)

    def _to_level_coordinates(self, position: Position) -> Position:
        return Position(position.x + 1, position.y + 1)

