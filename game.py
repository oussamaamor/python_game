import pdb 
import pygame
from pygame import mixer
import random
import math
#initialization 
pygame.init()
#creating the screen
screen_X =700
screen_Y =500
screen = pygame.display.set_mode((screen_X,screen_Y))

#title and icon 
pygame.display.set_caption("space invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)
#background sound 

mixer.music.load('background.wav')
mixer.music.play(-1)

#background 
background = pygame.image.load('background.png')
#player 
playerImage = pygame.image.load('battleship.png')
init_playerX = (screen_X-32)/2  #32 is the size of the spaceship , a litle bit of math and I'll get it :) 
init_playerY = 400
post_changeX = 0
post_changeY = 0

def player(x,y): #here x and y are local variables (only used inside this fucntion)
    screen.blit(playerImage,(x,y))


#enemy 
enemyImage  = []
init_enemyX = []
init_enemyY = []
enemy_stepX = []
enemy_stepY = []
enemies_num = 10
for i in range(enemies_num):
    enemyImage.append(pygame.image.load('enemy.png'))
    init_enemyX.append(random.randint(0,667))
    init_enemyY.append(random.randint(25,125))
    enemy_stepX.append(5)
    enemy_stepY.append(50)
def enemy(x,y,i): #here x and y are local variables (only used inside this fucntion)
    screen.blit(enemyImage[i],(x,y))

#bullet

# ready = the byllet is there but you can't see it 
# fire = the bullet is currently moving
bulletImage = pygame.image.load('bullet.png')
init_bulletX = 0
init_bulletY = init_playerY
bullet_stepX = 0
bullet_stepY = 8
bullet_state = 'ready'

def fire(x,y):
    global bullet_state
    bullet_state ='fire'
    screen.blit(bulletImage,(x,y)) 

#creating elementary displacment (dx and dy )
dx=2
dy=0 #the spaceship is only moving horizontally 

def iscollision(init_enemyX,init_enemyY,init_bulletX,init_bulletY):
    distance = math.sqrt(math.pow(init_enemyX - init_bulletX, 2) + (math.pow(init_enemyY - init_bulletY, 2)))
    if distance < 27:
        return True
    else: 
        return False

#score

score = 0
font = pygame.font.Font('freesansbold.ttf',32)

textX = 10
textY = 10 
def show_score(x,y):
    score_shown = font.render('score : ' + str(score),True,(250,250,250))
    screen.blit(score_shown,(x,y))

#endig the game 
over_shown = pygame.font.Font('freesansbold.ttf',64)
def game_over_text():
    over_text = over_shown.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


#game loop
runnig = True
while runnig:
    #setting screen color or background 
    screen.fill((0,0,0))
    screen.blit(background,(0,0))
    #checking events : 
    for event in pygame.event.get():
        if event.type is pygame.QUIT:
            runnig = False
        if event.type ==pygame.KEYDOWN:
            #incrementing/decrementing the X's
            if event.key == pygame.K_LEFT:
                post_changeX -=dx
            if event.key == pygame.K_RIGHT:
                post_changeX +=dx 
            #incrementing/decrementing the Y's
            if event.key == pygame.K_UP:
                post_changeY -=dy
            if event.key == pygame.K_DOWN:
                post_changeY +=dy 
            #bullet
            if event.key == pygame.K_SPACE:
                init_bulletX = init_playerX
                if bullet_state == "ready":
                    bulletSound = mixer.Sound("laser.wav")
                    bulletSound.play()
                    # Get the current x cordinate of the spaceship
                    init_bulletX = init_playerX
                    fire(init_bulletX, init_bulletY)
        if event.type == pygame.KEYUP :
            post_changeX =0
            post_changeY=0
    #changing positions :
    init_playerX += post_changeX
    init_playerY += post_changeY
    init_enemyX += enemy_stepX
    #making borders :

    #player borders 
    if init_playerX <= 0 :
        init_playerX =0 
    elif init_playerX >= screen_X -32 : #the size of the spaceship is 32px
        init_playerX = screen_X-32
    if init_playerY <= 0 :
        init_playerY =0
    elif init_playerY >= screen_Y-32:
        init_playerY = screen_Y-32
    #enemy borders and mouvment
    for i in range(enemies_num):
        #game over 
        if init_enemyY[i] > init_playerY:
            for j in range(enemies_num):
                init_enemyY[j] = 2000
            game_over_text()
            break
        init_enemyX[i] += enemy_stepX[i]
        if init_enemyX[i] <= 0 :
            enemy_stepX[i] = 1
            init_enemyY[i] += enemy_stepY[i]
        elif init_enemyX[i] >= screen_X -32 : #the size of the spaceship is 32px
            enemy_stepX[i] = -1
            init_enemyY[i] += enemy_stepY[i]
        #collison :
        collision = iscollision(init_enemyX[i], init_enemyY[i], init_bulletX, init_bulletY)
        if collision:
            explosionSound = mixer.Sound("explosion.wav")
            explosionSound.play()
            init_bulletY = init_playerY
            bullet_state = 'ready'
            score +=1 
            init_enemyX[i] = random.randint(0, 700)
            init_enemyY[i] = random.randint(25,125)
        enemy(init_enemyX[i],init_enemyY[i],i) 

    #bullet mouvment 
    if init_bulletY <= 0:
        init_bulletY = init_playerY
        bullet_state = "ready"

    if bullet_state is "fire":
        fire(init_bulletX, init_bulletY)
        init_bulletY -= bullet_stepY
    player(init_playerX,init_playerY)
    show_score(textX,textY)
    pygame.display.update()
pygame.quit()