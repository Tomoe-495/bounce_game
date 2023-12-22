import json
import pygame

slide_speed = 1

def get_map(filename):
	with open(filename, 'r') as f:
		return json.load(f)
	
def scale_image(img, factor):
    size = round(img.get_width() * factor), round(img.get_height() * factor)
    return pygame.transform.scale(img, size)

def collision_test(rect, tiles):
	hit_list = []
	for tile in tiles:
		if rect.colliderect(tile[0]):
			hit_list.append(tile)
	return hit_list

def move(rect, movement, tiles):
	normal_tiles = [t for t in tiles if t[1] in [1, 4]]
	ramps = [t for t in tiles if t[1] in [2, 3]]
	collision_types = {"top": False, "bottom": False, "left": False, "right": False}
	rect.x += movement[0]
	hit_list = collision_test(rect, normal_tiles)
	for tile in hit_list:
		if movement[0] > 0 and tile[1] != 4:
			rect.right = tile[0].left
			collision_types["right"] = True
		if movement[0] < 0 and tile[1] != 4:
			rect.left = tile[0].right
			collision_types["left"] = True
	rect.y += movement[1]
	hit_list = collision_test(rect, normal_tiles)
	for tile in hit_list:
		if movement[1] > 0:
			rect.bottom = tile[0].top
			collision_types["bottom"] = True
		if movement[1] < 0 and tile[1] != 4:
			rect.top = tile[0].bottom
			collision_types["top"] = True

	ramp_col = ""
	for ramp in ramps:
		ramp_rect = ramp[0]
		ramp_side = ramp[1]
		if rect.colliderect(ramp_rect):
			rel_x = rect.x - ramp_rect.x
		
			# 2 = right, 3 = left
			if ramp_side == 2:
				pos_height = rel_x + rect.width
			elif ramp_side == 3:
				pos_height = ramp_rect.width - rel_x 

			pos_height = min(pos_height, ramp_rect.width)
			pos_height = max(pos_height, 0)

			target_y = ramp_rect.y + ramp_rect.width - pos_height

			if rect.bottom > target_y:
				rect.bottom = target_y

				if ramp_side == 3:
					rect.x += slide_speed
					ramp_col = "left"
				else:
					rect.x -= slide_speed
					ramp_col = "right"

				collision_types["bottom"] = True

	return rect, collision_types, ramp_col
