
from GUI.BaseScreen import BaseScreen


class ManagerScreen:
    screen: BaseScreen

    def __init__(self, main_game):
        self.main_game = main_game

    def select_screen(self, screen):
        self.screen = screen(self)
