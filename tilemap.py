import pygame
from framework import get_map
from spritesheet import Sprite

def get_obj(map, obj):
	map = map["levels"][0]["layerInstances"]
	for id in map:
		if id["__identifier"] == obj:
			return id
		
def get_tile_layer(map, layer, size, sprite):
	map = get_obj(map, layer)
	surf = pygame.Surface((size * map["__cWid"], size * map["__cHei"]))
	surf.set_colorkey((0, 0, 0))
	# incoming data format
	# { "px": [0,0], "src": [64,64], "f": 0, "t": 132, "d": [0] },
	for tile in map["gridTiles"]:
		s = sprite.get_sprite(tile["src"], size)
		surf.blit(pygame.transform.flip(s, tile["f"], 0), (tile["px"][0], tile["px"][1]))

	return surf


class Tiles:
	def __init__(self, screen:tuple):
		self.tiles = []
		self.scroll = [0, 0]
		self.screen = screen
		
		self.map = get_map("map/swamp.ldtk")
		self.sprite = Sprite("map/Terrain_and_Props.png")

		self.csv_map = get_obj(self.map, "Grid_set")
		self.size = self.csv_map["__gridSize"]

		self.layerTiles = get_tile_layer(self.map, "Tiles", self.size, self.sprite)

		x = 0
		y = 0
		for block in self.csv_map["intGridCsv"]:
			if block != 0:
				self.tiles.append(pygame.Rect(x, y, self.size, self.size))
	
			x += self.size

			if x == self.csv_map["__cWid"] * self.size:
				y += self.size
				x = 0

	scroll_speed = 10

	def get_ball_pos(self):
		pos = get_obj(self.map, "Player")["entityInstances"][0]
		return pos["px"]

	def draw(self, win, ball):
		self.scroll[0] = 0 if self.scroll[0] < 0 else self.scroll[0]
		self.scroll[1] = 0 if self.scroll[1] < 0 else self.scroll[1]

		ball.draw(win, self.scroll)
		win.blit(self.layerTiles, (0 - self.scroll[0], 0 - self.scroll[1]))
	
	def camera(self, ball):
		self.scroll[0] += ( ball.x - self.scroll[0] - self.screen[0]/2 ) / self.scroll_speed
		self.scroll[1] += ( ball.y - self.scroll[1] - self.screen[1]*0.6 ) / self.scroll_speed
