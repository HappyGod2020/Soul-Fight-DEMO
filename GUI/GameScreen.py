import os
from GUI.BaseScreen import BaseScreen
from model.Player import Player
import pygame
import csv
from model.Spike import Spike
from model.Door import Door
from core.settings import GUI_SETTINGS
from model.Coin import Coin
from core.db_manager import DBManager
import time


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, sprite_path="Sprite/tile.png"):
        super().__init__()
        self.image = pygame.image.load(sprite_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))


class GameScreen(BaseScreen):
    def init(self):
        self.db_manager = DBManager()
        self.start_time = time.time()
        self.collected_coins = 0
        self.platforms = []
        self.spikes = []
        self.coins = pygame.sprite.Group()
        self.levels_folder = "levels"
        self.level_index = 1
        self.door = None
        self.height_block = self.width_block = GUI_SETTINGS.HEIGHT / 18
        self.player = Player(x=48, y=400, width=GUI_SETTINGS.HEIGHT / 19,
                             height=GUI_SETTINGS.HEIGHT // 19)  # Начальная позиция игрока
        self.background = None  # Фон уровня

        self.load_level()
        self.add_event(self.handle_input)
        self.clock = pygame.time.Clock()

    def load_level(self):
        """Загрузка текущего уровня из CSV."""
        level_file = os.path.join(self.levels_folder, f"level{self.level_index}.csv")
        if not os.path.exists(level_file):
            from GUI.FinalScreen import FinalScreen
            self.manager_screen.select_screen(FinalScreen)
        self.player.respawn(50, 400)
        self.platforms.clear()
        self.spikes.clear()
        self.door = None

        # Загружаем фон уровня
        self.background = pygame.image.load('Sprite/game_fon.png').convert_alpha()
        self.background = pygame.transform.scale(self.background, (GUI_SETTINGS.WIDTH, GUI_SETTINGS.HEIGHT))

        # Загрузка объектов уровня
        with open(level_file, "r") as csvfile:
            reader = csv.reader(csvfile)
            for y, row in enumerate(reader):
                for x, cell in enumerate(row):
                    if cell == "1":  # Платформа
                        platform = Platform(x * self.width_block, y * self.height_block, self.width_block,
                                            self.height_block)  # Размеры платформ
                        self.platforms.append(platform)
                    elif cell == "2":  # Шипы
                        spike = Spike(x * self.width_block, y * self.height_block, self.width_block, self.height_block)
                        self.spikes.append(spike)
                    elif cell == "3":  # Дверь
                        self.door = Door(x * self.width_block, y * self.height_block, self.width_block,
                                         self.height_block)
                    elif cell == "4":
                        coin = Coin(x * self.width_block, y * self.height_block, self.width_block, self.height_block)
                        self.coins.add(coin)

    def render(self):
        """Отрисовка игрового процесса."""
        font = pygame.font.SysFont("Arial", 24)
        text = font.render(f"Монет собрано: {self.collected_coins}", True, (255, 255, 255))

        # Отрисовка фона
        if self.background:
            self.screen.blit(self.background, (0, 0))

        # Отрисовка платформ
        for platform in self.platforms:
            self.screen.blit(platform.image, platform.rect)

        # Отрисовка шипов
        for spike in self.spikes:
            self.screen.blit(spike.image, spike.rect)

        # Отрисовка двери
        if self.door:
            self.screen.blit(self.door.image, self.door.rect)

        # Отрисовка монеток
        for coin in self.coins:
            self.screen.blit(coin.image, coin.rect)

        # Отрисовка игрока
        self.screen.blit(self.player.image, self.player.rect)

        # Обновление игрока
        self.player.update(GUI_SETTINGS.WIDTH, GUI_SETTINGS.HEIGHT, self.platforms)

        # Проверка на столкновения
        self.check_collisions()
        self.screen.blit(text, (10, 10))

    def check_collisions(self):
        """Проверка столкновений игрока с шипами и дверью."""
        # Проверка столкновения с шипами
        for spike in self.spikes:
            if self.player.rect.colliderect(spike.rect):
                self.player.respawn(50, 400)  # Спавн в начальной позиции

        collisions = pygame.sprite.spritecollide(self.player, self.coins, True)
        for coin in collisions:
            self.collect_coin()
        # Проверка столкновения с дверью
        if self.door and self.player.rect.colliderect(self.door.rect):
            self.next_level()

    def collect_coin(self):
        self.collected_coins += 1

    def next_level(self):
        time_played = time.time() - self.start_time
        formatted_time = time.strftime("%H:%M:%S", time.gmtime(time_played))
        self.db_manager.update_time(formatted_time)
        self.db_manager.update_coins(self.collected_coins)
        self.collected_coins = 0
        self.start_time = time.time()
        """Переключение на следующий уровень."""
        self.level_index += 1
        self.load_level()

    def handle_input(self, event):
        """Обработка ввода с клавиатуры."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                self.player.move_left()
            elif event.key == pygame.K_d:
                self.player.move_right()
            elif event.key == pygame.K_SPACE:
                self.player.jump()
        if event.type == pygame.KEYUP:
            if event.key in [pygame.K_a, pygame.K_d]:
                self.player.stop()
