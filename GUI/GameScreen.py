from .BaseScreen import BaseScreen
from model.Player import Player


class GameScreen(BaseScreen):

    def init(self):
        self.player = Player(sprite="")

    def render(self):
        pass