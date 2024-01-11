import pygame
from framework import load_image

class Sprite:
    def __init__(self, filename):
        self.sheet = load_image(filename)

    def get_sprite(self, pos, size):
        sprite = pygame.Surface((size, size))
        sprite.set_colorkey((0, 0, 0))
        sprite.blit(self.sheet, (0, 0), (pos[0], pos[1], size, size))
        return sprite
