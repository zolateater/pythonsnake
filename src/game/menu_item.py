class MenuItem():

    MAIN_MENU_CONTINUE = 1
    MAIN_MENU_NEW_GAME = 2
    MAIN_MENU_HOW_TO_PLAY = 3
    MAIN_MENU_DIFFICULTY = 4
    MAIN_MENU_QUIT = 5

    MENU_BACK = 10
    DIFFICULTY = 20

    # TODO: rename item_id to item_type
    def __init__(self, item_id: int, text: str):
        self.item_id = item_id
        self.text = text
