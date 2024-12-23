import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, sprite_path="player_sprite.png"):
        super().__init__()
        self.image = pygame.image.load(sprite_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.velocity = pygame.math.Vector2(0, 0)
        self.speed = 3  # Скорость движения по горизонтали
        self.gravity = 0.2
        self.jump_strength = -15
        self.on_ground = False

    def update(self, platforms):
        """Обновление состояния игрока"""
        self.apply_gravity()
        self.move_and_collide(platforms)

    def apply_gravity(self):
        """Применение гравитации"""
        if not self.on_ground:
            self.velocity.y += self.gravity

    def move_and_collide(self, platforms):
        """Перемещение с учётом столкновений"""
        # Горизонтальное движение
        self.rect.x += self.velocity.x
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.velocity.x > 0:  # Движение вправо
                    self.rect.right = platform.rect.left
                elif self.velocity.x < 0:  # Движение влево
                    self.rect.left = platform.rect.right

        # Вертикальное движение
        self.rect.y += self.velocity.y
        self.on_ground = False  # Сбрасываем флаг нахождения на земле
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.velocity.y > 0:  # Падение вниз
                    self.rect.bottom = platform.rect.top
                    self.velocity.y = 0
                    self.on_ground = True
                elif self.velocity.y < 0:  # Удар о потолок
                    self.rect.top = platform.rect.bottom
                    self.velocity.y = 0

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
