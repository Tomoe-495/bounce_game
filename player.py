import pygame
from framework import move

class Ball:
	def __init__(self, pos):
		self.x = pos[0]
		self.y = pos[1]
		# self.img = scale_image(pygame.image.load("img/ball.png"), 0.13)
		# self.size = self.img.get_width()
		self.size = 15
		self.rect = pygame.Rect(self.x, self.y, self.size+1, self.size+1)
		self.color = "#EF3838"

		self.vel = 0
		self.acc = 0.3

		self.right = None
		self.left = None
		self.speed = 0
		self.max_speed = 4
		self.ACC = 0.2

		self.jump_limit = 1
		self.jump_count = 0
		self.jump_power = -6

		self.draw_size = self.size * 0.75

	def draw(self, win, scroll):
		pygame.draw.circle(win, self.color, (self.rect.x + (self.rect.width/2) - scroll[0], self.rect.y + (self.rect.height/2) - scroll[1]), self.draw_size)
		# pygame.draw.rect(win, (255, 255, 255), (self.rect.x  - scroll[0], self.rect.y  - scroll[1], self.rect.width, self.rect.height), 1)

	def update(self, movement):
		if self.right:
			self.speed = min(self.max_speed, self.speed + self.ACC)

		elif self.left:
			self.speed = max(-self.max_speed, self.speed - self.ACC)

		elif not self.left and not self.right:
			if self.speed < 0:
				self.speed = min(0, self.speed + (self.ACC/2))
			elif self.speed > 0:
				self.speed = max(0, self.speed - (self.ACC/2))

		# moving in X velocity
		movement[0] += self.speed

		#		gravity - Y velocity
		self.vel += self.acc
		movement[1] += self.vel

	def jump(self):
		if self.jump_count < self.jump_limit:
			self.vel = self.jump_power
			self.jump_count += 1

	def platform(self, movement, tiles):
		self.rect, collisions, ramp = move(self.rect, movement, tiles)

		if collisions["bottom"]:
			self.jump_count = 0

			if ramp == "left":
				self.speed += self.vel/2
			elif ramp == "right":
				self.speed -= self.vel/2

			if self.vel > 2:
				self.vel = -self.vel/2
			elif self.vel < 2:
				self.vel = 0
	
		elif collisions["top"]:
			self.vel = 1

		if (collisions["left"] or collisions["right"]) and ramp == "":
			self.speed = -self.speed/2

	
	def event(self, event):
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_w:
				self.jump()
			if event.key == pygame.K_d:
				self.right = True
			if event.key == pygame.K_a:
				self.left = True

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_d:
				self.right = False
			if event.key == pygame.K_a:
				self.left = False
