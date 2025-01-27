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
        self.flag = True
        self.hitting_the_left_wall_flag = False
        self.hitting_the_right_wall_flag = False
        self.hitting_the_floor_flag = False
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
        # print(self.new_speed_y)
        self.rect.x += self.velocity.x
        flag = False
        # print(self.hitting_the_left_wall_flag)
        # print(self.hitting_the_right_wall_flag)
        # Проверка столкновений по горизонтали
        # for platform in platforms:
        #     if self.rect.colliderect(platform.rect):
        #         if self.new_speed_x > 0 and platform.rect.top - 4 <= self.rect.top <= platform.rect.top + 4:  # Движение вправо
        #             self.hitting_the_right_wall_flag = True
        #             self.rect.right = platform.rect.left
        #             self.new_speed_x = 0
        #             self.velocity.x = 0
        #         elif self.new_speed_x < 0 and platform.rect.top - 4 <= self.rect.top <= platform.rect.top + 4:  # Движение влево
        #             self.rect.left = platform.rect.right
        #             self.new_speed_x = 0
        #             self.velocity.x  = 0
        #             self.hitting_the_left_wall_flag = True

        # # Ограничение по горизонтали
        # if self.rect.left < 0:  # Левая граница
        #     self.rect.left = 0
        #     self.new_speed_x = abs(self.new_speed_x)
        #     self.hitting_the_left_wall_flag = True
        # if self.rect.right > screen_width:  # Правая граница
        #     self.rect.right = screen_width
        #     self.new_speed_x = - abs(self.new_speed_x)
        #     self.hitting_the_right_wall_flag = True
        # self.on_ground = False  # Сбрасываем флаг нахождения на земле
        # Проверка столкновений по вертикали
        crossing_flag = False
        for i in range(len(platforms)):
            # if self.rect.colliderect(platforms[i].rect):
            # print(self.new_speed_y)
            if not crossing_flag:
                if (((platforms[i].rect.y - 4 <= self.rect.y + 48 <= platforms[i].rect.y + 4 and
                        (platforms[i].rect.left < self.rect.right < platforms[i].rect.right or
                         platforms[i].rect.left < self.rect.left < platforms[i].rect.right) and self.new_speed_y >= 1)) or
                        self.hitting_the_floor_flag and
                        platforms[i].rect.y - 4 <= self.rect.y + 48 <= platforms[i].rect.y + 4 and
                        (platforms[i].rect.left < self.rect.right < platforms[i].rect.right or
                         platforms[i].rect.left < self.rect.left < platforms[i].rect.right)):
                    crossing_flag = True
                    # print('падение при высокой скорости')
                    if self.new_speed_y > 0:  # Падение вниз
                        self.rect.bottom = platforms[i].rect.top
                        self.on_ground = True
                        flag = True
                        self.velocity.y = 0
                        self.new_speed_y = 0
                    else:
                        self.rect.bottom = platforms[i].rect.top
                        self.on_ground = True
                        flag = True
                        self.velocity.y = 0
                        self.new_speed_y = 0
                elif (platforms[i].rect.bottom - 4 <= self.rect.top <= platforms[i].rect.bottom + 4 and
                      (platforms[i].rect.left < self.rect.right < platforms[i].rect.right or
                       platforms[i].rect.left < self.rect.left < platforms[i].rect.right)) and self.new_speed_y < 0:
                    crossing_flag = True
                    # print('удар о потолок при высокой скорости', self.new_speed_y)
                    if self.new_speed_y < 0:  # Удар о потолок
                        self.rect.top = platforms[i].rect.bottom
                        self.velocity.y = 0
                        self.new_speed_y = - self.new_speed_y
                elif (platforms[i].rect.y - 4 <= self.rect.y + 48 <= platforms[i].rect.y + 4 and
                        (platforms[i].rect.left < self.rect.right < platforms[i].rect.right or
                         platforms[i].rect.left < self.rect.left < platforms[i].rect.right) and 0 < self.new_speed_y < 1):
                    crossing_flag = True
                    # print('падение при низкой скорости')
                    if self.new_speed_y > 0:  # Падение вниз
                        self.on_ground = True
                        flag = True
                    else:
                        self.on_ground = True
                        flag = True
                elif (platforms[i].rect.bottom - 4 <= self.rect.top <= platforms[i].rect.bottom + 4 and
                          (platforms[i].rect.left < self.rect.right < platforms[i].rect.right or
                           platforms[i].rect.left < self.rect.left < platforms[i].rect.right)): # Удар о потолок
                    crossing_flag = True
                    if self.new_speed_y == 2:
                        self.new_speed_y = self.new_speed_y
                        self.velocity.y = 0
                        self.rect.top = platforms[i].rect.bottom
            # elif (platforms[i].rect.bottom - 4 <= self.rect.top <= platforms[i].rect.bottom + 4 and
            #           (platforms[i].rect.left < self.rect.right < platforms[i].rect.right or
            #            platforms[i].rect.left < self.rect.left < platforms[i].rect.right) and  -1 < self.new_speed_y < 0):
            #     # print('удар о потолок при низкой скорости')
            #     if self.new_speed_y < 0:  # Удар о потолок
            #         self.new_speed_y = - self.new_speed_y
            #         self.velocity.y = 0
            #         self.rect.top = platforms[i].rect.bottom
            # print(self.new_speed_y)
            # print(self.new_speed_y)
            # print((platforms[i].rect.bottom - 4 <= self.rect.top <= platforms[i].rect.bottom + 4 and (
            #             platforms[i].rect.left < self.rect.right < platforms[i].rect.right or platforms[
            #         i].rect.left < self.rect.left < platforms[i].rect.right)))

        # Вертикальное движение
        self.rect.y += self.velocity.y

        if not flag:
            self.on_ground = False

        # Ограничение по вертикали
        if self.rect.top < 0:  # Верхняя граница
            self.rect.top = 0
            self.velocity.y = 0
            self.new_speed_y = - self.new_speed_y
        if self.rect.bottom > screen_height:  # Нижняя граница
            self.rect.bottom = screen_height - 48
            self.hitting_the_floor_flag = True
            self.velocity.y = 0
            self.new_speed_y = 0
            self.on_ground = True

        crossing_flag = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect) and not crossing_flag:
                crossing_flag = True
                if (self.new_speed_x > 0 and
                        (platform.rect.top - 4 <= self.rect.top <= platform.rect.top + 4 or
                         platform.rect.top - 4 <= self.rect.bottom <= platform.rect.top + 4)):  # Движение вправо
                    # self.hitting_the_right_wall_flag = True
                    self.rect.right = platform.rect.left
                    self.new_speed_x = 0
                    self.velocity.x = 0
                elif (self.new_speed_x < 0 and
                      (platform.rect.top - 4 <= self.rect.top <= platform.rect.top + 4 or
                       platform.rect.top - 4 <= self.rect.bottom <= platform.rect.top + 4)):  # Движение влево
                    self.rect.left = platform.rect.right
                    self.new_speed_x = 0
                    self.velocity.x  = 0
                    # self.hitting_the_left_wall_flag = True

        # Ограничение по горизонтали
        if self.rect.left < 0:  # Левая граница
            self.rect.left = 0
            self.new_speed_x = abs(self.new_speed_x)
            self.velocity.x = 0
            self.hitting_the_left_wall_flag = True
        if self.rect.right > screen_width:  # Правая граница
            self.rect.right = screen_width
            self.new_speed_x = -abs(self.new_speed_x)
            self.velocity.x = 0
            self.hitting_the_right_wall_flag = True

    def update(self, screen_width, screen_height, platforms, move_flag=0, flag_stop=False):
        # print(self.on_ground)
        # print(self.new_speed_y)
        """Обновление состояния игрока"""
        if move_flag:
            self.move_flag = move_flag
        if flag_stop:
            self.flag_stop = flag_stop
            self.move_flag = 0
        self.clock.tick(self.fps)
        self.move(screen_width, screen_height, platforms)
        move_flag = False
        if not self.on_ground and self.new_speed_x == 0:
            self.apply_gravity()
            move_flag = True
        if not self.on_ground and self.new_speed_x != 0:
            self.boll_movie()
            move_flag = True
        if (self.move_flag == 2 and not flag_stop and self.on_ground) or self.hitting_the_left_wall_flag:
            self.flag_stop = False
            self.move_right()
            move_flag = True
        if (self.move_flag == 1 and not flag_stop and self.on_ground) or self.hitting_the_right_wall_flag:
            self.flag_stop = False
            self.move_left()
            move_flag = True
        if (self.flag_stop and self.on_ground) or not move_flag:
            self.stop()
            if self.new_speed_x == 0:
                self.flag_stop = False
        # print(self.velocity.x, self.velocity.y, self.new_speed_x, self.new_speed_y, self.on_ground)

    def apply_gravity(self):
        """Применение гравитации"""
        if self.new_speed_y == 0:
            self.flag = True
            self.hitting_the_right_wall_flag = False
            self.hitting_the_left_wall_flag = False
        if not self.on_ground:
            self.velocity.y += self.new_speed_y * 0.0125 + (self.g * 0.0125 ** 2) / 2
            self.new_speed_y += self.g * 0.0125

    def boll_movie(self):
        print(1)
        self.apply_gravity()
        if not self.hitting_the_right_wall_flag and not self.hitting_the_left_wall_flag:
            self.velocity.x += self.new_speed_x / 2 * 0.0125

    def jump(self):
        """Прыжок"""
        if self.on_ground:
            self.flag = False
            self.new_speed_y = -self.jump_speed
            self.on_ground = False
            self.hitting_the_floor_flag = False

    def move_left(self):
        """Движение влево"""
        if abs(self.new_speed_x - self.player_boost * 0.0125) <= self.max_speed_x:
            self.velocity.x += self.new_speed_x * 0.0125 - (self.player_boost * 0.0125 ** 2) / 2
            self.new_speed_x -= self.player_boost * 0.0125
        else:
            self.velocity.x += self.new_speed_x * 0.0125

    def move_right(self):
        """Движение вправо"""
        if self.new_speed_x + self.player_boost * 0.0125 <= self.max_speed_x:
            self.velocity.x += self.new_speed_x * 0.0125 + (self.player_boost * 0.0125 ** 2) / 2
            self.new_speed_x += self.player_boost * 0.0125
        else:
            self.velocity.x += self.new_speed_x * 0.0125

    def stop(self):
        """Остановка"""
        if self.new_speed_x != 0:
            if self.new_speed_x > 0:
                if self.new_speed_x - self.spop_boost * 0.0125 <= 0:
                    self.new_speed_x = 0
                    self.velocity.x = 0
                else:
                    self.velocity.x += self.new_speed_x * 0.0125 - (self.spop_boost * 0.0125 ** 2) / 2
                    self.new_speed_x -= self.spop_boost * 0.0125
            if self.new_speed_x < 0:
                if self.new_speed_x + self.spop_boost * 0.0125 >= 0:
                    self.new_speed_x = 0
                    self.velocity.x = 0
                else:
                    self.velocity.x += -self.new_speed_x * 0.0125 + (self.spop_boost * 0.0125 ** 2) / 2
                    self.new_speed_x += self.spop_boost * 0.0125
