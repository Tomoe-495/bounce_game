import pygame
from framework import move
import sys
from tilemap import Tiles
from player import Ball

w, h = 1000, 450
W, H = w/10*5, h/10*5
FPS = 60

pygame.init()
clock = pygame.time.Clock()

dis = pygame.display.set_mode((w, h), 0, 32)
win = pygame.Surface((W, H))
pygame.display.set_caption("ball movements")

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
		win.fill((144, 244, 200))

		bullet.draw(tile.scroll)
		tile.draw(win, ball)

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

		tile.camera(ball, [W, H])

		ball.update(movement)
		ball.platform(movement, tile.tiles)

		bullet.update(ball.rect.x, ball.rect.y, move)
		bullet.platform(move, tile.tiles)

	pygame.quit()	
	sys.exit()



if __name__ == "__main__":
	main()
