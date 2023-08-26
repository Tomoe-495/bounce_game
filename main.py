import pygame
from framework import move
import sys

w, h = 1000, 450
W, H = w/10*8, h/10*8 
FPS = 60

pygame.init()
clock = pygame.time.Clock()

dis = pygame.display.set_mode((w, h), 0, 32)
win = pygame.Surface((W, H))
pygame.display.set_caption("ball movements")


def get_map(filename):
	with open(filename, 'r') as f:
		Map = f.read()
		return Map.split("\n")

class Tiles:
	def __init__(self):
		self.color = (255,255,255)
		self.w = 10
		self.size = 25
		self.map = get_map("map.txt")
		self.tiles = []
		self.scroll = [0, 0]
		self.surf = pygame.Surface((self.size * (len(self.map[0])), self.size * (len(self.map))))
		self.surf.set_colorkey((0, 0, 0))
		self.ball_pos = [0, 0]

		x = 0
		y = 0
		for line in self.map:
			for block in line:
				if block == "x":
					self.tiles.append(pygame.Rect(x, y, self.size, self.size))
					pygame.draw.rect(self.surf, self.color, (x, y, self.size, self.size))
				elif block == "o":
					self.ball_pos = [x, y]
				x += self.size
			y += self.size
			x = 0

	def draw(self):
		win.blit(self.surf, (0 - self.scroll[0], 0 - self.scroll[1]))
		# x = 0
		# y = 0
		# for line in self.map:
		# 	for block in line:
		# 		if block == "x":
		# 			pygame.draw.rect(win, self.color, (x - self.scroll[0], y - self.scroll[1], self.size, self.size))
		# 		x += self.size
		# 	y += self.size
		# 	x = 0
	
	def camera(self, ball):
		speed = 10
		self.scroll[0] += (ball.rect.x - self.scroll[0] - W/2) / speed
		self.scroll[1] += (ball.rect.y - self.scroll[1] - H/2) / speed


class Ball:
	def __init__(self, pos):
		self.x = pos[0]
		self.y = pos[1]
		self.size = 20
		self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
		self.color = (35, 35, 35)
		self.vel = 0
		self.acc = 0.3
		self.jump_limit = 1
		self.jump_count = 0
		self.jump_power = -8
		self.right = False
		self.left = False
		self.speed = 0
		self.max_speed = 4
		self.ACC = 0.3

	def draw(self, scroll):
		pygame.draw.circle(win, self.color, (self.rect.x + (self.rect.width/2) - scroll[0], self.rect.y + (self.rect.height/2) - scroll[1]), self.size/10*7, 0)
	
	def size_change(self, plus=True):
		if plus:
			self.size += 1
		else:
			self.size -= 1

		self.rect = pygame.Rect(self.rect.x, self.rect.y, self.size, self.size)

	def update(self, movement):
		if self.right:
			if self.speed < self.max_speed:
				self.speed += self.ACC
		else:
			if self.speed > 0:
				self.speed -= self.ACC/2

		if self.left:
			if self.speed > -self.max_speed:
				self.speed -= self.ACC
		else:
			if self.speed < 0:
				self.speed += self.ACC/2

		movement[0] += self.speed

		#		gravity
		self.vel += self.acc
		movement[1] += self.vel

	def jump(self):
		if self.jump_count < self.jump_limit:
			self.vel = self.jump_power
			self.jump_count += 1

	def platform(self, movement, tiles):
		self.rect, collisions = move(self.rect, movement, tiles)

		if collisions["bottom"]:
			self.jump_count = 0
			if self.vel > 2:
				self.vel = -self.vel/2
			else:
				self.vel = 0

		if collisions["left"] or collisions["right"]:
			self.speed = -self.speed/2

		if collisions["top"]:
			self.vel = 2


class Bullet:
	def __init__(self, ball):
		self.x = ball.rect.x
		self.y = ball.rect.y
		self.size = 10
		self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
		self.color = (255, 255, 255)
		self.right = False
		self.left = False
		self.up = False
		self.down = False
	
	def draw(self, scroll):
		pygame.draw.circle(win, self.color, (self.rect.x + (self.rect.width/2) - scroll[0], self.rect.y + (self.rect.height/2) - scroll[1]), self.size/2, 0)

	def update(self, mx, my, movement):
		speed = 30

		if self.right:
			movement[0] += speed
		elif self.left:
			movement[0] -= speed
		elif self.down:
			movement[1] += speed
		elif self.up:
			movement[1] -= speed
		else:
			if self.rect.x < mx:
				movement[0] += (mx - self.rect.x) / speed + 1
			elif self.rect.x > mx:
				movement[0] += (mx - self.rect.x) / speed
			if self.rect.y < my:
				movement[1] += (my - self.rect.y) / speed + 1
			elif self.rect.y > my:
				movement[1] += (my - self.rect.y) / speed

	def platform(self, movement, tiles):
		self.rect, collisions = move(self.rect, movement, tiles)

		if collisions["top"] or collisions["bottom"] or collisions["left"] or collisions["right"]:
			self.up, self.down, self.right, self.left = False, False, False, False
			self.color = (255, 0,0)
		else:
			self.color = (255, 255, 255)


def main():
	run = True

	tile = Tiles()
	ball = Ball(tile.ball_pos)
	bullet = Bullet(ball)

	def draw():
		win.fill((180, 30, 40))

		bullet.draw(tile.scroll)
		ball.draw(tile.scroll)
		tile.draw()

		surf = pygame.transform.scale(win, (w, h))
		dis.blit(surf, (0, 0))

		pygame.display.update()

	while run:
		clock.tick(FPS)

		draw()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP:
					ball.jump()
				if event.key == pygame.K_RIGHT:
					ball.right = True
				if event.key == pygame.K_LEFT:
					ball.left = True
				if event.key == pygame.K_ESCAPE:
					run = False
			
				if event.key == pygame.K_q:
					ball.size_change(False)
				if event.key == pygame.K_e:
					ball.size_change()

				
				if event.key == pygame.K_a:
					bullet.left = True
				if event.key == pygame.K_d:
					bullet.right = True
				if event.key == pygame.K_w:
					bullet.up = True
				if event.key == pygame.K_s:
					bullet.down = True

			if event.type == pygame.KEYUP:
				if event.key == pygame.K_RIGHT:
					ball.right = False
				if event.key == pygame.K_LEFT:
					ball.left = False

			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					mx, my = pygame.mouse.get_pos()
					ball.rect.x = mx
					ball.rect.y = my

		movement = [0, 0]
		move = [0, 0]

		tile.camera(ball)

		ball.update(movement)
		ball.platform(movement, tile.tiles)

		bullet.update(ball.rect.x, ball.rect.y, move)
		bullet.platform(move, tile.tiles)

	pygame.quit()	
	sys.exit()



if __name__ == "__main__":
	main()
