import pygame
import os
from framework import scale_image

def load_image(filename, size=1):
    img = pygame.image.load(os.path.join(filename))
    return scale_image(img, size)
class Paralax:
    def __init__(self, screen):
        self.screen = screen
    bg1 = load_image("map/background/BG_1.png")
    bg2 = load_image("map/background/BG_2.png")
    bg3 = load_image("map/background/BG_3.png")
    bg1_lax = 4
    bg2_lax = 7
    bg3_lax = 12
    x = -800
    y = 0

    def draw(self, win, scroll):
        win.blit(self.bg3, (self.x - scroll[0]/self.bg3_lax, self.y - scroll[1]/self.bg3_lax))
        win.blit(self.bg2, (self.x - scroll[0]/self.bg2_lax, self.y - scroll[1]/self.bg2_lax))
        win.blit(self.bg1, (self.x - scroll[0]/self.bg1_lax, self.y - scroll[1]/self.bg1_lax))
