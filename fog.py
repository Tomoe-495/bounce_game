from PIL import Image, ImageDraw, ImageFilter
import random
import pygame
from framework import get_config
from counter import count

def get_cloud(width=1000, height=600, num_clouds=random.randint(30, 40), opacity=(40, 100)):
    # Create a new RGBA image with a transparent background

    image = Image.new("RGBA", (width, height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)

    edge = 50
    # Generate random foggy clouds
    for _ in range(num_clouds):
        cloud_radius = random.randint(25, 40)
        cloud_x = random.randint(edge, width - edge)
        cloud_y = random.randint(edge, height - edge)

        # Draw the cloud on the image with a random opacity
        cloud_color = (255, 255, 255, random.randint(opacity[0], opacity[1]))
        draw.ellipse(
            (
                cloud_x - cloud_radius,
                cloud_y - cloud_radius*0.60,
                cloud_x + cloud_radius*0.75,
                cloud_y + cloud_radius,
            ),
            fill=cloud_color,
        )

    # Apply a blur filter to the image to make it look foggy
    image = image.filter(ImageFilter.GaussianBlur(radius=7))

    return image

'''     ----    using pillow generated image in pygme
foggy_cloud_image = generate_foggy_cloud(width, height, num_clouds)

pygame_surface = pygame.image.fromstring(
    # foggy_cloud_image.tobytes(), foggy_cloud_image.size, "RGBA"
)
'''

class Fog:
    def __init__(self, screen:tuple, scroll:list, back:bool=True):
        self.screen = screen
        self.scroll = scroll

        self.opacity = (60, 120) if back else (60, 80)

        self.fog = get_cloud(width=self.screen[0], height=self.screen[1], opacity=self.opacity)
        self.fog = pygame.image.fromstring(self.fog.tobytes(), self.fog.size, "RGBA")

        self.x = random.randint(self.screen[0] + self.scroll[0], self.screen[0] + 500 + self.scroll[0])
        self.y = random.randint(-int(self.fog.get_height()*0.30), self.screen[1] - int(self.fog.get_height()*0.10))

    def draw(self, win, scroll, wind_pressure):
        win.blit(self.fog, (self.x - scroll[0], self.y - scroll[1]))

        self.x -= wind_pressure*0.7


back_fogs = []
fore_fogs = []


def fog_updating(screen, scroll):

    if get_config("fog"):
        if count.count%180 == 0:
            if random.random() < 0.1:
                rand = random.random()
                if rand > 0.5:
                    back_fogs.append(Fog(screen, scroll))
                elif rand < 0.5:
                    fore_fogs.append(Fog(screen, scroll, back=False))

if get_config("fog"):
    for i in range(0, 3):
        rand = random.random()
        if rand < 0.5:
            back_fogs.append(Fog((400, 240), [0, 0]))
        elif rand > 0.5:
            fore_fogs.append(Fog((400, 240), [0, 0], back=False))
