import pygame
from core.settings import GUI_SETTINGS


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, sprite_path="Sprite/idle.png"):
        super().__init__()
        self.move_flag = 0
        self.height = height
        self.height_screen = GUI_SETTINGS.HEIGHT
        self.width_screen = GUI_SETTINGS.WIDTH
        self.flag_stop = False
        self.image = pygame.image.load(sprite_path).convert_alpha()
        self.walk_igame = [pygame.image.load(f'Sprite/Walk00{str(i).zfill(2)}.png') for i in range(1, 13)]
        self.death_igame = [pygame.image.load(f'Sprite/death{i}.png') for i in range(1, 8)]
        self.walk_igame += [pygame.image.load("Sprite/idle.png")]
        self.image = pygame.transform.scale(self.image, (width, height))
        self.width = width
        self.rect = self.image.get_rect(topleft=(x, y))
        self.death_flag = False
        self.back_flag = False
        self.image_index = 0
        self.velocity = pygame.math.Vector2(0, 0)
        self.max_speed_x = 5  # Скорость движения по горизонтали
        self.new_speed_x = 0
        self.last_speed_x = []
        self.new_speed_y = 0
        self.count_coin = 0
        self.death_image_index = 0
        self.button_render_flag = 0
        self.player_boost = 100
        self.spop_boost = 600
        self.speed = 5
        self.g = 40
        self.flag = True
        self.hitting_the_left_wall_flag = False
        self.hitting_the_right_wall_flag = False
        self.render_flag = False
        self.hitting_the_floor_flag = False
        self.render_platforms_close_flag = 0
        self.render_player_flag = 1
        self.jump_speed = 17
        self.on_ground = False
        self.on_button = False
        self.crossing_flag = False
        self.clock = pygame.time.Clock()
        self.fps = 80

    def respawn(self, x, y):
        """Респавн игрока в начальной позиции."""
        self.rect.topleft = (x, y)
        self.back_flag = False
        self.new_speed_x = 0
        self.new_speed_y = 0
        self.hitting_the_left_wall_flag = False
        self.hitting_the_floor_flag = False
        self.hitting_the_right_wall_flag = False
        self.velocity = pygame.math.Vector2(0, 0)  # Сбрасываем вектор
        self.image = pygame.transform.scale(self.walk_igame[12], (self.width, self.height))
        self.death_image_index = 0
        self.death_flag = False
        self.image_index = 0

    def move(self, screen_width, screen_height, platforms, buttons):
        """Перемещение игрока с учётом границ экрана и столкновений"""
        # Горизонтальное движение
        self.rect.x += self.velocity.x
        flag = False
        crossing_flag = False
        for i in range(len(platforms)):
            if (((platforms[i].rect.bottom >= self.rect.bottom >= platforms[i].rect.top and
                    (platforms[i].rect.left < self.rect.right < platforms[i].rect.right or
                     platforms[i].rect.left < self.rect.left < platforms[i].rect.right) and self.new_speed_y >= 1)) or
                    self.hitting_the_floor_flag and
                    platforms[i].rect.y - 4 <= self.rect.y + 48 <= platforms[i].rect.y + 4 and
                    (platforms[i].rect.left < self.rect.right < platforms[i].rect.right or
                     platforms[i].rect.left < self.rect.left < platforms[i].rect.right)):
                if self.new_speed_y > 0:  # Падение вниз
                    self.rect.bottom = platforms[i].rect.top
                    self.on_ground = True
                    flag = True
                    self.velocity.y = 0
                    self.velocity.x = 0
                    self.new_speed_y = 0
                else:
                    self.rect.bottom = platforms[i].rect.top
                    self.on_ground = True
                    flag = True
                    self.velocity.y = 0
                    self.new_speed_y = 0
                    self.velocity.x = 0
            elif (platforms[i].rect.bottom >= self.rect.top >= platforms[i].rect.top and
                  (platforms[i].rect.left < self.rect.right < platforms[i].rect.right or
                   platforms[i].rect.left < self.rect.left < platforms[i].rect.right)) and self.new_speed_y < 0:
                crossing_flag = True
                if self.new_speed_y < 0:  # Удар о потолок
                    self.rect.top = platforms[i].rect.bottom
                    self.velocity.y = 0
                    self.new_speed_y = - self.new_speed_y
            elif (platforms[i].rect.y - 4 <= self.rect.y + 48 <= platforms[i].rect.y + 4 and
                    (platforms[i].rect.left < self.rect.right < platforms[i].rect.right or
                     platforms[i].rect.left < self.rect.left < platforms[i].rect.right) and 0 < self.new_speed_y < 1):
                if self.new_speed_y > 0:  # Падение вниз
                    self.on_ground = True
                    flag = True
                else:
                    self.on_ground = True
                    flag = True
            elif (platforms[i].rect.bottom > self.rect.top > platforms[i].rect.top and
                      (platforms[i].rect.left < self.rect.right < platforms[i].rect.right or
                       platforms[i].rect.left < self.rect.left < platforms[i].rect.right)): # Удар о потолок
                crossing_flag = True
                self.new_speed_y = -self.new_speed_y
                self.velocity.y = 0
                self.rect.top = platforms[i].rect.bottom
        if not (GUI_SETTINGS.WIDTH / 32 * 16 <= self.rect.right <= GUI_SETTINGS.WIDTH / 32 * 19 and GUI_SETTINGS.HEIGHT / 18 * 3.5 <= self.rect.bottom <= GUI_SETTINGS.HEIGHT / 18 * 4.5):
            for platform in platforms:
                if self.rect.colliderect(platform.rect) and not crossing_flag:
                    if (self.new_speed_x > 0 and
                            (platform.rect.bottom >= self.rect.top >= platform.rect.top or
                             platform.rect.bottom >= self.rect.bottom >= platform.rect.top)):  # Движение вправо
                        crossing_flag = True
                        self.rect.right = platform.rect.left
                        self.new_speed_x = -abs(self.new_speed_x)
                        self.hitting_the_right_wall_flag = True
                        self.velocity.x = 0
                    elif (self.new_speed_x < 0 and
                          (platform.rect.bottom >= self.rect.top >= platform.rect.top or
                           platform.rect.bottom >= self.rect.bottom >= platform.rect.top)):  # Движение влево
                        crossing_flag = True
                        self.rect.left = platform.rect.right
                        self.velocity.x = 0
                        self.new_speed_x = abs(self.new_speed_x)
                        self.hitting_the_left_wall_flag = True

        for button in buttons:
            if (button.rect.top - 4 <= self.rect.bottom <= button.rect.bottom + 4 and
                    ((self.rect.right >= button.rect.left >= self.rect.left) or
                     (self.rect.left <= button.rect.right <= self.rect.right))):
                if self.rect.bottom <= button.rect.bottom:
                    self.on_button = True

        # Вертикальное движение
        self.rect.y += self.velocity.y

        if not flag:
            self.on_ground = False

        # Ограничение по вертикали
        if self.rect.top < 0:  # Верхняя граница
            self.rect.top = 0
            self.velocity.y = 0
            self.new_speed_y = 4
        if self.rect.bottom > screen_height:  # Нижняя граница
            self.rect.bottom = screen_height - 48
            self.hitting_the_floor_flag = True
            self.velocity.y = 0
            self.new_speed_y = 0
            self.on_ground = True

        # Ограничение по горизонтали
        if self.rect.left < 0:  # Левая граница
            self.rect.left = 0
            if abs(self.new_speed_y) >= 1:
                self.new_speed_x = abs(self.new_speed_x)
                self.hitting_the_left_wall_flag = True
            self.velocity.x = 0
        if self.rect.right > screen_width:  # Правая граница
            self.rect.right = screen_width
            if abs(self.new_speed_y) >= 1:
                self.new_speed_x = -abs(self.new_speed_x)
                self.hitting_the_right_wall_flag = True
            self.velocity.x = 0

    def update(self, screen_width, screen_height, platforms, platform_close, buttons, count_coin, move_flag=0, flag_stop=False):
        self.plaform_close = platform_close
        self.clock.tick(self.fps)
        if self.death_flag:
            self.death_render()
        else:
            self.render_button(buttons, platforms)
            if self.render_flag == 3:
                self.render_player()
            if self.render_flag == 3:
                self.render_flag = 0
            else:
                self.render_flag += 1
            self.count_coin = count_coin
            if len(self.last_speed_x) < 5:
                self.last_speed_x.append(self.new_speed_x)
            else:
                self.last_speed_x.append(self.new_speed_x)
                self.last_speed_x = self.last_speed_x[1:]
            """Обновление состояния игрока"""
            if move_flag:
                self.move_flag = move_flag
            if flag_stop:
                self.flag_stop = flag_stop
                self.move_flag = 0
            self.move(screen_width, screen_height, platforms, buttons)
            k = screen_height / 576
            self.render_platforms_close(k, screen_height)
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

    def render_button(self, buttons, platforms):
        if self.button_render_flag == 3:
            if self.on_button:
                if buttons[0].rect.bottom < self.height_screen / 18 * 5.2:
                    for platform in platforms:
                        if (platform.rect.left in (self.width_screen / 32 * 16,
                                                  self.width_screen / 32 * 17, self.width_screen / 32 * 18)
                                and platform.rect.top < self.height_screen / 18 * 5):
                            if platform.rect.bottom + 1 > self.height_screen / 18 * 5.2:
                                platform.rect.bottom = self.height_screen / 18 * 5.2
                            else:
                                platform.rect.y += 1
                    for button in buttons:
                        if button.rect.bottom + 1 > self.height_screen / 18 * 5.2:
                            button.rect.bottom = self.height_screen / 18 * 5.2
                            # self.rect.y = self.height_screen / 18 * 5.5
                        else:
                            button.rect.y += 1
                    self.rect.y += 1
            else:
                if buttons[0].rect.top > self.height_screen / 18 * 4:
                    for button in buttons:
                        if button.rect.top - 1 < self.height_screen / 18 * 4:
                            button.rect.top = self.height_screen / 18 * 4
                        else:
                            button.rect.y -= 1
                    for platform in platforms:
                        if (platform.rect.left in (self.width_screen / 32 * 16,
                                                  self.width_screen / 32 * 17, self.width_screen / 32 * 18)
                                and platform.rect.top < self.height_screen / 18 * 5):
                            if platform.rect.top - 1 < self.height_screen / 18 * 4:
                                platform.rect.top = self.height_screen / 18 * 4
                            else:
                                platform.rect.y -= 1
        if self.button_render_flag == 3:
            self.button_render_flag = 0
        else:
            self.button_render_flag += 1

    def render_player(self):
        if self.new_speed_x > 0:
            if abs(self.new_speed_y) <= 0.5:
                if self.image_index < 11:
                    self.image_index += 1
                else:
                    self.image_index = 0
                self.image = pygame.transform.scale(self.walk_igame[self.image_index], (self.width, self.height))
        elif self.new_speed_x < 0:
            if abs(self.new_speed_y) <= 0.5:
                if self.image_index < 11:
                    self.image_index += 1
                else:
                    self.image_index = 0
                self.image = pygame.transform.scale(pygame.transform.flip(self.walk_igame[self.image_index], True, False), (self.width, self.height))
        else:
            self.image = pygame.transform.scale(self.walk_igame[12], (self.width, self.height))

    def death_render(self):
        pygame.time.delay(35)
        if self.render_player_flag == 5:
            if self.new_speed_x <= 0:
                if self.death_image_index != 6:
                    self.image = pygame.transform.scale(self.death_igame[self.death_image_index], (self.width * 1.8, self.height * 1.8))
                else:
                    self.image = pygame.transform.scale(self.death_igame[self.death_image_index],
                                                        (self.width, self.height))
            else:
                if self.death_image_index != 6:
                    self.image = pygame.transform.scale(pygame.transform.flip(self.death_igame[self.death_image_index], True, False), (self.width * 1.8, self.height * 1.8))
                else:
                    self.image = pygame.transform.scale(
                        pygame.transform.flip(self.death_igame[self.death_image_index], True, False),
                        (self.width, self.height))
            if self.death_image_index == 6:
                pygame.time.delay(100)
                self.death_flag = False
                self.back_flag = True
                self.death_image_index = 0
            else:
                self.death_image_index += 1
        else:
            if self.render_player_flag < 5:
                self.render_player_flag += 1
            else:
                self.render_player_flag = 0

    def render_platforms_close(self, k, screen_height):
        if self.on_button or (not (self.level_index - 1)):
            if self.level_index == 4:
                if self.on_button and self.count_coin == 9:
                    if self.plaform_close[0].rect.top > 0:
                        for platform in self.plaform_close:
                            platform.rect.y -= k / 2
            else:
                if self.plaform_close[0].rect.top > 0:
                    for platform in self.plaform_close:
                        platform.rect.y -= k / 2
        else:
            if self.level_index == 3:
                if not self.render_platforms_close_flag:
                    if self.plaform_close[-1].rect.bottom < screen_height / 18 * 5:
                        for platform in self.plaform_close:
                            platform.rect.y += k / 2
                    else:
                        self.plaform_close[0].rect.bottom = screen_height / 18 * 3
        if self.render_platforms_close_flag < 6:
            self.render_platforms_close_flag += 1
        else:
            self.render_platforms_close_flag = 0

    def level(self, index):
        self.level_index = index
        self.count_coin = 0

    def apply_gravity(self):
        """Применение гравитации"""
        self.on_button = False
        if self.new_speed_y == 0:
            self.flag = True
            self.hitting_the_right_wall_flag = False
            self.hitting_the_left_wall_flag = False
        if not self.on_ground:
            if self.new_speed_y != 30:
                self.velocity.y += self.new_speed_y * 0.0125 + (self.g * 0.0125 ** 2) / 2
            else:
                self.velocity.y += self.new_speed_y * 0.0125
            if self.new_speed_y + self.g * 0.0125 <= 33.5:
                self.new_speed_y += self.g * 0.0125
            else:
                self.new_speed_y = 30

    def boll_movie(self):
        self.on_button = False
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
