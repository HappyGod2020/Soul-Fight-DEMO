class ManagerScreen:
    def __init__(self, main_game):
        self.main_game = main_game  # Ссылка на объект Game
        self.current_screen = None  # Текущий экран

    def select_screen(self, screen_class):
        self.current_screen = screen_class(self)
