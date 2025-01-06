import os
from GUI.BaseScreen import BaseScreen
from model.Player import Player
import pygame
import csv
from model.Spike import Spike
from model.Door import Door
from core.settings import GUI_SETTINGS


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, sprite_path="Sprite/блок1.2.png"):
        super().__init__()
        self.image = pygame.image.load(sprite_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))


class GameScreen(BaseScreen):
    def init(self):
        self.platforms = []
        self.spikes = []
        self.levels_folder = "levels"
        self.level_index = 1
        self.door = None
        self.player = Player(x=48, y=400, width=GUI_SETTINGS.HEIGHT // 16, height=GUI_SETTINGS.HEIGHT // 16)  # Начальная позиция игрока
        self.load_level()
        self.add_event(self.handle_input)
        self.clock = pygame.time.Clock()

    def load_level(self):
        """Загрузка текущего уровня из CSV."""
        level_file = os.path.join(self.levels_folder, f"level{self.level_index}.csv")
        if not os.path.exists(level_file):
            print("Все уровни пройдены!")
            pygame.quit()
            exit()
        self.player.respawn(50, 400)
        self.platforms.clear()
        self.spikes.clear()
        self.door = None

        with open(level_file, "r") as csvfile:
            reader = csv.reader(csvfile)
            for y, row in enumerate(reader):
                for x, cell in enumerate(row):
                    x_pos = x * 48
                    y_pos = y * 48
                    if cell == "1":  # Платформа
                        platform = Platform(x * 48, y * 48, 48, 48)  # Размеры платформ
                        self.platforms.append(platform)
                    elif cell == "2":  # Шипы
                        spike = Spike(x * 48, y * 48, 48, 48)
                        self.spikes.append(spike)
                    elif cell == "3":  # Дверь
                        self.door = Door(x * 48, y * 48, 48, 48)
    #
    # def load_map(self):
    #     """Загрузка карты из CSV файла."""
    #     with open(filename, "r") as file:
    #         reader = csv.reader(file)
    #         for y, row in enumerate(reader):
    #             for x, tile in enumerate(row):
    #                 if tile == "1":  # Платформа
    #                     platform = Platform(x * 50, y * 50, 50, 50)  # Размеры платформ
    #                     self.platforms.append(platform)
    #                 elif tile == "2":  # Шипы
    #                     spike = Spike(x * 50, y * 50, 50, 50)
    #                     self.spikes.append(spike)
    #                 elif tile == "3":  # Дверь
    #                     self.door = Door(x * 50, y * 50, 50, 50)

    def render(self):
        # self.image = pygame.image.load('Sprite/страшный фон.png').convert_alpha()
        # self.image = pygame.transform.scale(self.image, (1920, 1080))
        # self.screen.blit(self.image, (0, 0))
        """Отрисовка игрового процесса."""
        # Отрисовка платформ
        for platform in self.platforms:
            self.screen.blit(platform.image, platform.rect)

        # Отрисовка шипов
        for spike in self.spikes:
            self.screen.blit(spike.image, spike.rect)

        # Отрисовка двери
        if self.door:
            self.screen.blit(self.door.image, self.door.rect)

        # Отрисовка игрока
        self.screen.blit(self.player.image, self.player.rect)

        # Обновление игрока
        self.player.update(GUI_SETTINGS.WIDTH, GUI_SETTINGS.HEIGHT, self.platforms)

        # Проверка на столкновения
        self.check_collisions()

    def check_collisions(self):
        """Проверка столкновений игрока с шипами и дверью."""
        # Проверка столкновения с шипами
        for spike in self.spikes:
            if self.player.rect.colliderect(spike.rect):
                self.player.respawn(50, 400)  # Спавн в начальной позиции

        # Проверка столкновения с дверью
        if self.door and self.player.rect.colliderect(self.door.rect):
            self.next_level()

    def next_level(self):
        """Переключение на следующий уровень."""
        self.level_index += 1
        self.load_level()

    def handle_input(self, event):
        """Обработка ввода с клавиатуры."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                self.player.update(GUI_SETTINGS.WIDTH, GUI_SETTINGS.HEIGHT, self.platforms, 1)
            elif event.key == pygame.K_d:
                self.player.update(GUI_SETTINGS.WIDTH, GUI_SETTINGS.HEIGHT, self.platforms, 2)
            elif event.key == pygame.K_SPACE:
                self.player.jump()
        if event.type == pygame.KEYUP:
            if event.key in [pygame.K_a, pygame.K_d]:
                self.player.update(GUI_SETTINGS.WIDTH, GUI_SETTINGS.HEIGHT, self.platforms, flag_stop=True)
