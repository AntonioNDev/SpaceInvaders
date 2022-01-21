import pygame
import random
import math
import json

#Game configurations
pygame.init()

#Window size
window = pygame.display.set_mode((700,700))
pygame.display.set_caption("Arcade shooting")
iconPath = pygame.image.load("images/icon.png")
pygame.display.set_icon(iconPath)


#Game images paths
background = pygame.image.load("images/background.png")
bulletImage = pygame.image.load("images/bullet.png")

#Colors
white = (255,255,255)
red = (255, 0, 0)
blue = (0,0,255)
black = (0,0,0)

f = open('GameSettings.json')
data = json.load(f)

#Main game class
class Game:
   #Game conf settings
   def __init__(self) -> None:
      pass
   #Conf for player
   def player(self,x,y):
      window.blit(pygame.image.load(data["Player"]["PlayerImage"]), (x,y))

   #Conf for enemy
   def enemy(self, x,y,i):
      pass

   #Conf for bullet
   def bullet(self,x,y):
      data["Bullet"]["Bullet_moving"] = "fired"
      window.blit(pygame.image.load(data["Bullet"]["BulletImage"]), (x+16,y+10))

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
   def main(self):
      global bulletX
      bulletX = 0
      #while running is true the window will be displayed, else it will exit the game
      window_running = True
      
      while window_running:
         #fill the screen with black constantly
         window.fill((black))

         #Background image
         window.blit(background,(0,0))

         #Loop through event keys
         for event in pygame.event.get():
            if event.type == pygame.QUIT:
               window_running = False

            #Moving keys
            if event.type == pygame.KEYDOWN:
               #IF left key is pressed then move left
               if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                  data["Player"]["PlayerX_moving_speed"] = -0.9
               #If right key is pressed move right
               if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                  data["Player"]["PlayerX_moving_speed"] = 0.9
               #If space is pressed then shoot:
               if event.key == pygame.K_SPACE:
                  if data["Bullet"]["Bullet_moving"] != "fired":
                     bulletX = data["Player"]["PlayerX"]
                     self.bullet(bulletX, data["Bullet"]["BulletY"])
            #check if the key is released
            if event.type == pygame.KEYUP:
               if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_a or event.key == pygame.K_d:
                  data["Player"]["PlayerX_moving_speed"] = 0

            
         #Move it right or left         
         data["Player"]["PlayerX"] += data["Player"]["PlayerX_moving_speed"]

         #Check if it goes biond the window borders
         if data["Player"]["PlayerX"] <= 0:
            data["Player"]["PlayerX"] = 0
         elif data["Player"]["PlayerX"] >= 640:
            data["Player"]["PlayerX"] = 640

         #Check if bullet reach the top if yes then return
         if data["Bullet"]["BulletY"] <= 0:
            data["Bullet"]["BulletY"] = 480
            data["Bullet"]["Bullet_moving"] = "ready"

         if data["Bullet"]["Bullet_moving"] == "fired":
            self.bullet(bulletX, data["Bullet"]["BulletY"])
            data["Bullet"]["BulletY"] -= data["Bullet"]["BulletY_moving_speed"]


         self.player(data["Player"]["PlayerX"], data["Player"]["PlayerY"])
         pygame.display.update()

start = Game()
start.main()
