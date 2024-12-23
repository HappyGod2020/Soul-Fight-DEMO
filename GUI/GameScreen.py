from GUI.BaseScreen import BaseScreen
from model.Player import Player
from core.settings import GUI_SETTINGS
import pygame


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, sprite_path="tile.png"):
        super().__init__()
        self.image = pygame.image.load(sprite_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))




class GameScreen(BaseScreen):

    def init(self):
        self.player = Player(50, GUI_SETTINGS.HEIGHT - 100, 50, 50, "player_sprite.png")
        self.platforms = pygame.sprite.Group()
        self.create_map()
        self.add_event(self.handle_input)

    def create_map(self):
        platform_positions = [
            (0, GUI_SETTINGS.HEIGHT - 50, 100, 20),  # Нижний блок
            (200, GUI_SETTINGS.HEIGHT - 150, 100, 20),  # Средний блок
            (400, GUI_SETTINGS.HEIGHT - 250, 100, 20),  # Верхний блок
        ]
        for x, y, w, h in platform_positions:
            platform = Platform(x, y, w, h, "tile.png")
            self.platforms.add(platform)

    def render(self):
        self.screen.fill((135, 206, 250))  # Светло-голубой фон
        self.platforms.draw(self.screen)
        self.screen.blit(self.player.image, self.player.rect)
        self.player.update(self.platforms)

    def handle_input(self, e):
        if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
            self.player.jump()
