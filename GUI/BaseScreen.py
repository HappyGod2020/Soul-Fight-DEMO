class BaseScreen:
    def __init__(self, manager_screen):
        self.manager_screen = manager_screen

        self.screen = self.manager_screen.main_game.screen

        self.init()

    def init(self):
        pass

    def render(self):
        pass

    def add_event(self, func):
        self.manager_screen.main_game.event_array.append(func)