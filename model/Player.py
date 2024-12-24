import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, sprite_path="Sprite/player_sprite.png"):
        super().__init__()
        self.image = pygame.image.load(sprite_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.velocity = pygame.math.Vector2(0, 0)
        self.speed = 2  # Скорость движения по горизонтали
        self.gravity = 0.5
        self.max_fall_speed = 2  # Максимальная скорость падения
        self.jump_strength = -10
        self.on_ground = False

    def respawn(self, x, y):
        """Респавн игрока в начальной позиции."""
        self.rect.topleft = (x, y)
        self.velocity = pygame.math.Vector2(0, 0)  # Сбрасываем скорость

    def move(self, screen_width, screen_height, platforms):
        """Перемещение игрока с учётом границ экрана и столкновений"""
        # Горизонтальное движение
        self.rect.x += self.velocity.x

        # Проверка столкновений по горизонтали
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.velocity.x > 0:  # Движение вправо
                    self.rect.right = platform.rect.left
                elif self.velocity.x < 0:  # Движение влево
                    self.rect.left = platform.rect.right

        # Ограничение по горизонтали
        if self.rect.left < 0:  # Левая граница
            self.rect.left = 0
        if self.rect.right > screen_width:  # Правая граница
            self.rect.right = screen_width

        # Вертикальное движение
        self.rect.y += self.velocity.y
        self.on_ground = False  # Сбрасываем флаг нахождения на земле

        # Проверка столкновений по вертикали
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.velocity.y > 0:  # Падение вниз
                    self.rect.bottom = platform.rect.top
                    self.velocity.y = 0
                    self.on_ground = True
                elif self.velocity.y < 0:  # Удар о потолок
                    self.rect.top = platform.rect.bottom
                    self.velocity.y = 0

        # Ограничение по вертикали
        if self.rect.top < 0:  # Верхняя граница
            self.rect.top = 0
            self.velocity.y = 0
        if self.rect.bottom > screen_height:  # Нижняя граница
            self.rect.bottom = screen_height
            self.on_ground = True

    def update(self, screen_width, screen_height, platforms):
        """Обновление состояния игрока"""
        self.apply_gravity()
        self.move(screen_width, screen_height, platforms)

    def apply_gravity(self):
        """Применение гравитации"""

        self.velocity.y += self.gravity
        if self.velocity.y > self.max_fall_speed:
            self.velocity.y = self.max_fall_speed

    def jump(self):
        """Прыжок"""

        self.velocity.y = self.jump_strength

    def move_left(self):
        """Движение влево"""
        self.velocity.x = -self.speed

    def move_right(self):
        """Движение вправо"""
        self.velocity.x = self.speed

    def stop(self):
        """Остановка"""
        self.velocity.x = 0
