import pygame
import random
import math

#Game configurations
pygame.init()
#Window size
window = pygame.display.set_mode((700,700))
pygame.display.set_caption("Arcade shooting")
iconPath = pygame.image.load("images/icon.png")
pygame.display.set_icon(iconPath)


#Game images paths
background = pygame.image.load("images/background.png")
planeImage = pygame.image.load("images/plane.png")
aliensImages = ["images/alien1.png", "images/alien2.png", "images/alien3.png"]
bulletImage = pygame.image.load("images/bullet.png")

#Colors
white = (255,255,255)
red = (255, 0, 0)
blue = (0,0,255)
black = (0,0,0)

#Main game class
class Game:
   #Conf for player
   def player(self,x,y):
      pass

   #Conf for enemy
   def enemy(self, x,y,i):
      pass

   #Conf for bullet
   def bullet(self,x,y):
      pass

   #Check if the bullet and enemy have collided 
   def isCollided(self,enemyX,enemyY,bulletX,bulletY):
      pass

   #Conf for the score
   def score(textX, textY):
      pass

   #Game over text
   def game_over(self):
      pass

#Main function
def main():
   #while running is true the window will be displayed, else it will exit the game
   window_running = True
   
   while window_running:
      #fill the screen with black constantly
      window.fill((black))

      #Background image DA SE POPRAVI!
      #window.blit(background,(0,0))
      #Loop through event keys
      for event in pygame.event.get():
         if event.type == pygame.QUIT:
            window_running = False

         #Moving keys
         if event.type == pygame.KEYDOWN:
            #IF left key is pressed then move left
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
               pass
            #If right key is pressed move right
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
               pass
            #If space is pressed then shoot:
            if event.key == pygame.K_SPACE:
               pass

         #check if the key is released
         if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
               pass
         




main()
pygame.display.update()
