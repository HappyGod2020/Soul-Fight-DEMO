import pygame
from GUI.BaseScreen import BaseScreen


class FinalScreen(BaseScreen):
    def init(self):
        self.add_event(self.handle_input)  # Добавляем обработку событий
        self.font = pygame.font.SysFont("Arial", 36)
        self.small_font = pygame.font.SysFont("Arial", 24)
        self.background_color = (0, 0, 128)  # Темно-синий фон

    def render(self):
        """Отрисовка финального окна."""
        self.screen.fill(self.background_color)

        # Поздравительное сообщение
        congrats_text = self.font.render("Поздравляем!", True, (255, 255, 0))
        self.screen.blit(congrats_text, (self.screen.get_width() // 2 - congrats_text.get_width() // 2, 50))

        # Информация о прохождении
        info_text = self.small_font.render("Вы успешно прошли игру!", True, (255, 255, 255))
        self.screen.blit(info_text, (self.screen.get_width() // 2 - info_text.get_width() // 2, 120))

        # Техническая информация
        dev_info = [
            "Soul Fight DEMO v0.9",
            "Разработано с использованием Pygame",
            "Авторы: Муратов Богдан, Михайлов Вячеслав",
            "Благодарим за игру!"
        ]
        for i, line in enumerate(dev_info):
            line_rendered = self.small_font.render(line, True, (200, 200, 200))
            self.screen.blit(line_rendered,
                             (self.screen.get_width() // 2 - line_rendered.get_width() // 2, 180 + i * 30))

        # Инструкция
        instruction_text = self.small_font.render("Нажмите ESC, чтобы выйти в меню", True, (255, 255, 255))
        self.screen.blit(instruction_text, (self.screen.get_width() // 2 - instruction_text.get_width() // 2, 300))

    def handle_input(self, event):
        """Обработка нажатий клавиш."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # Возврат в главное меню
                from GUI.MenuScreen import MenuScreen
                self.manager_screen.select_screen(MenuScreen)
