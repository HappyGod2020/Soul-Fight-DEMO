from pygame import display, FULLSCREEN, event, QUIT, font
from .settings import GUI_SETTINGS
from .ManagerScreen import ManagerScreen
from GUI.MenuScreen import MenuScreen
import pygame


class Game:
    def __init__(self):
        pygame.init()  # Инициализация всех модулей Pygame
        info = display.Info()
        GUI_SETTINGS.WIDTH = info.current_w
        GUI_SETTINGS.HEIGHT = info.current_h

        WIDTH = GUI_SETTINGS.WIDTH
        HEIGHT = GUI_SETTINGS.HEIGHT
        args = [(WIDTH, HEIGHT)]
        if GUI_SETTINGS.is_FullScreen:
            args.append(FULLSCREEN)
        self.screen = display.set_mode(*args)
        display.set_caption("Soul Fight DEMO")
        font.init()

        self.event_array = []

        self.manage_screen = ManagerScreen(self)
        self.manage_screen.select_screen(MenuScreen)  # Устанавливаем начальный экран

        self.update()

    def update(self):
        self.is_game = True
        while self.is_game:
            self.screen.fill((0, 0, 0))
            self.event_loop()
            if self.manage_screen.screen:  # Проверяем, установлен ли экран
                self.manage_screen.screen.render()
            display.update()

    def event_loop(self):
        for e in event.get():
            if e.type == QUIT:
                self.is_game = False
            for fun in self.event_array:
                fun(e)
