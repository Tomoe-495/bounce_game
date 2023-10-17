import pygame
from framework import get_map
from spritesheet import Sprite

def get_obj(map, obj):
	map = map["levels"][0]["layerInstances"]
	for id in map:
		if id["__identifier"] == obj:
			return id
		
def get_tile_layer(map, layer, size):
	map = get_obj(map, layer)
	sprite = Sprite("map/map.png")
	surf = pygame.Surface((size * map["__cWid"], size * map["__cHei"]))
	surf.set_colorkey((0, 0, 0))
	# incoming data format
	# { "px": [0,0], "src": [64,64], "f": 0, "t": 132, "d": [0] },
	for tile in map["gridTiles"]:
		s = sprite.get_sprite(tile["src"], size)
		surf.blit(pygame.transform.flip(s, tile["f"], 0), (tile["px"][0], tile["px"][1]))

	return surf


class Tiles:
	def __init__(self):
		self.color = (255,255,255)
		self.tiles = []
		self.scroll = [0, 0]
		
		map = get_map("map/map.ldtk")

		pos = get_obj(map, "Player")["entityInstances"][0]
		self.ball_pos = pos["px"]
		
		csv_map = get_obj(map, "Grid_set")
		self.size = csv_map["__gridSize"]

		self.layer1 = get_tile_layer(map, "Tiles", self.size)
		self.layer2 = get_tile_layer(map, "Trees", self.size)
		self.layer3 = get_tile_layer(map, 'Assets', self.size)
		self.layer4 = get_tile_layer(map, "Background", self.size)

		x = 0
		y = 0
		for block in csv_map["intGridCsv"]:
			if block == 1:
				self.tiles.append(pygame.Rect(x, y, self.size, self.size))
	
			x += self.size

			if x == csv_map["__cWid"] * self.size:
				y += self.size
				x = 0

	def draw(self, win, ball):
		win.blit(self.layer4, (0 - self.scroll[0], 0 - self.scroll[1]))
		win.blit(self.layer2, (0 - self.scroll[0], 0 - self.scroll[1]))
		ball.draw(win, self.scroll)
		win.blit(self.layer3, (0 - self.scroll[0], 0 - self.scroll[1]))
		win.blit(self.layer1, (0 - self.scroll[0], 0 - self.scroll[1]))
	
	def camera(self, ball, screen_size):
		speed = 10
		self.scroll[0] += (ball.rect.x - self.scroll[0] - screen_size[0]/2) / speed
		self.scroll[1] += (ball.rect.y - self.scroll[1] - (screen_size[1]/10)*5) / speed
