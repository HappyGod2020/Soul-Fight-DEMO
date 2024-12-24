from GUI.BaseScreen import BaseScreen

class ManagerScreen:
    screen: BaseScreen

    def __init__(self, main_game):
        self.main_game = main_game
        self.screen = None  # Изначально экран не установлен

    def select_screen(self, screen_class):
        self.screen = screen_class(self)
