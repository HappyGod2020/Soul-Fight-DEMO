from GUI.BaseScreen import BaseScreen
import pygame
from core.settings import GUI_SETTINGS


class MenuScreen(BaseScreen):

    def init(self):  # Функция "АнтиСпама"
        self.add_event(self.callback_start)
        self.add_event(self.callback_exit)
        self.add_event(self.callback_setting)

    def render(self):  # Отрисовка (Рендер)
        self.png_main()
        self.png_start()
        self.png_setting()
        self.png_exit()

    def callback_start(self, e):
        pos = pygame.mouse.get_pos()
        but_down = pygame.mouse.get_pressed()
        if but_down[0]:
            if GUI_SETTINGS.WIDTH // 2 - 75 <= pos[0] <= GUI_SETTINGS.WIDTH // 2 + 75:
                if (GUI_SETTINGS.HEIGHT - 120 - 70) // 2 <= pos[1] <= ((GUI_SETTINGS.HEIGHT - 120 - 70) // 2) + 40:
                    self.manager_screen.select_screen(BaseScreen)
                    # старт базе скриин доделан, и это радует, как инчае то  ххахахахахахахахахаха

    def callback_setting(self, e):
        pos = pygame.mouse.get_pos()
        but_down = pygame.mouse.get_pressed()
        if but_down[0]:
            if GUI_SETTINGS.WIDTH // 2 - 75 <= pos[0] <= GUI_SETTINGS.WIDTH // 2 + 75:
                if (GUI_SETTINGS.HEIGHT - 120 - 70) // 2 + 75 <= pos[1] <= (GUI_SETTINGS.HEIGHT - 120 - 70) // 2 + 115:
                    print("сетт доделать")

    def callback_exit(self, e):  # Проверка нажатия кнопки выхода, Выход из игры
        pos = pygame.mouse.get_pos()
        but_down = pygame.mouse.get_pressed()
        if but_down[0]:
            if GUI_SETTINGS.WIDTH // 2 - 75 <= pos[0] <= GUI_SETTINGS.WIDTH // 2 + 75:
                if ((GUI_SETTINGS.HEIGHT - 190) // 2) + 150 <= pos[1] <= ((GUI_SETTINGS.HEIGHT - 120 - 70) // 2) + 190:
                    self.manager_screen.main_game.is_game = False
                    print("выход по кнопке регистр")

    def png_main(self):
        main_png = pygame.image.load("fon_main.png")
        main_idle = pygame.transform.scale(main_png, (GUI_SETTINGS.WIDTH, GUI_SETTINGS.HEIGHT))
        self.manager_screen.main_game.screen.blit(main_idle, (0, 0))

    def png_start(self):
        start_png = pygame.image.load("start.png")
        start_png.set_colorkey((255, 255, 255))
        start_idle = pygame.transform.scale(start_png, (150, 40))
        self.manager_screen.main_game.screen.blit(start_idle, (GUI_SETTINGS.WIDTH // 2 - 75,
                                                               (GUI_SETTINGS.HEIGHT - 120 - 70) // 2))

    def png_setting(self):
        setting_png = pygame.image.load("setting.png")
        setting_png.set_colorkey((255, 255, 255))
        setting_idle = pygame.transform.scale(setting_png, (150, 40))
        self.manager_screen.main_game.screen.blit(setting_idle, (GUI_SETTINGS.WIDTH // 2 - 75,
                                                                 (GUI_SETTINGS.HEIGHT - 120 - 70) // 2 + 75))

    def png_exit(self):
        exit_png = pygame.image.load("quit.png")
        exit_idle = pygame.transform.scale(exit_png, (150, 40))
        exit_png.set_colorkey((255, 255, 255))
        self.manager_screen.main_game.screen.blit(exit_idle, (GUI_SETTINGS.WIDTH // 2 - 75,
                                                              (GUI_SETTINGS.HEIGHT - 120 - 70) // 2 + 150))
