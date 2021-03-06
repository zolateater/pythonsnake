from typing import List
from ..config.app import App
from .menu_item import MenuItem
from .enums import ControllerEvent, Direction
from .menu import Menu
from .abstract_controller import AbstractController
from time import time, sleep
from .level import Level
from .levelrunner import Level, LevelRunner
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
        if active_item.item_id == MenuItem.MAIN_MENU_NEW_GAME:
            self.run_new_game()
            self._renderer.render_menu(self.active_menu)

    def get_menu_from_difficulties(self) -> Menu:
        active_difficulty = App.AllDifficulties.index(App.CurrentDifficulty)
        menu_items = map(lambda difficulty: MenuItem(MenuItem.DIFFICULTY, difficulty.name), App.AllDifficulties)
        return Menu(list(menu_items), active_difficulty)

    def run_new_game(self):
        game_score = 0
        for level in App.LevelList:
            level_runner = LevelRunner(self._renderer, level, App.CurrentDifficulty, game_score)
            last_tick_time = time()
            while not level_runner.is_game_over() and not level_runner.is_level_completed():
                controller_event = self.game_controller.read_action()
                level_runner.render_frame()

                # Controller events
                if controller_event == ControllerEvent.GAME_QUIT:
                    self.should_quit = True
                    return
                if controller_event == ControllerEvent.GAME_MENU:
                    # TODO: add save game
                    return
                if controller_event == ControllerEvent.GAME_DOWN:
                    level_runner.set_new_direction(Direction.DOWN)
                if controller_event == ControllerEvent.GAME_UP:
                    level_runner.set_new_direction(Direction.UP)
                if controller_event == ControllerEvent.GAME_LEFT:
                    level_runner.set_new_direction(Direction.LEFT)
                if controller_event == ControllerEvent.GAME_RIGHT:
                    level_runner.set_new_direction(Direction.RIGHT)

                current_tick_time = time()
                if current_tick_time - last_tick_time >= level_runner.difficulty.tick:
                    last_tick_time = current_tick_time
                    level_runner.make_game_turn()

            # Game over or level completed
            if level_runner.is_game_over():
                level_runner.render_frame()
                self._renderer.render_defeat()
                sleep(1)
                return

            if level_runner.is_level_completed():
                level_runner.render_frame()
                self._renderer.render_victory()
                sleep(1)
                game_score = level_runner.get_total_score()

        # All levels are completed!
        self._renderer.render_total_victory()
        sleep(1)
