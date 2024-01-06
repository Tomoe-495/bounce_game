import pygame
from framework import get_map
from spritesheet import Sprite
from fog import back_fogs, fore_fogs

def get_obj(map, obj):
	map = map["levels"][0]["layerInstances"]
	for id in map:
		if id["__identifier"] == obj:
			return id
		
def map_screen(map, layer, size) -> tuple:
	map = get_obj(map, layer)
	screen = (size * map["__cWid"], size * map["__cHei"])
	return screen
		
def get_tile_layer(map, layer, size, sprite):
	map = get_obj(map, layer)
	surf = pygame.Surface((size * map["__cWid"], size * map["__cHei"]))
	surf.set_colorkey((0, 0, 0))
	# incoming data format
	# { "px": [0,0], "src": [64,64], "f": 0, "t": 132, "d": [0] },
	for tile in map["gridTiles"]:
		s = sprite.get_sprite(tile["src"], size)
		surf.blit(pygame.transform.flip(s, tile["f"], 0), tile['px'])

	return surf

def fog_draw(win, scroll, fogs, wind_pressure):
	for fog in fogs:
		fog.draw(win, scroll, wind_pressure)
		if fog.x + fog.fog.get_width() < 0:
			fogs.remove(fog)


class Tiles:
	def __init__(self, screen:tuple, wind):
		self.tiles = []
		self.scroll = [0, 0]
		self.screen = screen

		self.wind = wind
		
		self.map = get_map("map/swamp.ldtk")
		self.sprite = Sprite("map/Terrain_and_Props.png")

		self.csv_map = get_obj(self.map, "Grid_set")
		self.size = self.csv_map["__gridSize"]
		self.map_screen = map_screen(self.map, "Tiles", self.size)

		self.layerTiles = get_tile_layer(self.map, "Tiles", self.size, self.sprite)
		self.layerAssets = get_tile_layer(self.map, "Assets", self.size, self.sprite)
		self.layerWater = get_tile_layer(self.map, "Water", self.size, self.sprite)
		self.layerBackground = get_tile_layer(self.map, "Background", self.size, self.sprite)


		x = 0
		y = 0
		for block in self.csv_map["intGridCsv"]:
			if block != 0:
				self.tiles.append([pygame.Rect(x, y, self.size, self.size), block])
	
			x += self.size

			if x == self.csv_map["__cWid"] * self.size:
				y += self.size
				x = 0

	scroll_speed = 10

	def get_ball_pos(self):
		return get_obj(self.map, "Player")["entityInstances"][0]["px"]

	def draw(self, win, ball):

		win.blit(self.layerBackground, (0 - self.scroll[0], 0 - self.scroll[1]))

		#  background fogs
		fog_draw(win, self.scroll, back_fogs, self.wind.pressure)

		ball.draw(win, self.scroll)
		
		win.blit(self.layerWater, (0 - self.scroll[0], 0 - self.scroll[1]))
		win.blit(self.layerAssets, (0 - self.scroll[0], 0 - self.scroll[1]))
		win.blit(self.layerTiles, (0 - self.scroll[0], 0 - self.scroll[1]))

		# foreground fog
		fog_draw(win, self.scroll, fore_fogs, self.wind.pressure)
		
		# for tile in self.tiles:
		# 	pygame.draw.rect(win, (255, 255, 255), (tile[0].x - self.scroll[0], tile[0].y - self.scroll[1], tile[0].width, tile[0].height), 1)
	
	def camera(self, ball):
		self.scroll[0] += ( ball.x - self.scroll[0] - self.screen[0]/2 ) / self.scroll_speed
		self.scroll[1] += ( ball.y - self.scroll[1] - self.screen[1]*0.6 ) / self.scroll_speed

		self.scroll[0] = int(max(0, min(self.scroll[0], self.map_screen[0] - self.screen[0])));
		self.scroll[1] = int(max(0, min(self.scroll[1], self.map_screen[1] - self.screen[1])));

		# print(self.scroll, len(back_fogs), len(fore_fogs))
