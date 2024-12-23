import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, sprite_path):
        super().__init__()
        self.image = pygame.image.load(sprite_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))

        self.velocity_y = 0
        self.gravity = 0.1
        self.jump_speed = -5
        self.grounded = False

    def update(self, platforms):
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y

        self.grounded = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect) and self.velocity_y > 0:
                self.rect.bottom = platform.rect.top
                self.velocity_y = 0
                self.grounded = True

    def jump(self):
        if self.grounded:
            self.velocity_y = self.jump_speed
