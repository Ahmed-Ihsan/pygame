import math
import random

import pygame
from pygame import mixer
import time

# Intialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('background.png')

# Sound
mixer.music.load("background.wav")
mixer.music.play(-1)

# Caption and Icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0
bullet_state_counter = 10
level = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 2

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# Bullet

# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving

bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"
slowMotion = False
# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
testY = 10

# font
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def show_bullet(x, y):
    score = font.render("Bullet: " + str(bullet_state_counter), True, (255, 255, 255))
    screen.blit(score, (x, y))

def show_level(x, y):
    score = font.render("Level: " + str(level), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    distance2 = math.sqrt(math.pow(enemyX - playerX, 2) + (math.pow(enemyY - playerY, 2)))
    if distance2 < 27:
        return 2
    if distance < 27:
        return 1
    else:
        return False

# Game Loop
n =[ n for n in range(num_of_enemies)]
counter = 0
running = True
Game_Over = False
while running:
    # RGB = Red, Green, Blue
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_UP:
                playerY_change = -5
            if event.key == pygame.K_DOWN:
                playerY_change = 5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_s:
                slowMotion = True
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready" and bullet_state_counter > 0:
                    bulletSound = mixer.Sound("laser.wav")
                    bulletSound.play()
                    # Get the current x cordinate of the spaceship
                    bulletX = playerX
                    bulletY = playerY
                    fire_bullet(bulletX, bulletY)
                    bullet_state_counter -= 1
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerX_change = 0
                playerY_change = 0
            if event.key == pygame.K_s:
                slowMotion = False
        if slowMotion:
            time.sleep(0.03)
               
    # 5 = 5 + -0.1 -> 5 = 5 - 0.1
    # 5 = 5 + 0.1
    playerX += playerX_change
    playerY += playerY_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    if playerY <= 0:
        playerY = 0
    elif playerY >= 536:
        playerY = 536

    # Enemy Movement
    
    
    for i in n :
        if counter == num_of_enemies:
            level += 1
            bullet_state_counter += 5 + level
            num_of_enemies += 2
            counter = 0
            n =[ n for n in range(num_of_enemies)]
            enemyX = []
            enemyY = []
            for i in range(num_of_enemies):
                enemyImg.append(pygame.image.load('enemy.png'))
                enemyX.append(random.randint(0, 736))
                enemyY.append(random.randint(50, 150))
                enemyX_change.append(4)
                enemyY_change.append(40)
            continue
        if i == -1:
            continue
        
        # Game Over
        if enemyY[i] > 440 or Game_Over :
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            playerX = 2000
            playerY = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision == 1:
            explosionSound = mixer.Sound("explosion.wav")
            explosionSound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            n[i] = -1
            counter += 1
            print(n)
        elif collision == 2:
            explosionSound = mixer.Sound("explosion.wav")
            explosionSound.play()
            Game_Over = True
        enemy(enemyX[i], enemyY[i], i)

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
          
    
    player(playerX, playerY)
    show_score(textX, testY)
    show_bullet(10, 60)
    show_level(10, 110)
    pygame.display.update()
