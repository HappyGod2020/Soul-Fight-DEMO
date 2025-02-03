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


class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, sprite_path="Sprite/button.png"):
        super().__init__()
        self.image = pygame.image.load(sprite_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))


class GameScreen(BaseScreen):
    def init(self):
        self.db_manager = DBManager()
        self.clock = pygame.time.Clock()
        self.start_time = time.time()
        self.collected_coins = 0
        self.platforms = []
        self.platforms_close = []
        self.spikes = []
        self.buttons = []
        self.under_button_block = []
        self.count_coin = 0
        self.coins = pygame.sprite.Group()
        self.levels_folder = "levels"
        self.level_index = 1
        self.door = None
        self.Flag = False
        self.height_block = self.width_block = GUI_SETTINGS.HEIGHT / 18
        self.player = Player(x=48, y=400, width=GUI_SETTINGS.HEIGHT // 18 - 2,
                             height=GUI_SETTINGS.HEIGHT // 18 - 2)  # Начальная позиция игрока
        self.collisions = pygame.sprite.spritecollide(self.player, self.coins, True)
        self.background = None  # Фон уровня

        self.load_level()
        self.add_event(self.handle_input)
        self.clock = pygame.time.Clock()

    def load_level(self):
        """Загрузка текущего уровня из CSV."""
        self.player.death_flag = False
        level_file = os.path.join(self.levels_folder, f"level{self.level_index}.csv")
        if not os.path.exists(level_file):
            self.Flag = True
            from GUI.FinalScreen import FinalScreen
            self.manager_screen.select_screen(FinalScreen)
        self.player.respawn(0, GUI_SETTINGS.HEIGHT / 18 * 10)
        self.player.level(self.level_index)

        self.platforms.clear()
        self.spikes.clear()
        self.door = None

        # Загружаем фон уровня
        self.background = pygame.image.load('Sprite/game_fon.png').convert_alpha()
        self.background = pygame.transform.scale(self.background, (GUI_SETTINGS.WIDTH, GUI_SETTINGS.HEIGHT))

        # Загрузка объектов уровня
        self.platforms_close = []
        if not self.Flag:
            with open(level_file, "r") as csvfile:
                reader = csv.reader(csvfile)
                for y, row in enumerate(reader):
                    for x, cell in enumerate(row):
                        if cell == "1":  # Платформа
                            platform = Platform(x * self.width_block, y * self.height_block, self.width_block,
                                                self.height_block)  # Размеры платформ
                            self.platforms.append(platform)
                            if x == 28 and (y == 4 or y == 3 or y == 2):
                                self.platforms_close.append(platform)
                            if x in (16, 17, 18) and y == 5:
                                self.under_button_block.append(platform)
                        elif cell == "2":  # Шипы
                            spike = Spike(x * self.width_block, y * self.height_block, self.width_block, self.height_block)
                            self.spikes.append(spike)
                        elif cell == "3":  # Дверь
                            self.door = Door(x * self.width_block, y * self.height_block, self.width_block,
                                             self.height_block)
                        elif cell == "4":
                            coin = Coin(x * self.width_block, y * self.height_block, self.width_block, self.height_block)
                            self.coins.add(coin)
                        elif cell == '5':
                            platform = Platform(x * self.width_block, y * self.height_block, self.width_block,
                                                self.height_block)  # Размеры платформ
                            self.platforms.append(platform)
                            button = Button(x * self.width_block, y * self.height_block, self.width_block, self.height_block)
                            self.buttons.append(button)

    def render(self):
        """Отрисовка игрового процесса."""
        font = pygame.font.SysFont("Arial", 24)
        text = font.render(f"Монет собрано: {self.count_coin}", True, (255, 255, 255))

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

        for button in self.buttons:
            self.screen.blit(button.image, button.rect)

        for platform in self.under_button_block:
            self.screen.blit(platform.image, platform.rect)

        # Проверка на столкновения
        self.check_collisions()
        self.screen.blit(text, (10, 10))

        # Отрисовка игрока
        self.screen.blit(self.player.image, self.player.rect)
        if self.player.back_flag:
            self.player.respawn(0, GUI_SETTINGS.HEIGHT / 18 * 10)
        # Обновление игрока
        self.player.update(GUI_SETTINGS.WIDTH, GUI_SETTINGS.HEIGHT, self.platforms, self.platforms_close, self.buttons, count_coin=self.count_coin)

    def check_collisions(self):
        """Проверка столкновений игрока с шипами и дверью."""
        # Проверка столкновения с шипами
        flag = True
        for spike in self.spikes:
            p = self.player.rect
            s = spike.rect
            if ((p.right - 10 > s.left and p.left < s.left) or (p.left < s.right - 10 and p.right > s.right)) and p.bottom >= s.top and p.top <= s.top + 20 and not self.player.death_flag:
                self.player.death_flag = True
                # self.player.respawn(0, GUI_SETTINGS.HEIGHT / 18 * 10)  # Спавн в начальной позиции

        # for platforms in self.platforms_close:
        if (self.platforms[-1].rect.bottom > self.player.rect.top and
                (self.player.rect.right > self.platforms[-1].rect.left and self.player.rect.left < self.platforms[-1].rect.right)):
            self.player.respawn(0, GUI_SETTINGS.HEIGHT / 18 * 10)

        collisions = pygame.sprite.spritecollide(self.player, self.coins, True)
        for coin in collisions:
            self.collect_coin()
            self.count_coin += 1
        # Проверка столкновения с дверью
        if self.door and self.player.rect.colliderect(self.door.rect):
            self.next_level()

    def collect_coin(self):
        self.collected_coins += 1

    def next_level(self):
        self.coins = pygame.sprite.Group()
        time_played = time.time() - self.start_time
        formatted_time = time.strftime("%H:%M:%S", time.gmtime(time_played))
        self.db_manager.update_time(formatted_time)
        self.db_manager.update_coins(self.collected_coins)
        self.collected_coins = 0
        self.count_coin = 0
        self.start_time = time.time()
        """Переключение на следующий уровень."""
        self.level_index += 1
        self.load_level()

    def handle_input(self, event):
        """Обработка ввода с клавиатуры."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                self.player.update(GUI_SETTINGS.WIDTH, GUI_SETTINGS.HEIGHT, self.platforms, self.platforms_close, self.buttons, move_flag=1, count_coin=self.count_coin)
            elif event.key == pygame.K_d:
                self.player.update(GUI_SETTINGS.WIDTH, GUI_SETTINGS.HEIGHT, self.platforms, self.platforms_close, self.buttons, move_flag=2, count_coin=self.count_coin)
            elif event.key == pygame.K_SPACE:
                self.player.jump()
        if event.type == pygame.KEYUP:
            if event.key in [pygame.K_a, pygame.K_d]:
                self.player.update(GUI_SETTINGS.WIDTH, GUI_SETTINGS.HEIGHT, self.platforms, self.platforms_close, self.buttons, flag_stop=True, count_coin=self.count_coin)
