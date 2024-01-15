import json
import pygame
import pygame
import configparser
import os

config = configparser.ConfigParser();
config.read("config.ini")

def get_config(attri:str, sect="General") -> str|int:
	val = config.get(sect, attri)
	try:
		return int(val)
	except ValueError as e:
		return val

def add_on(attri:str, sect:str="General"):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if get_config(attri):
                return func(*args, **kwargs)
        return wrapper
    return decorator

def color_change(surface, color):
	w, h = surface.get_size()
	r, g, b, _ = color
	surface = surface.copy()
	for x in range(w):
		for y in range(h):
			a = surface.get_at((x, y))[3]
			surface.set_at((x, y), pygame.Color(r, g, b, a))
	return surface

def get_map(filename):
	with open(filename, 'r') as f:
		return json.load(f)

def scale_image(img, factor):
    size = round(img.get_width() * factor), round(img.get_height() * factor)
    return pygame.transform.scale(img, size)

def load_image(filename, size=1):
    img = pygame.image.load(os.path.join(filename))
    if size == 1:
        return img
    return scale_image(img, size)

def collision_test(rect, tiles):
	hit_list = []
	for tile in tiles:
		if rect.colliderect(tile):
			hit_list.append(tile)
	return hit_list

def move(rect, movement, tiles, slide_speed=1):
	normal_tiles = list(map(lambda x: x[0], [t for t in tiles if t[1] == 1]))
	ramps = [t for t in tiles if t[1] in [2, 3]]

	collision_types = {"top": False, "bottom": False, "left": False, "right": False}

	rect.x += movement[0]
	hit_list = collision_test(rect, normal_tiles)
	for tile in hit_list:
		if movement[0] > 0:
			rect.right = tile.left
			collision_types["right"] = True
		elif movement[0] < 0:
			rect.left = tile.right
			collision_types["left"] = True
	rect.y += movement[1]
	hit_list = collision_test(rect, normal_tiles)
	for tile in hit_list:
		if movement[1] > 0:
			rect.bottom = tile.top
			collision_types["bottom"] = True
		elif movement[1] < 0:
			rect.top = tile.bottom
			collision_types["top"] = True

	ramp_col = ""
	for ramp in ramps:
		ramp_rect = ramp[0]
		ramp_side = ramp[1]
		if rect.colliderect(ramp_rect):
			rel_x = rect.x - ramp_rect.x

			# 2 = right, 3 = left
			if ramp_side == 2:
				pos_height = rel_x + rect.height
				ramp_col = "right"
				rect.x -= slide_speed
			elif ramp_side == 3:
				pos_height = ramp_rect.height - rel_x 
				ramp_col = "left"
				rect.x += slide_speed

			pos_height = min(pos_height, ramp_rect.height)
			pos_height = max(pos_height, 0)

			target_y = ramp_rect.y + ramp_rect.height - pos_height

			if rect.top > target_y:
				collision_types["top"] = True
				if(rect.left < ramp_rect.right):
					rect.left = ramp_rect.right
					collision_types["left"] = True
				ramp_col = ""
				return rect, collision_types, ramp_col

			if rect.bottom > target_y:
				rect.bottom = target_y

				collision_types["bottom"] = True

	return rect, collision_types, ramp_col
