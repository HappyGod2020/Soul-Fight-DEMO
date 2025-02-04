import pygame
from GUI.BaseScreen import BaseScreen
from core.db_manager import DBManager  # Подключаем класс работы с БД

class StatsScreen(BaseScreen):
    def init(self):
        self.add_event(self.handle_input)
        self.font = pygame.font.SysFont("Arial", 36)
        self.small_font = pygame.font.SysFont("Arial", 24)
        self.background_color = (30, 30, 30)  # Темный фон

        # Загружаем статистику из БД
        self.db = DBManager()
        self.total_coins, self.total_time = self.db.get_stats()

        # Параметры кнопки сброса
        self.reset_button_rect = pygame.Rect(self.screen.get_width() // 2 - 100, 250, 200, 50)

    def render(self):
        """Отрисовка окна статистики."""
        self.screen.fill(self.background_color)

        # Заголовок
        title = self.font.render("Статистика игрока", True, (255, 255, 0))
        self.screen.blit(title, (self.screen.get_width() // 2 - title.get_width() // 2, 50))

        # Вывод статистики
        stats = [
            f"Собрано монет: {self.total_coins}",
            f"Общее время в игре: {self.total_time}"
        ]

        for i, stat in enumerate(stats):
            text = self.small_font.render(stat, True, (200, 200, 200))
            self.screen.blit(text, (self.screen.get_width() // 2 - text.get_width() // 2, 150 + i * 40))

        # Кнопка "Сбросить статистику"
        pygame.draw.rect(self.screen, (200, 50, 50), self.reset_button_rect, border_radius=8)
        button_text = self.small_font.render("Сбросить статистику", True, (255, 255, 255))
        self.screen.blit(button_text, (self.screen.get_width() // 2 - button_text.get_width() // 2, 265))

        # Инструкция
        instruction = self.small_font.render("Нажмите ESC для возврата", True, (255, 255, 255))
        self.screen.blit(instruction, (self.screen.get_width() // 2 - instruction.get_width() // 2, 320))

    def handle_input(self, event):
        """Обработка ввода."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # Возвращаемся в главное меню
                from GUI.MenuScreen import MenuScreen
                self.manager_screen.select_screen(MenuScreen)

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.reset_button_rect.collidepoint(event.pos):
                self.reset_stats()

    def reset_stats(self):
        """Сбрасываем статистику в БД и обновляем экран."""
        self.db.cursor.execute("UPDATE stats SET total_coins = 0, total_time = '00:00:00' WHERE id = 1")
        self.db.connection.commit()
        self.total_coins, self.total_time = 0, "00:00:00"