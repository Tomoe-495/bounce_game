import pygame
from framework import move

class Bullet:
	def __init__(self, ball):
		self.x = ball.x
		self.y = ball.y
		self.size = 10
		self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
		self.color = (255, 255, 255)
		self.right = False
		self.left = False
		self.up = False
		self.down = False
	
	def draw(self, win, scroll):
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

	def event(self, event):
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_a:
				self.left = True
			if event.key == pygame.K_d:
				self.right = True
			if event.key == pygame.K_w:
				self.up = True
			if event.key == pygame.K_s:
				self.down = True
