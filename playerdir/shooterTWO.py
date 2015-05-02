#John F. Lake, Jr. & James Bowyer
#Final Project
#Shooter Platforming Game


#All we need is pygame and some math: 
import pygame
import math
import sys
from datetime import datetime
from twisted.internet.protocol import Factory
from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Protocol
from twisted.internet.task import LoopingCall
from twisted.internet import reactor

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

class Bullet(pygame.sprite.Sprite):
	def __init__(self,gs=None,posX=0,posY=0,fac=0):
		#Initialize the sprite, sound, and images:
		gs.bullet = self
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("laser.png")
		self.rect = self.image.get_rect()
		self.rect = self.rect.move(posX,posY)

		#Laser movement: 
		self.location = self.rect
		self.velX = 7
		if fac:
			self.velX = -7
	def tick(self):
		self.rect = self.rect.move(self.velX,0)
		#code to kill bullet once off screen ... syntax not working
		if (self.rect.right > 1000 or self.rect.left < -1000 or self.rect.top > 1000 or self.rect.bottom < -1000):
			self.kill()


#Player class: 
class Player(pygame.sprite.Sprite):
	def __init__(self,gs=None):
		#Initialize the sprite, sound, and images:
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("images/redBlock2.png")
		self.gs = gs
		self.rect = self.image.get_rect()
		self.rect = self.rect.move(20,SCREEN_HEIGHT-self.rect.h)
		self.facing = 0
		self.left = 0
		self.right = 0
		self.up = 0
		self.down = 0

		#Location/velocity of the death star:
		self.location = self.rect
		self.gravity = 1
		self.velX = 0
		self.velY = 0
	def jump(self):
		self.velY = -20

	def containWithinBorder(self):
		l = self.rect
		if l.x <= 0:
			l.x = 0
		if l.y <= 0:
			l.y = 0
		if l.y >= SCREEN_HEIGHT-self.rect.h:
			l.y = SCREEN_HEIGHT-self.rect.h
		if l.x >= SCREEN_WIDTH-self.rect.w:
			l.x = SCREEN_WIDTH-self.rect.w
			

	#Tick (alters movement and rotates the player)
	def tick(self):
		#User input: 
		for event in pygame.event.get():
			#If you press a key, move in that direction
			if event.type is pygame.KEYDOWN:
				if event.key == pygame.K_LEFT or event.key == pygame.K_a:
					self.left = 1
					self.facing = 1
				elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
					self.right = 1
					self.facing = 0
				elif event.key == pygame.K_UP or event.key == pygame.K_w:
					self.up = 1
				elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
					self.down = 1
				elif event.key == pygame.K_SPACE:
					self.jump()
				elif event.key == pygame.K_c:
					gs.bullet_list.append(Bullet(self.gs,self.rect.x,self.rect.y,self.facing))
			#if you let up on a key in a direction, stop motion in that direction: 
			elif event.type is pygame.KEYUP:
				if event.key == pygame.K_LEFT or event.key == pygame.K_a:
					self.left = 0
				elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
					self.right = 0
				elif event.key == pygame.K_UP or event.key == pygame.K_w:
					self.up = 0
				elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
					self.down = 0
			elif event.type is pygame.MOUSEBUTTONDOWN:
				gs.bullet_list.append(Bullet(self.gs,self.rect.x,self.rect.y,self.facing))
			elif event.type is pygame.QUIT:
				pygame.quit()
				sys.exit(0)


		#Determine the velocity: 
		self.velX = 0
		if self.left:
			self.velX = -5
		elif self.right:
			self.velX = 5
		

		#Account for gravity: 
		self.velY = self.velY + self.gravity
		self.rect = self.rect.move(self.velX,self.velY)
		self.containWithinBorder()
		#TODO: Platform detection

			

				

#Main game class: 
class GameSpace:
	def main(self):
		#Initialize everything:
		pygame.init()
		pygame.mixer.init()

		self.size = self.width,self.height=800,800
		self.black = 0,0,0
		self.screen = pygame.display.set_mode(self.size)
		self.clock = pygame.time.Clock()
		self.player = Player(self)
		self.bullet_list = []




		#Main game loop;
	def pygame_interior(self):

		self.clock.tick(60)
		self.player.tick()
		#self.bullet.tick()
		for bullet in self.bullet_list:
			bullet.tick()
		self.screen.fill(self.black)
		self.screen.blit(self.player.image,self.player.rect)
		for bullet in self.bullet_list:
			self.screen.blit(bullet.image, bullet.rect)
		pygame.display.flip()




#Run the game 
if __name__ == '__main__':
	gs = GameSpace()
	gs.main()
	FPS = 45
	lc = LoopingCall(gs.pygame_interior)
	lc.start(1/FPS)
	reactor.run()
