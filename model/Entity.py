import pygame


class Entity(pygame.Rect):
    name: str

    hp: int
    stamina: int

    attack: int
    armor: int

    inventory: list
    level: int

    sprite: pygame.Surface

    def __init__(self,
                 name="Zero",
                 hp=1,
                 stamina=1,
                 attack=1,
                 armor=1,
                 inventory=[],
                 level=1,
                 sprite="",
                 x=0,
                 y=0,
                 width=64,
                 height=64,):
        self.name = name
        self.hp = hp
        self.stamina = stamina
        self.attack = attack
        self.armor = armor
        self.inventory = inventory
        self.level = level
        # self.load_sprite(sprite)
        super().__init__(x, y, width, height)

    def load_sprite(self, path_img):
        self.sprite = pygame.image.load(path_img)

