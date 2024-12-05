from core.settings import GUI_SETTINGS
import pygame

class BaseScreen:

    def __init__(self, manager_screen):
        self.manager_screen = manager_screen

        self.screen = self.manager_screen.main_game.screen

        self.init()

    def init(self):
        self.add_event(self.callback_exit_to_menu)

    def callback_exit_to_menu(self, e):
        pos = pygame.mouse.get_pos()
        but_down = pygame.mouse.get_pressed()
        if but_down[0]:
            if GUI_SETTINGS.WIDTH // 2 - 75 <= pos[0] <= GUI_SETTINGS.WIDTH // 2 + 75:
                if (GUI_SETTINGS.HEIGHT - 120 - 70) // 2 <= pos[1] <= ((GUI_SETTINGS.HEIGHT - 120 - 70) // 2) + 40:
                    self.manager_screen.main_game.is_game = False


    def render(self):
        self.png_main()
        self.png_exit_to_main()

    def add_event(self, func):
        self.manager_screen.main_game.event_array.append(func)

    def png_main(self):
        main_png = pygame.image.load("game-fon.jpg")
        main_idle = pygame.transform.scale(main_png, (GUI_SETTINGS.WIDTH, GUI_SETTINGS.HEIGHT))
        self.manager_screen.main_game.screen.blit(main_idle, (0, 0))

    def png_exit_to_main(self):
        start_png = pygame.image.load("icon-to-menu.png")
        start_png.set_colorkey((255, 255, 255))
        start_idle = pygame.transform.scale(start_png, (150, 40))
        self.manager_screen.main_game.screen.blit(start_idle, (GUI_SETTINGS.WIDTH // 2 - 75,
                                                               (GUI_SETTINGS.HEIGHT - 120 - 70) // 2))
