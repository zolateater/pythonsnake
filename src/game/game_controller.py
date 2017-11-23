import curses
from typing import Any
from typing import Optional
from .enums import ControllerEvent
from .abstract_controller import AbstractController


class GameController(AbstractController):
    def __init__(self, window: Any):
        self.window = window

    def read_action(self) -> Optional[ControllerEvent]:
        key_code = self.window.getch()  # type: int

        if self.key_code_equals_to_char(key_code, 'q'):
            return ControllerEvent.GAME_QUIT
        if self.key_code_equals_to_char(key_code, 'm'):
            return ControllerEvent.GAME_MENU
        if key_code == curses.KEY_UP:
            return ControllerEvent.GAME_UP
        if key_code == curses.KEY_DOWN:
            return ControllerEvent.GAME_DOWN
        if key_code == curses.KEY_LEFT:
            return ControllerEvent.GAME_LEFT
        if key_code == curses.KEY_RIGHT:
            return ControllerEvent.GAME_RIGHT

        return None