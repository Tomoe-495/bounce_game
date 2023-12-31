from PIL import Image, ImageDraw, ImageFilter
import random

def get_cloud(width=1000, height=600, num_clouds=50, opacity=(10, 180)):
    # Create a new RGBA image with a transparent background
    image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    edge = 100
    # Generate random foggy clouds
    for _ in range(num_clouds):
        cloud_radius = random.randint(70, 100)
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
    image = image.filter(ImageFilter.GaussianBlur(radius=30))

    # Save the resulting image
    # image.save("cloud_image.png", "PNG")
    return image

# using pillow generated image in pygme

# foggy_cloud_image = generate_foggy_cloud(width, height, num_clouds)

# pygame_surface = pygame.image.fromstring(
    # foggy_cloud_image.tobytes(), foggy_cloud_image.size, "RGBA"
# )

class Fog:
    def __init__(self, screen):
        self.screen = screen
