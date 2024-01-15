import pygame

class Pond:
    def __init__(self, points:list):
        self.points = points


class Water:
    def __init__(self, paths:list):
        self.paths = paths
        self.points = self.get_points()

    def get_points(self):
        points = []
        for path in self.paths:
            pts = [(i, path["px"][1] + (path["height"]//2)) for i in range(path["px"][0], path["px"][0] + path["width"], 2)]
            points.append(pts)
        return points

    def draw(self, win, scroll):
        for point in self.points:
            pts = list(map(lambda x: (x[0] - scroll[0], x[1] - scroll[1]), point))
            pygame.draw.lines(win, (72, 178, 223), 0, pts)

    def update(self, ball):
        pass

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