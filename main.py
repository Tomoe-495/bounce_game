import pygame
import sys
from tilemap import Tiles
from player import Ball
from paralax import Paralax

W, H = 1000, 600
FPS = 60

pygame.init()
clock = pygame.time.Clock()

scale = 0.40
w, h =  W * scale, H * scale

dis = pygame.display.set_mode((W, H), 0, 32)
pygame.display.set_caption("ball movements")

def scale_screen(tilemap, up=True):
	global scale
	scale = scale + 0.01 if up else scale - 0.01
	w, h = W*scale, H*scale
	tilemap.screen = (w, h)
	return pygame.Surface((w, h))

def main():
	run = True

	tile = Tiles((w, h))
	ball = Ball(tile.get_ball_pos())
	paralax = Paralax((w, h))

	win = pygame.Surface((w, h))

	def draw(win):
		win.fill((155, 212, 245))

		paralax.draw(win, tile.scroll)
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

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					run = False

				if event.key == pygame.K_e:
					win = scale_screen(tile)
				elif event.key == pygame.K_q:
					win = scale_screen(tile, up=False)
							
			# if event.type == pygame.MOUSEBUTTONDOWN:
			# 	if event.button == 1:
			# 		mx, my = pygame.mouse.get_pos()
			# 		ball.rect.x = mx
			# 		ball.rect.y = my
					
		movement = [0, 0]

		tile.camera(ball.rect)

		ball.update(movement)
		ball.platform(movement, tile.tiles)

	pygame.quit()	
	sys.exit()



if __name__ == "__main__":
	main()
