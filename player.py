import pygame
from framework import move, scale_image

class Ball:
	def __init__(self, pos):
		self.x = pos[0]
		self.y = pos[1]
		self.img = scale_image(pygame.image.load("img/ball.png"), 0.13)
		self.size = self.img.get_width()
		self.size = 17
		self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
		self.color = (35, 35, 35)
		self.vel = 0
		self.acc = 0.3
		self.jump_limit = 1
		self.jump_count = 0
		self.jump_power = -6
		self.right = False
		self.left = False
		self.speed = 0
		self.max_speed = 4
		self.ACC = 0.2
		self.rotate = 0

		self.surf = pygame.Surface((self.size, self.size))
		self.surf.set_colorkey((0, 0, 0))
		pygame.draw.circle(self.surf, self.color,
		     (0 + (self.surf.get_width()/2), 0 + self.surf.get_width()/2), self.surf.get_width()/2, 0)
		pygame.draw.circle(self.surf, (180, 50, 30), (7, 7), 2, 0)
		

	def draw(self, win, scroll):
		win.blit(pygame.transform.rotate(self.surf, self.rotate), (self.rect.x - scroll[0], self.rect.y - scroll[1]))
		# pygame.draw.circle(win, self.color, (self.rect.x + (self.rect.width/2) - scroll[0], self.rect.y + (self.rect.height/2) - scroll[1]), self.size/10*7, 0)
		# pygame.draw.rect(win, (255, 255, 255), (self.rect.x - scroll[0], self.rect.y - scroll[1], self.rect.width, self.rect.height), 1)
		# img = pygame.transform.rotate(self.img, self.rotate)
		# win.blit(img, 
	   	# 	(self.rect.x - scroll[0], self.rect.y - scroll[1])
	   	# )

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
		
		print(self.speed)

		self.rotate -= self.speed*2
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
