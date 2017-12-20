import curses
from typing import Any
from typing import Optional
from .enums import ControllerEvent
from .abstract_controller import AbstractController


class MenuController(AbstractController):
    def __init__(self, window: Any):
        self.window = window

    def read_action(self) -> Optional[ControllerEvent]:
        key_code = self.window.getch() # type: int

        if self.key_code_equals_to_char(key_code, 'q'):
            return ControllerEvent.MENU_EXIT
        if key_code == curses.KEY_UP:
            return ControllerEvent.MENU_UP
        if key_code == curses.KEY_DOWN:
            return ControllerEvent.MENU_DOWN
        if key_code == curses.KEY_ENTER or self.key_code_equals_to_char(key_code, '\n'):
            return ControllerEvent.MENU_CHOOSE

        return None