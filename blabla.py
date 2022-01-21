import pygame
import random
import math

pygame.init()

screen = pygame.display.set_mode((800,600))

pygame.display.set_caption("Test")

PlayerX = 370
PlayerY = 480
PlayerX_change = 0
playerImg = pygame.image.load("avionce.png")


enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
enemyImg = []
num_of_enemies = 7



for i in range(num_of_enemies):
   enemyX.append(random.randint(10, 400))
   enemyY.append(50)
   enemyX_change.append(0.5)
   enemyY_change.append(15)
   enemyImg.append(pygame.image.load("enemy.png"))

bulletX = 0
bulletY = 480
bulletY_change = 0.8
bullet_state = "ready"
bulletImg = pygame.image.load("pogolemBullet.png")


score_val = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX, textY = 10, 10

over_font = pygame.font.Font('freesansbold.ttf', 64)

def game_over():
   over_text = over_font.render("GAME OVER", True, (255,255,255))
   screen.blit(over_text, (200,250))


def player234234(x,y):
   screen.blit(playerImg, (x, y))


def enemy(x,y,i):
   screen.blit(enemyImg[i], (x, y))


def bullet(x,y):
   global bullet_state

   bullet_state = "fired" 
   screen.blit(bulletImg, (x+8, y+10))

def isColladed(enemyX, enemyY, bulletX, bulletY):
   distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
   if distance < 20:
      return True

def score(x,y):
   score = font.render(f"Score: {str(score_val)}", True, (255,255,255))
   screen.blit(score, (x,y))


running = True
while running:

   screen.fill((0))
   for event in pygame.event.get():
      if event.type == pygame.QUIT:
         running = False

      if event.type == pygame.KEYDOWN:
         if event.key == pygame.K_LEFT:
            PlayerX_change = -0.7
         if event.key == pygame.K_RIGHT:
            PlayerX_change = 0.7
         if event.key == pygame.K_SPACE:
            if bullet_state != "fired":
               bulletX = PlayerX
               bullet(bulletX, bulletY)

      if event.type == pygame.KEYUP:
         if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
            PlayerX_change = 0



   PlayerX += PlayerX_change

   if PlayerX <= 0:
      PlayerX = 0
   elif PlayerX >= 770:
      PlayerX = 770

   for i in range(num_of_enemies):

      if enemyY[i] > 400:
         for j in range(num_of_enemies):
            enemyY[j] = 2000
         game_over()
         break

      enemyX[i] += enemyX_change[i]
      if enemyX[i] <= 0:
         enemyX_change[i] = 0.3
         enemyY[i] += enemyY_change[i]
      elif enemyX[i] >= 765:
         enemyX_change[i] = -0.3
         enemyY[i] += enemyY_change[i]

      collision = isColladed(enemyX[i], enemyY[i], bulletX, bulletY)
      if collision:
         bulletY = 480
         bullet_state = "ready"
         score_val += 1
      
      enemy(enemyX[i], enemyY[i], i)


   if bulletY <= 0:
      bulletY = 480 
      bullet_state = "ready"

   if bullet_state == "fired":
      bullet(bulletX, bulletY)
      bulletY -= bulletY_change

   
 """   player(PlayerX, PlayerY)
   score(textX, textY)
   pygame.display.update()    """