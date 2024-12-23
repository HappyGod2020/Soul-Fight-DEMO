from GUI.BaseScreen import BaseScreen
from model.Player import Player
from core.settings import GUI_SETTINGS
import pygame
import csv


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
        self.load_map_from_csv("level1.csv")  # Загрузка карты
        self.add_event(self.handle_input)

    def load_map_from_csv(self, filepath):
        """Загрузка карты из CSV файла"""
        tile_size = 50  # Размер одной плитки
        with open(filepath, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for y, row in enumerate(reader):
                for x, cell in enumerate(row):
                    if cell == "1":
                        platform = Platform(x * tile_size, y * tile_size, tile_size, tile_size, "tile.png")
                        self.platforms.add(platform)

    def render(self):
        self.screen.fill((135, 206, 250))  # Светло-голубой фон
        self.platforms.draw(self.screen)
        self.screen.blit(self.player.image, self.player.rect)
        self.player.update(self.platforms)

    def handle_input(self, event):
        """Обработка событий ввода"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:  # Кнопка "A"
                self.player.move_left()
            elif event.key == pygame.K_d:  # Кнопка "D"
                self.player.move_right()
            elif event.key == pygame.K_SPACE:  # Прыжок
                self.player.jump()
        elif event.type == pygame.KEYUP:
            if event.key in [pygame.K_a, pygame.K_d]:  # Остановка при отпускании "A" или "D"
                self.player.stop()