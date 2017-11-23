from typing import List

from ..config.app import App
from .menu_item import MenuItem
from .enums import ControllerEvent
from .menu import Menu
from .abstract_controller import AbstractController
from .level import Level
from .levelrunner import Level
from .renderer import Renderer
from sys import exit


class GameRunner():
    def __init__(
        self,
        renderer: Renderer,
        levels: List[Level],
        gui_controller: AbstractController,
        game_controller: AbstractController
    ):
        self.game_controller = game_controller
        self.gui_controller = gui_controller
        self.levels = levels
        self._renderer = renderer
        self.main_menu = Menu.get_main_menu()
        self.active_menu = self.main_menu
        self.should_quit = False

    def start(self) -> None:
        # render menu
        # get active action
        # if action is move - rerender
        # if action is select - handle (selected menu item)
        self._renderer.render_menu(self.active_menu)
        while not self.should_quit:
            action = self.gui_controller.read_action()
            if action == ControllerEvent.MENU_EXIT:
                self.should_quit = True
            if action == ControllerEvent.MENU_DOWN:
                self.active_menu.set_active_next()
                self._renderer.render_menu(self.active_menu)
            if action == ControllerEvent.MENU_UP:
                self.active_menu.set_active_prev()
                self._renderer.render_menu(self.active_menu)
            if action == ControllerEvent.MENU_CHOOSE:
                self.handle_menu_item_choose(self.active_menu.active_item)

    def handle_menu_item_choose(self, active_item: MenuItem):
        # TODO: add how to play and records
        if active_item.item_id == MenuItem.MAIN_MENU_QUIT:
            self.should_quit = True
        if active_item.item_id == MenuItem.MAIN_MENU_DIFFICULTY:
            self.active_menu = self.get_menu_from_difficulties()
            self._renderer.render_menu(self.active_menu)
        if active_item.item_id == MenuItem.DIFFICULTY:
            App.CurrentDifficulty = App.AllDifficulties[self.active_menu.active_index]
            self.active_menu = self.main_menu
            self._renderer.render_menu(self.active_menu)

    def get_menu_from_difficulties(self) -> Menu:
        active_difficulty = App.AllDifficulties.index(App.CurrentDifficulty)
        menu_items = map(lambda difficulty: MenuItem(MenuItem.DIFFICULTY, difficulty.name), App.AllDifficulties)
        return Menu(list(menu_items), active_difficulty)