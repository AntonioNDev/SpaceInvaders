from turtle import distance
import pygame
import random
import math
import json
import threading
from pygame import font, mixer


#Game configurations
pygame.init()

#Window size
window = pygame.display.set_mode((700,700))
pygame.display.set_caption("Arcade shooting")
iconPath = pygame.image.load("images/icon.png")
pygame.display.set_icon(iconPath)



#Colors
white = (255,255,255)
red = (255, 0, 0)
blue = (0,0,255)
black = (0,0,0)

f = open('GameSettings.json')
data = json.load(f)
#Background music
""" mixer.music.load(data["Music"]["song"])
mixer.music.play(-1) """

backgroundImage = pygame.image.load(data["Background"]["image"])
alive_aliens = data["Enemies"]["NOE"]
#Main game class
class Game:
   #Game conf settings
   def __init__(self) -> None:
      pass
   #Conf for player
   def player(self,x,y):
      window.blit(pygame.image.load(data["Player"]["PlayerImage"]), (x,y))

   #Append enemies in the list
   def createEnemies():
      for _ in range(data["Enemies"]["NOE"]):
         data["Enemies"]["EnemyX"].append(int(random.randint(10,640) + 5))
         data["Enemies"]["EnemyY"].append(int(random.randint(10,150)))
         data["Enemies"]["EnemyX_moving_speed"].append(1)
         data["Enemies"]["EnemyY_moving_speed"].append(int(random.randint(10,35)))

         if len(data["Enemies"]["EnemyX"]) >= data["Enemies"]["NOE"]:
            break

   #Thread to call createEnemies
   x = threading.Thread(target=createEnemies, daemon=True)
   x.start()

   #Conf for enemy NOTE: Try to make every alien with their own image
   def enemy(self,x,y):
      image = pygame.image.load(data["Enemies"]["EnemiesImages"][0])
      window.blit(image, (x,y))

   #Conf for bullet
   def bullet(self,x,y):
      data["Bullet"]["Bullet_moving"] = "fired"
      window.blit(pygame.image.load(data["Bullet"]["BulletImage"]), (x+16,y+10))

   #Check if the bullet and enemy have collided 
   def isCollided(self,enemyX,enemyY,bulletX,bulletY):
      distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
      if distance < 27:
         return True
   #Conf for the score
   def score(self):
      font = pygame.font.Font(data["Score"]["font"], 40)
      score_text = font.render(f"Aliens alive {alive_aliens}", True, (white))
      window.blit(score_text, (data["Score"]["scoreX"], data["Score"]["scoreY"]))

   #Game over text
   def game_over(self):
      font = pygame.font.Font(data["GameOver"]["font"], 64)

      over_text = font.render("GAME OVER", True, (black))
      window.blit(over_text, (150,200))

   #Main function
   def main(self):
      global bulletX, alive_aliens
      bulletX = 0
      #while running is true the window will be displayed, else it will exit the game
      window_running = True
      
      while window_running:
         #fill the screen with black constantly
         window.fill((black))

         #Background image
         window.blit(backgroundImage,(0,0))
         self.score()
         #Loop through event keys
         for event in pygame.event.get():
            if event.type == pygame.QUIT:
               window_running = False

            #Moving keys
            if event.type == pygame.KEYDOWN:
               #IF left key is pressed then move left
               if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                  data["Player"]["PlayerX_moving_speed"] = -2
               #If right key is pressed move right
               if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                  data["Player"]["PlayerX_moving_speed"] = 2
               #If space is pressed then shoot:
               if event.key == pygame.K_SPACE:
                  if data["Bullet"]["Bullet_moving"] != "fired":
                     laser = mixer.Sound(data["Music"]["laserSound"])
                     laser.play()
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
         if data["Bullet"]["BulletY"] <= -50:
            data["Bullet"]["BulletY"] = 480
            data["Bullet"]["Bullet_moving"] = "ready"

         if data["Bullet"]["Bullet_moving"] == "fired":
            self.bullet(bulletX, data["Bullet"]["BulletY"])
            data["Bullet"]["BulletY"] -= data["Bullet"]["BulletY_moving_speed"]

         
         #Control enemies
         for x in range(data["Enemies"]["NOE"]):
            #Moving speed of the enemy
            data["Enemies"]["EnemyX"][x] += data["Enemies"]["EnemyX_moving_speed"][x]
            #Check if enemy is reaching the zero of X if yes then turn it back so it doesn't go behind the scene
            if data["Enemies"]["EnemyX"][x] <= 0:
               data["Enemies"]["EnemyX_moving_speed"][x] = random.randint(2,3)
               data["Enemies"]["EnemyY"][x] += data["Enemies"]["EnemyY_moving_speed"][x]
            elif data["Enemies"]["EnemyX"][x] >= 640:
               data["Enemies"]["EnemyX_moving_speed"][x] = int(f"-{random.randint(2,3)}")
               data["Enemies"]["EnemyY"][x] += data["Enemies"]["EnemyY_moving_speed"][x]

            #print(f"EnemyX:{data['Enemies']['EnemyX']}--EnemyY:{data['Enemies']['EnemyX'][x]} ---- BulletX:{data['Bullet']['BulletX']}--BulletY:{data['Bullet']['BulletY']}")
            kaboom = self.isCollided(data["Enemies"]["EnemyX"][x], data["Enemies"]["EnemyY"][x], bulletX, data["Bullet"]["BulletY"]) 
            
            #If the bullet hit the enemy then...
            if kaboom == True:
               data["Bullet"]["BulletY"] = 480
               data["Bullet"]["Bullet_moving"] = "ready" 
               explosion = mixer.Sound(data["Music"]["explosion"])
               explosion.play()
               data["Enemies"]["EnemyY"][x] = -1000
               data["Enemies"]["EnemyX_moving_speed"][x] = 0
               alive_aliens -= 1
               data["Score"]["score"] += 1

            #If the enemy come close to your Y then the game is over
            if data['Enemies']['EnemyY'][x] > 430:
               self.game_over()
               for j in range(data["Enemies"]["NOE"]):
                  data["Enemies"]["EnemyY"][j] = 1000
                  data["Enemies"]["EnemyX_moving_speed"][j] = 0
               data["Bullet"]["BulletY_moving_speed"] = 0
               data["Player"]["PlayerY"] = -1000
               data["Score"]["scoreX"] = 1000
               scoreF = font.Font(data["Score"]["font"], 32)
               score = scoreF.render(f"Score {data['Score']['score']} out of {data['Enemies']['NOE']}", True, (white))
               window.blit(score, (220,280))
              



            self.enemy(data["Enemies"]["EnemyX"][x],data["Enemies"]["EnemyY"][x])
      


         self.player(data["Player"]["PlayerX"], data["Player"]["PlayerY"])

         pygame.display.update()



start = Game()
start.main()

