import csv
import pygame

TILE_SIZE = 32

def load_level(filename):
    tiles = []
    with open(filename, newline='') as file:
        reader = csv.reader(file)
        for y, row in enumerate(reader):
            for x, tile in enumerate(row):
                if tile == '1':  # 1 обозначает платформу
                    tiles.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
    return tiles

def draw_level(screen, tiles, tile_image):
    for tile in tiles:
        screen.blit(tile_image, tile.topleft)
