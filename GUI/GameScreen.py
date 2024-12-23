from GUI.BaseScreen import BaseScreen
import pygame
from core.settings import GUI_SETTINGS
from model.Player import Player
from model.Tile import Tile


class GameScreen(BaseScreen):

    def init(self):
        self.player = Player(x=50, y=50, sprite="player_sprite.png")
        self.tiles = []
        self.load_map("level1.csv")
        self.add_event(self.handle_events)

    def load_map(self, map_file):
        with open(map_file, "r") as file:
            rows = file.readlines()

        tile_size = 50
        for row_index, row in enumerate(rows):
            for col_index, tile in enumerate(row.strip().split(",")):
                if tile == "1":
                    self.tiles.append(Tile(x=col_index * tile_size, y=row_index * tile_size, sprite="tile.png"))

    def render(self):
        self.screen.fill((135, 206, 235))  # Sky blue background
        for tile in self.tiles:
            tile.render(self.screen)
        self.player.render(self.screen)

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.player.move(0, -10)
            elif event.key == pygame.K_s:
                self.player.move(0, 10)
            elif event.key == pygame.K_a:
                self.player.move(-10, 0)
            elif event.key == pygame.K_d:
                self.player.move(10, 0)
