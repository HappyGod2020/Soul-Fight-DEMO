import pygame


class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, sprite_path="Sprite/coin_sprite.png"):
        super().__init__()
        self.image = pygame.image.load(sprite_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
