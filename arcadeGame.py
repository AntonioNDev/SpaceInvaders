import pygame
import random
import math
import json
from pygame import font, mixer


#Game configurations
pygame.init()

#Window size
window = pygame.display.set_mode((700,700))
pygame.display.set_caption("Space invaders")
iconPath = pygame.image.load("Images/icon.png")
pygame.display.set_icon(iconPath)
pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])


#Colors
white = (255,255,255)
red = (255, 0, 0)
blue = (0,0,255)
black = (0,0,0)

with open("GameSettings.json") as data:
   data = json.load(data)

#Background music
""" mixer.music.load(data["Music"]["song"])
mixer.music.play(-1) """

backgroundImage = pygame.image.load(data["Background"]["image"]).convert()
FPS = 60

#Main game class
class Game:
   #Game conf settings
   def __init__(self) -> None:
      self.isMenuOpen = True
      self.window_running = True
      self.isGameOver = False
      self.aliens_alive = data["Enemies"]["NOE"]

   #Conf for player
   def player(self,x,y):
      window.blit(pygame.image.load(data["Player"]["PlayerImage"]).convert_alpha(), (x,y))

   #Add enemies in the list
   def createEnemies(self):
      images = ["Images/alien1.png", "Images/alien2.png", "Images/alien3.png", "Images/alien4.png"]
      for _ in range(data["Enemies"]["NOE"]):
         data["Enemies"]["EnemyX"].append(int(random.randint(10,640) + 5))
         data["Enemies"]["EnemyY"].append(int(random.randint(-100,-30)))
         data["Enemies"]["EnemyY_moving_speed"].append(0.7)
         data["Enemies"]["EnemiesImages"].append(images[random.randint(0,3)])

         if len(data["Enemies"]["EnemyX"]) >= data["Enemies"]["NOE"]:
            break

   #Conf for enemy 
   def enemy(self,x,y,i):
      image = pygame.image.load(data["Enemies"]["EnemiesImages"][i]).convert_alpha()
      window.blit(image, (x,y))

   #Conf for bullet
   def bullet(self,x,y):
      data["Bullet"]["Bullet_moving"] = "fired"
      bulletImg = pygame.image.load(data["Bullet"]["BulletImage"]).convert_alpha()
      window.blit(bulletImg, (x+16,y+10))

   #Check if the bullet and enemy have collided 
   def isCollided(self,enemyX,enemyY,bulletX,bulletY):
      distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
      if distance < 27:
         return True
         
   #Conf for the score
   def score(self):
      font = pygame.font.Font(data["Fonts"]["arcade"], 35)
      score_text = font.render(f"Aliens alive: {self.aliens_alive}", True, (white))
      window.blit(score_text, (data["Score"]["scoreX"], data["Score"]["scoreY"]))

   #Game over text
   def game_over(self):
      #Mouse pos
      mouse_pos = pygame.mouse.get_pos()

      #GameOver title
      gameover = pygame.font.Font(data["Fonts"]["gameplay"], 64)
      over_text = gameover.render("GAME OVER", True, (white))

      #Display the score
      scoreF = font.Font(data["Fonts"]["arcade"], 32)
      score = scoreF.render(f"Score {data['Score']['score']} out of {data['Enemies']['NOE']}", True, (white))

      #Restart button image
      restart_btn = pygame.image.load("images/restart.png").convert_alpha()

      if pygame.mouse.get_pressed()[0] == 1:
         if mouse_pos[0] >= 312 and mouse_pos[0] <= 369 and mouse_pos[1] >= 253 and mouse_pos[1] <= 309:
            self.isGameOver = False
            data["Score"]["score"] = 0
            self.main()

      window.blit(restart_btn, (310, 250))
      window.blit(over_text, (150,100))
      window.blit(score, (220,180))

   #Remove enemies
   def removeEnemy(self):
      data["Enemies"]["EnemyX"].clear()
      data["Enemies"]["EnemyY"].clear()
      data["Enemies"]["EnemyX_moving_speed"].clear()
      data["Enemies"]["EnemyY_moving_speed"].clear()
      
   #Start menu
   def startMenu(self):
      #Mouse position
      mouse_position = pygame.mouse.get_pos()

      #Title 
      title = pygame.font.Font(data["Fonts"]["arcade_n"], 44)
      title_text = title.render("Space Invaders", True, (white))

      #start and exit images
      start_image = pygame.image.load("images/start_btn.png").convert_alpha()
      exit_image = pygame.image.load("images/exit_btn.png").convert_alpha()

      #Resize image
      start_image = pygame.transform.scale(start_image, (130, 60))   
      exit_image = pygame.transform.scale(exit_image, (130, 60))   

      #start and exit buttons reactangles
      start_rect = start_image.get_rect()
      start_rect_pos = (270,300)

      exit_rect = exit_image.get_rect()
      exit_rect_pos = (270,390)

      if pygame.mouse.get_pressed()[0] == 1:
         if mouse_position[0] >= 272 and mouse_position[0] <= 397 and mouse_position[1] >= 302 and mouse_position[1] <= 353:
            self.isMenuOpen = False

         if mouse_position[0] >= 271 and mouse_position[0] <= 397 and mouse_position[1] >= 392 and mouse_position[1] <= 443:
            self.window_running = False
      

      window.blit(start_image, start_rect_pos)
      window.blit(exit_image, exit_rect_pos)
      window.blit(title_text, (57,100))

   #SHOW FPS FOR DEBUGGING
   def showFps(self, fps):
      fpsFont = pygame.font.Font(data["Fonts"]["arcade_n"], 10)
      fps_text = fpsFont.render(f"FPS: {int(fps)}", True, (white))

      window.blit(fps_text, (10,10))

   #Main function
   def main(self):
      global bulletX, alive_aliens
      
      bulletX = 0
      clock = pygame.time.Clock()

      self.createEnemies()

      #while window_running == True, the game will run, else it will be closed
      while self.window_running:
         #FPS
         clock.tick(FPS)
         #fill the screen with black constantly
         window.fill((black))

         #Background image
         window.blit(backgroundImage,(0,0))
         self.score()

         #Loop through event keys
         for event in pygame.event.get():
            if event.type == pygame.QUIT:
               self.window_running = False

            #Moving keys
            if event.type == pygame.KEYDOWN:

               #IF left key is pressed then move left
               if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                  data["Player"]["PlayerX_moving_speed"] = -7

               #If right key is pressed move right
               if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                  data["Player"]["PlayerX_moving_speed"] = 7

               #If space is pressed then shoot:
               if event.key == pygame.K_SPACE:
                  if data["Bullet"]["Bullet_moving"] != "fired" and self.isGameOver != True and self.isMenuOpen != True:
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

         #Set borders so the player can't go outside of the window
         if data["Player"]["PlayerX"] <= 0:
            data["Player"]["PlayerX"] = 0

         elif data["Player"]["PlayerX"] >= 640:
            data["Player"]["PlayerX"] = 640

         #Check if bullet reach the top if yes then return it back to the plane
         if data["Bullet"]["BulletY"] <= -50:
            data["Bullet"]["BulletY"] = 480
            data["Bullet"]["Bullet_moving"] = "ready"

         if data["Bullet"]["Bullet_moving"] == "fired":
            self.bullet(bulletX, data["Bullet"]["BulletY"])
            data["Bullet"]["BulletY"] -= data["Bullet"]["BulletY_moving_speed"]

         if self.isMenuOpen != True:
            #Control enemies
            for x in range(data["Enemies"]["NOE"]):
               #check if it's game over if yes then stop the looping [reduce using of cpu]
               if self.isGameOver != True:
                  #Moving speed of the enemy
                  data["Enemies"]["EnemyY"][x] += data["Enemies"]["EnemyY_moving_speed"][x]

                  #If enemy Y is > than 435 then it's game over
                  if data["Enemies"]["EnemyY"][x] != 435:
                     data["Enemies"]["EnemyY"][x] += data["Enemies"]["EnemyY_moving_speed"][x]

                  kaboom = self.isCollided(data["Enemies"]["EnemyX"][x], data["Enemies"]["EnemyY"][x], bulletX, data["Bullet"]["BulletY"]) 
                  
                  data["Player"]["PlayerY"] = 510
                  data["Score"]["scoreX"] = 10

                  #NOTE: REMOVE ENEMY AFTER HITTING
                  if kaboom == True:
                     data["Bullet"]["BulletY"] = 480
                     data["Bullet"]["Bullet_moving"] = "ready" 

                     #explosion sound when the bullet hit enemy
                     explosion = mixer.Sound(data["Music"]["explosion"])
                     explosion.play()

                     data["Enemies"]["EnemyY"][x] = -1000
                     data["Enemies"]["EnemyY_moving_speed"][x] = 0
                     print(data["Enemies"])
                     self.aliens_alive -= 1
                     data["Score"]["score"] += 1

                  #If the enemy come close to player Y then the game is over
                  if data['Enemies']['EnemyY'][x] > 430:
                     self.isGameOver = True                  
                  self.enemy(data["Enemies"]["EnemyX"][x],data["Enemies"]["EnemyY"][x], x)

               else:
                  self.game_over()

                  data["Bullet"]["BulletX"] = 900
                  data["Player"]["PlayerY"] = 900
                  data["Score"]["scoreX"] = 900
                  self.aliens_alive = data["Enemies"]["NOE"]
                  self.removeEnemy()
                  break
         else:
            self.startMenu()
            data["Bullet"]["BulletX"] = 900
            data["Player"]["PlayerY"] = 900
            data["Score"]["scoreX"] = 900
      
         self.showFps(clock.get_fps())
         self.player(data["Player"]["PlayerX"], data["Player"]["PlayerY"])
         pygame.display.flip()


start = Game()
start.main()

