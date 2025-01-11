import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, sprite_path="Sprite/player_sprite.png"):
        super().__init__()
        self.move_flag = 0
        self.flag_stop = False
        self.image = pygame.image.load(sprite_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.velocity = pygame.math.Vector2(0, 0)
        self.max_speed_x = 5  # Скорость движения по горизонтали
        self.new_speed_x = 0
        self.new_speed_y = 0
        self.player_boost = 100
        self.spop_boost = 600
        self.speed = 5
        self.g = 40
        self.flag = False
        self.flag1 = True
        self.jump_speed = 17
        self.on_ground = False
        self.clock = pygame.time.Clock()
        self.fps = 80

    def respawn(self, x, y):
        """Респавн игрока в начальной позиции."""
        self.rect.topleft = (x, y)
        self.velocity = pygame.math.Vector2(0, 0)  # Сбрасываем скорость

    def move(self, screen_width, screen_height, platforms):
        """Перемещение игрока с учётом границ экрана и столкновений"""
        # Горизонтальное движение
        self.rect.x += self.velocity.x
        flag = False
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
        # self.on_ground = False  # Сбрасываем флаг нахождения на земле
        # Проверка столкновений по вертикали
        for i in range(len(platforms)):
            if self.rect.colliderect(platforms[i].rect):
                if self.new_speed_y > 0:  # Падение вниз
                    print('sefsefsefs')
                    self.rect.bottom = platforms[i].rect.top
                    if self.velocity.y != 1:
                        self.on_ground = True
                        flag = True
                    self.velocity.y = 0
                    self.new_speed_y = 0
                elif self.new_speed_y < 0:  # Удар о потолок
                    self.rect.top = platforms[i].rect.bottom
                else:
                    self.rect.bottom = platforms[i].rect.top
                    if self.velocity.y != 1:
                        self.on_ground = True
                        flag = True
                    self.velocity.y = 0
                    self.new_speed_y = 0
            # elif (platforms[i].rect.y - 4 <= self.rect.y + 48 <= platforms[i].rect.y + 4 and
            #       (platforms[i].rect.x - 4 <= self.rect.x <= platforms[i].rect.x + 4 or
            #        platforms[i].rect.x - 4 <= self.rect.x + 48 <= platforms[i].rect.x + 4) or
            #         platforms[i].rect.x - 4 <= self.rect.x - 48 <= platforms[i].rect.x + 4):
            #     if self.new_speed_y > 0:  # Падение вниз
            #         self.on_ground = True
            #         flag = True
            #     elif self.new_speed_y < 0:  # Удар о потолок
            #         pass
            #     else:
            #         self.on_ground = True
            #         flag = True
        if not flag and self.new_speed_x != 0:
            self.on_ground = False
            self.flag = False

        # Ограничение по вертикали
        if self.rect.top < 0:  # Верхняя граница
            self.rect.top = 0
        if self.rect.bottom > screen_height:  # Нижняя граница
            self.rect.bottom = screen_height
            self.new_speed_y = 0
            self.on_ground = True

    def update(self, screen_width, screen_height, platforms, move_flag=0, flag_stop=False):
        """Обновление состояния игрока"""
        if move_flag:
            self.move_flag = move_flag
        if flag_stop:
            self.flag_stop = flag_stop
            self.move_flag = 0
        self.clock.tick(self.fps)
        self.move(screen_width, screen_height, platforms)
        if not self.on_ground and self.new_speed_x == 0:
            self.apply_gravity()
        if not self.on_ground and self.new_speed_x != 0:
            self.boll_movie()
        if self.move_flag == 2 and not flag_stop and self.on_ground:
            self.flag_stop = False
            self.move_right()
        if self.move_flag == 1 and not flag_stop and self.on_ground:
            self.flag_stop = False
            self.move_left()
        if self.flag_stop and self.on_ground:
            self.stop()
            if self.new_speed_x == 0:
                self.flag_stop = False
        print(self.velocity.x, self.velocity.y, self.new_speed_x, self.new_speed_y, self.on_ground)

    def apply_gravity(self):
        """Применение гравитации"""
        print(self.new_speed_y, self.on_ground)
        self.velocity.y += self.new_speed_y * 0.0125 + (self.g * 0.0125 ** 2) / 2
        self.new_speed_y += self.g * 0.0125
        self.flag = False

    def boll_movie(self):
        self.apply_gravity()
        self.velocity.x += self.new_speed_x * 0.0125

    def jump(self):
        """Прыжок"""
        if self.on_ground:
            self.new_speed_y = -self.jump_speed
            self.on_ground = False

    def move_left(self):
        """Движение влево"""
        if abs(self.new_speed_x - self.player_boost * 0.0125) <= self.max_speed_x:
            self.velocity.x += self.new_speed_x * 0.0125 - (self.player_boost * 0.0125 ** 2) / 2
            self.new_speed_x -= self.player_boost * 0.0125
        else:
            self.velocity.x += self.new_speed_x * 0.0125
        self.flag = False
        # self.velocity.y = 1

    def move_right(self):
        """Движение вправо"""
        if self.new_speed_x + self.player_boost * 0.0125 <= self.max_speed_x:
            self.velocity.x += self.new_speed_x * 0.0125 + (self.player_boost * 0.0125 ** 2) / 2
            self.new_speed_x += self.player_boost * 0.0125
        else:
            self.velocity.x += self.new_speed_x * 0.0125
        self.flag = False
        # self.velocity.y = 1

    def stop(self):
        """Остановка"""
        if self.new_speed_x != 0:
            if self.new_speed_x > 0:
                if self.new_speed_x - self.spop_boost * 0.0125 <= 0:
                    self.new_speed_x = 0
                    self.velocity.x = 0
                    self.velocity.y = 1
                    self.flag = True
                else:
                    self.velocity.x += self.new_speed_x * 0.0125 - (self.spop_boost * 0.0125 ** 2) / 2
                    self.new_speed_x -= self.spop_boost * 0.0125
            if self.new_speed_x < 0:
                if self.new_speed_x + self.spop_boost * 0.0125 >= 0:
                    self.new_speed_x = 0
                    self.velocity.x = 0
                    self.velocity.y = 1
                    self.flag = True
                else:
                    self.velocity.x += -self.new_speed_x * 0.0125 + (self.spop_boost * 0.0125 ** 2) / 2
                    self.new_speed_x += self.spop_boost * 0.0125
