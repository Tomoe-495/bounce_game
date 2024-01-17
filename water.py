import pygame

class Pond:
    def __init__(self, points:list, height=64):
        self.points = points
        self.pos = self.points[0][1]
        self.acc = 1

    def draw(self, win, scroll):
        point = list(map(lambda x: (x[0] - scroll[0], x[1] - scroll[1]), self.points))
        # pygame.draw.lines(win, (72, 178, 223), False, point)
        pygame.draw.polygon(win, (72, 178, 223, 100), point)
    
    def update(self, ball):
        for i, point in enumerate(self.points):
            if ball.rect.collidepoint(point):
                self.points[i][1] += ball.vel*0.8

    def rupple(self):
        for i, point in enumerate(self.points):
            if point[1] > self.pos:
                # point[1] -= self.acc
                point[1] = max(self.pos, point[1] - self.acc)
            elif point[1] < self.pos:
                # point[1] += self.acc
                point[1] = min(self.pos, point[1] + self.acc)



class Water:
    def __init__(self, paths:list):
        self.paths = paths
        self.points = self.get_points()

    def get_points(self):
        points = []
        for path in self.paths:
            pts = [[i, path["px"][1] + (16//2)] for i in range(path["px"][0], path["px"][0] + path["width"], 8)]
            points.append(Pond(pts))
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