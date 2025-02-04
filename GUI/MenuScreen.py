from GUI.BaseScreen import BaseScreen
import pygame
from core.settings import GUI_SETTINGS
from GUI.GameScreen import GameScreen
from GUI.StatsScreen import StatsScreen

class MenuScreen(BaseScreen):

    def init(self):
        self.add_event(self.callback_start)
        self.add_event(self.callback_exit)
        self.add_event(self.callback_stats)

    def render(self):
        self.render_background()
        self.render_buttons()

    def render_background(self):
        background = pygame.image.load("Sprite/menu_background.png")
        background = pygame.transform.scale(background, (GUI_SETTINGS.WIDTH, GUI_SETTINGS.HEIGHT))
        self.screen.blit(background, (0, 0))

    def render_buttons(self):
        start_button = pygame.image.load("Sprite/start_button.png")
        start_button = pygame.transform.scale(start_button, (200, 50))
        self.screen.blit(start_button, (GUI_SETTINGS.WIDTH // 2 - 100, GUI_SETTINGS.HEIGHT // 2 - 50))

        statist_button = pygame.image.load("Sprite/statist_button.png")
        statist_button = pygame.transform.scale(statist_button, (200, 200))
        self.screen.blit(statist_button, (GUI_SETTINGS.WIDTH // 2 + 200, GUI_SETTINGS.HEIGHT // 2 - 300))

        exit_button = pygame.image.load("Sprite/exit_button.png")
        exit_button = pygame.transform.scale(exit_button, (200, 50))
        self.screen.blit(exit_button, (GUI_SETTINGS.WIDTH // 2 - 100, GUI_SETTINGS.HEIGHT // 2 + 20))

    def callback_start(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if GUI_SETTINGS.WIDTH // 2 - 100 <= x <= GUI_SETTINGS.WIDTH // 2 + 100:
                if GUI_SETTINGS.HEIGHT // 2 - 50 <= y <= GUI_SETTINGS.HEIGHT // 2:
                    self.manager_screen.select_screen(GameScreen)

    def callback_exit(self, event):
        if isinstance(self.manager_screen.screen, GameScreen):
            return
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if GUI_SETTINGS.WIDTH // 2 - 100 <= x <= GUI_SETTINGS.WIDTH // 2 + 100:
                if GUI_SETTINGS.HEIGHT // 2 + 20 <= y <= GUI_SETTINGS.HEIGHT // 2 + 70:
                    pygame.quit()
                    exit()

    def callback_stats(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if GUI_SETTINGS.WIDTH // 2 + 200 <= x <= GUI_SETTINGS.WIDTH // 2 + 400:
                if GUI_SETTINGS.HEIGHT // 2 - 300 <= y <= GUI_SETTINGS.HEIGHT // 2 - 100:
                    self.manager_screen.select_screen(StatsScreen)