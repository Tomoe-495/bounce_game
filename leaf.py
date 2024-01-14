from framework import color_change, load_image, add_on
import pygame
import random
from counter import count

leaves = []

img = load_image("sprites/leaf.png")

colors = [
    img,
    color_change(img, (42, 180, 0, 255)),
    color_change(img, (41, 95, 72, 255)),
    color_change(img, (17, 130, 59, 255))
]


class Leaf:
    def __init__(self, map_size, img, wind):
        self.map_size = map_size
        self.x = random.randint(0, self.map_size[0])
        self.y = random.randint(-70, -10)

        self.img = img

        self.side = random.randint(0, 1)
        # True = Left
        # False = Right

        self.wind = wind
        self.angle = 45 if self.side else -45

        self.velocity = [
            self.wind.pressure if self.side else -self.wind.pressure/2,
            0.6
        ]

        self.speed = [
            self.velocity[0],
            self.velocity[1]
        ]

        self.acc = [0.1, 0.01]
        self.slow = False
        self.count = 0

    
    def draw(self, win, scroll):
        win.blit(pygame.transform.rotate(self.img, self.angle), (self.x - scroll[0] - (self.img.get_width()/2), self.y - scroll[1] - (self.img.get_height()/2)))

        self.x -= self.speed[0]
        self.y += self.speed[1]

        if self.side:
            self.angle = min(45, self.angle + 0.5)
        else:
            self.angle = max(-45, self.angle - 0.5)

        if self.count >= 120:
            if self.wind.pressure > 0.8:
                self.side = True
            elif self.wind.pressure < 0.8:
                rand = random.randint(0, 1)
                if rand != self.side:
                    self.side = rand
                    self.slow = True
            self.count = 0

        self.velocity[0] = self.wind.pressure if self.side else -self.wind.pressure*0.35

        if self.speed[0] < self.velocity[0]:
            self.speed[0] = min(self.velocity[0], self.speed[0] + self.acc[0])
        elif self.speed[0] > self.velocity[0]:
            self.speed[0] = max(self.velocity[0], self.speed[0] - self.acc[0])

        if self.speed[1] < self.velocity[1] and not self.slow:
            self.speed[1] = min(self.velocity[1], self.speed[1] + self.acc[1])
        elif self.slow:
            self.speed[1] = max(0.2, self.speed[1] - 0.03)
            if self.speed[1] == 0.2:
                self.slow = False

        self.count += 1

@add_on("leaf")
def updating_leaves(map_size, wind):
    if count.count%10 == 0 and random.random() < 0.8:
        leaves.append(Leaf(map_size, random.choice(colors), wind))
