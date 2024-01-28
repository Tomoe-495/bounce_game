import pygame

class Pond:
    def __init__(self, points, width, height):
        self.acc = 0.8

        self.points = [ [i, points[1] + (16//2)] for i in range(points[0], points[0] + width, 10)]
        self.pos = self.points[0][1]

        self.surf = pygame.Surface((width, height+32))
        self.surf.set_colorkey((0, 0, 0))
        self.surf.set_alpha(100)
        self.surf_pos = ([points[0], points[1]-16])

        self.surf_points = [ [i, 24] for i in range(0, width, 10) ]
        self.surf_fix_pos = self.surf_points[0][1]

        self.surf_points += [
            [width,  height+16],
            [0,  height+16]
        ]


    def draw(self, win, scroll):

        self.surf.fill((0, 0, 0))
        pygame.draw.polygon(self.surf, (72, 178, 223), self.surf_points)
        win.blit(self.surf, (self.surf_pos[0] - scroll[0], self.surf_pos[1] - scroll[1]))

        point = list(map(lambda x: (x[0] - scroll[0], x[1] - scroll[1]), self.points))
        pygame.draw.lines(win, (92, 198, 223), False, point)
        # pygame.draw.polygon(win, (72, 178, 223), point)
        
    
    def update(self, ball):
        for i, point in enumerate(self.points):
            if ball.rect.collidepoint(point):
                self.points[i][1] += ball.vel*0.8
                self.surf_points[i][1] += ball.vel*0.8

    def rupple(self):

        for i, point in enumerate(self.points):
            if point[1] > self.pos:
                point[1] = max(self.pos, point[1] - self.acc)
            elif point[1] < self.pos:
                point[1] = min(self.pos, point[1] + self.acc)
                    
        for point in self.surf_points[0:-2]:
            if point[1] > self.surf_fix_pos:
                point[1] = max(self.surf_fix_pos, point[1] - self.acc)
            elif point[1] < self.surf_fix_pos:
                point[1] = min(self.surf_fix_pos, point[1] + self.acc)



class Water:
    def __init__(self, paths:list):
        self.paths = paths
        self.points = self.get_points()

    def get_points(self):
        points = []
        for path in self.paths:
            points.append(Pond(path["px"], path["width"], path["height"]))
        return points

    def draw(self, win, scroll):
        for point in self.points:
            point.draw(win, scroll)

    def update(self, ball):
        for point in self.points:
            point.update(ball)
            point.rupple()

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