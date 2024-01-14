import pygame

class Spring:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, 1, 1)
        self.vel = 0
        self.acc = 0
        self.bounce_amplitude = 0

    def update(self):
        self.rect.y += self.vel

        # Bouncing behavior
        if self.rect.y < self.y - self.bounce_amplitude:
            self.rect.y = self.y - self.bounce_amplitude
            self.vel = abs(self.vel)  # Reverse the velocity to bounce back
            self.bounce_amplitude = max(0, self.bounce_amplitude - 2)
        elif self.rect.y > self.y + self.bounce_amplitude:
            self.rect.y = self.y + self.bounce_amplitude
            self.vel = -abs(self.vel)  # Reverse the velocity to bounce back
            self.bounce_amplitude = max(0, self.bounce_amplitude - 2)

    def rupple(self, vel):
        self.vel = vel/2
        self.acc = vel*.25
        self.bounce_amplitude = 10 + vel

class Water:
    def __init__(self, paths:list):
        self.paths = paths
        self.points = self.get_points()

    def get_points(self):
        points = []
        for i in self.paths:
            y = i["px"][1] + (i["height"]//2)
            x = [i["px"][0], i["px"][0] + i["width"]]
            point = [Spring(j, y) for j in range(x[0], x[1], 5)]
            points.append(point)
        return points
    
    def draw(self, win, scroll):
        for point in self.points:
            pt = list(map(lambda x: (x.rect.x - scroll[0], x.rect.y - scroll[1]), point))
            # pygame.draw.polygon(win, (71, 151, 232), pt, width=1)
            pygame.draw.lines(win, (71, 151, 232), 0, pt, 1)
        
    def update(self, ball):
        for point_group in self.points:
            for i, pt in enumerate(point_group):
                pt.update()

                if ball.rect.colliderect(pt.rect):
                    pt.rupple(ball.vel)



''' ---- water object
{
    "__identifier": "Water",
    "__grid": [143,25],
    "__pivot": [0,0],
    "__tags": [],
    "__tile": null,
    "__smartColor": "#2CE8F5",
    "__worldX": 2272,
    "__worldY": 176,
    "iid": "4b800790-b0a0-11ee-917a-458cb6a9882f",
    "width": 224,
    "height": 16,
    "defUid": 105,
    "px": [2288,400],
    "fieldInstances": []
}
'''