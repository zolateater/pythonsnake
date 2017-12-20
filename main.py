#!/usr/bin/env python3
from src.config.app import init_app, App, shutdown_curses
from src.game.game_controller import GameController
from src.game.game_runner import GameRunner
from src.game.menu_controller import MenuController
from src.game.renderer import Renderer

try:

    init_app()
    game_runner = GameRunner(
        Renderer(App.CursesWindow),
        App.LevelList,
        MenuController(App.CursesWindow),
        GameController(App.CursesWindow)
    )
    game_runner.start()
except Exception as e:
    App.Logger.fatal(str(e))
    raise e
finally:
    shutdown_curses(App.CursesWindow)


