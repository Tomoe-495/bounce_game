import pygame
from framework import move
import sys
from tilemap import Tiles
from player import Ball
from bullet import Bullet

W, H = 1366, 768
FPS = 60

pygame.init()
clock = pygame.time.Clock()

scale = 0.50
w, h =  W * scale, H * scale

dis = pygame.display.set_mode((W, H), pygame.FULLSCREEN)
win = pygame.Surface((w, h))
pygame.display.set_caption("ball movements")


def main():
	run = True

	tile = Tiles((w, h))
	ball = Ball(tile.get_ball_pos())
	bullet = Bullet(ball.rect)

	def draw(win):
		win.fill((100, 244, 200))

		bullet.draw(win, tile.scroll)
		tile.draw(win, ball)

		surf = pygame.transform.scale(win, (W, H))
		dis.blit(surf, (0, 0))

		pygame.display.update()

	while run:
		clock.tick(FPS)

		draw(win)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			
			ball.event(event)
			bullet.event(event)

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					run = False
							
			# if event.type == pygame.MOUSEBUTTONDOWN:
			# 	if event.button == 1:
			# 		mx, my = pygame.mouse.get_pos()
			# 		ball.rect.x = mx
			# 		ball.rect.y = my

		movement = [0, 0]
		move = [0, 0]

		tile.camera(ball.rect)

		ball.update(movement)
		ball.platform(movement, tile.tiles)

		bullet.update(ball.rect.x, ball.rect.y, move)
		bullet.platform(move, tile.tiles)

	pygame.quit()	
	sys.exit()



if __name__ == "__main__":
	main()
