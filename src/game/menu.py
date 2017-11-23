from typing import List
from .difficulty import Difficulty
from .menu_item import MenuItem


class Menu():
    def __init__(self, items: List[MenuItem], active_index: int):
        self.items = items
        self._fail_if_active_is_not_in_range(active_index)
        self._active_index = active_index

    def set_active_next(self) -> None:
        self._active_index = (self._active_index + 1) % len(self.items)

    def set_active_prev(self) -> None:
        if self._active_index == 0:
            self._active_index = len(self.items) - 1
        else:
            self._active_index = self._active_index - 1

    @property
    def active_item(self) -> MenuItem:
        return self.items[self._active_index]\

    @property
    def active_index(self) -> int:
        return self._active_index

    def _fail_if_active_is_not_in_range(self, active_index: int):
        if active_index < 0 or active_index >= len(self.items):
            raise ValueError('Active item of the menu should not be one of the items')

    @classmethod
    def get_main_menu(self) -> 'Menu':
        return Menu([
            MenuItem(MenuItem.MAIN_MENU_NEW_GAME, "New Game"),
            MenuItem(MenuItem.MAIN_MENU_DIFFICULTY, "Difficulty"),
            MenuItem(MenuItem.MAIN_MENU_HOW_TO_PLAY, "How To Play"),
            MenuItem(MenuItem.MAIN_MENU_QUIT, "Quit Game"),
        ], 0)