import pygame
import random
import math
from pygame import mixer
import os

#Initialize pygame
pygame.init()

#Creating a screen, in bracket is the screen size
screen = pygame.display.set_mode((800,600))

#Background
base_path = os.path.dirname(__file__)
background_path = os.path.join(base_path, "background.png")
background = pygame.image.load(background_path)

#Background sound
base_path = os.path.dirname(__file__)
background_music_path = os.path.join(base_path, "background.wav")
mixer.music.load(background_music_path)
mixer.music.play(-1)

#Title and icon
pygame.display.set_caption("Alien Invaders")
base_path = os.path.dirname(__file__)
icon_path = os.path.join(base_path, "alien.png")
icon = pygame.image.load(icon_path)
pygame.display.set_icon(icon)

#Player image
base_path = os.path.dirname(__file__)
player_path = os.path.join(base_path, "spaceship.png")
playerImg = pygame.image.load(player_path)
playerX = 470
playerY = 470
playerX_change = 0

#Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 10

for i in range(num_of_enemies):
    base_path = os.path.dirname(__file__)
    enemy_path = os.path.join(base_path, "ufo.png")
    enemyImg.append(pygame.image.load(enemy_path))
    enemyX.append(random.randint(0,735))
    enemyY.append(random.randint(30,150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# Bullet

# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving

base_path = os.path.dirname(__file__)
bullet_path = os.path.join(base_path, "bullet.png")
bulletImg = pygame.image.load(bullet_path)
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

#score

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 30)
textX = 20
textY = 20

#Game over

over_font = pygame.font.Font('freesansbold.ttf', 70)


def show_score(x,y):
    score = font.render("Score: " + str(score_value), True, (255,255,255))
    screen.blit(score, (x, y))

def game_over_text():
    game_over = over_font.render("Game Over ", True, (255,255,255))
    screen.blit(game_over, (200, 250))

def player(x,y):
    screen.blit(playerImg, (x, y))

def enemy(x,y,i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg,(x + 16, y + 10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 30 :
        return True
    else:
        return False

#Game Loop
#for exiting game to make sure it does not hang the screen, we create an event
running = True
while running:

    #Screen color
    screen.fill((0, 0, 0))
    
    #Background image
    screen.blit(background, (0,0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
        #If keystroke is pressed, check if it is left or right
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -7
            if event.key == pygame.K_RIGHT:
                playerX_change = 7
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    base_path = os.path.dirname(__file__)
                    bullet_sound_path = os.path.join(base_path, "bullet.wav")
                    bullet_Sound = mixer.Sound(bullet_sound_path)
                    bullet_Sound.play() #we dont add -1 because we dont want it to play in a loop
                    #Getting current X-cordinate of spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change
    
    #adding boundary for player
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    #Movement of enemy
    for i in range(num_of_enemies):

        #Game over
        if enemyY[i] > 420 :
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] +=  enemyX_change[i]
        if  enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        #Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            base_path = os.path.dirname(__file__)
            explosion_sound_path = os.path.join(base_path, "collision.wav")
            explosion_Sound = mixer.Sound(explosion_sound_path)
            explosion_Sound.play()
            bulletY = 480
            bullet_state = "ready"

            score_value += 5

            enemyX[i] = random.randint(0,735)
            enemyY[i] = random.randint(30,150)
        
        enemy(enemyX[i], enemyY[i], i)
    
    #Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX,playerY)

    show_score(textX, textY)
    
    pygame.display.update() #To update screen continuously, this line needs to be present in every game