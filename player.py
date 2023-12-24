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
		self.color = (45, 45, 45)
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
		

	def draw(self, win, scroll):
		pygame.draw.circle(win, self.color, (self.rect.x + (self.rect.width/2) - scroll[0], self.rect.y + (self.rect.height/2) - scroll[1]), self.size*0.75)
		# pygame.draw.rect(win, (255, 255, 255), (self.rect.x  - scroll[0], self.rect.y  - scroll[1], self.rect.width, self.rect.height), 1)

	def update(self, movement):
		if self.right:
			# if self.speed < self.max_speed:
			# 	self.speed += self.ACC
			self.speed += self.ACC
			self.speed = min(self.speed, self.max_speed)
		elif self.left:
			# if self.speed > -self.max_speed:
			self.speed -= self.ACC
			self.speed = max(self.speed, -self.max_speed)
		elif not self.left and not self.right:
			if self.speed < 0:
				self.speed += self.ACC/2
				self.speed = min(0, self.speed)
			elif self.speed > 0:
				self.speed -= self.ACC/2
				self.speed = max(0, self.speed)

		# print(self.speed)
		
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
		self.rect, collisions, ramp = move(self.rect, movement, tiles)

		if collisions["bottom"]:
			self.jump_count = 0

			if ramp == "left":
				self.speed += self.vel/2
			elif ramp == "right":
				self.speed -= self.vel/2

			if self.vel > 2:
				self.vel = -self.vel/2
			else:
				self.vel = 0

		# if collisions["left"] or collisions["right"]:
		# 	self.speed = -self.speed/2

		if collisions["top"]:
			self.vel = 1
	
	def event(self, event):
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				self.jump()
			if event.key == pygame.K_RIGHT:
				self.right = True
			if event.key == pygame.K_LEFT:
				self.left = True

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_RIGHT:
				self.right = False
			if event.key == pygame.K_LEFT:
				self.left = False
