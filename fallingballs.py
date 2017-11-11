#falling balls game
#by parker sorenson
#07/02/17
import pygame, sys
from pygame.locals import *
import random as rand
import numpy as np
import time

WINDOWWIDTH = 600
WINDOWHEIGHT = 400
PLAYERHEIGHT = 30
PLAYERWIDTH = 40
ORIGIN = (0,0)

WHITE = (255,255,255)

BLACK = (0,0,0)
RED = (255,0,0)
PLAYERCOLOR = BLACK
BALLCOLOR = BLACK

class Ball:
    def __init__(self):
        self.radius = rand.randint(25,45)
        self.x = -self.radius - 10
        self.y = rand.randint(self.radius*2, WINDOWHEIGHT- self.radius*2)
        self.position = np.array([-self.radius -rand.randint(10,70),
                                  rand.randint(self.radius*2,
                                               WINDOWHEIGHT- self.radius*2)])
        self.velocity = np.array([20.0, rand.randrange(4,5)])
        self.color = (rand.randint(0,255), rand.randint(0,255),rand.randint(0,255))
        self.gravity = np.array([0.0, 12])

    def reset(self):
        self.position[0] = -self.radius - rand.randint(10,70)
        self.position[1] = rand.randint(self.radius*2, WINDOWHEIGHT- self.radius*2)

    def draw(self, pos):
        self.position[0] = pos[0]
        self.position[1] = pos[1]
        pygame.draw.circle(screen, self.color, (self.position), self.radius, 3)

    def move(self, velocity, dt):
        self.position[0] += int(velocity[0]*dt)
        self.position[1] += int(velocity[1]*dt)
        self.velocity += self.gravity*dt
    
    def getTop(self):
        return self.position[1] - self.radius

    def getBottom(self):
        return self.position[1] + self.radius

    def getLeft(self):
        return self.position[0] - self.radius

    def getRight(self):
        return self.position[0] + self.radius

def initObjects():
    global WINDOWWIDTH, WINDOWHEIGHT, PLAYERWWIDTH, PLAYERHEIGHT
    
    player = pygame.Rect(int(WINDOWWIDTH/2- PLAYERWIDTH/2),
                         int(WINDOWHEIGHT- PLAYERHEIGHT),
                         PLAYERWIDTH,PLAYERHEIGHT)
    balls = [Ball() for i in range(1)]
    return player, balls

def drawBackground(color):
    screen.fill(color)
    
def drawScore(score):
    font = pygame.font.Font(None, 36)
    scoreText = font.render('Score: {}'.format(score), 1, BLACK)
    textpos = scoreText.get_rect()
    textpos.topleft = (WINDOWWIDTH/2- 45, 50)
    screen.blit(scoreText, textpos)

def updatePlayer(player):
     if player.right > WINDOWWIDTH:
        player.right = WINDOWWIDTH
     if player.left < 0:
        player.left = 0
     if player.bottom > WINDOWHEIGHT:
         player.bottom = WINDOWHEIGHT
     if player.top < 0:
         player.top = 0
     pygame.draw.rect(screen, PLAYERCOLOR, player)
 
def updateBalls(balls, score, dt):
    for ball in balls:
        if ball.getTop() <= 0:
            ball.velocity[1] *= -1
        if ball.getBottom() >= WINDOWHEIGHT:
            ball.velocity[1] *= -1
        if ball.getLeft() > WINDOWWIDTH:
            score += 1
            ball.reset()
        ball.move(ball.velocity, dt)
        ball.draw(ball.position)
    return score

def collisionOccurred(player, balls):
    for ball in balls:
        if ball.getTop() > player.bottom: continue #no collision    
        if ball.getBottom() < player.top: continue #no collision
        if ball.getRight() < player.left: continue #no collision
        if ball.getLeft() > player.right: continue #no collision
        return True
    return False

def addBall(balls):
    newBall = Ball()
    balls.append(newBall)
    return balls

def gameOver(score, player, balls, dt):
    drawBackground(RED)
    updatePlayer(player)
    updateBalls(balls, score, dt)

    for ball in balls:
        ball.velocity.fill(0)
    
    font = pygame.font.Font(None, 36)
    text = font.render('Game Over! Final Score: {}'.format(score), 1, WHITE)
    textpos = text.get_rect()
    textpos.topleft = (WINDOWWIDTH/2 - 150, 50)
    screen.blit(text, textpos)

def checkEvents(player):
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player.x += 10
    elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player.x -= 10

def main():
    pygame.init()
    global screen
    screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))    
    pygame.display.set_caption('Falling Balls')
    clock = pygame.time.Clock()
    fps = 30

    player, balls = initObjects()
    score = 0

    timeCount = 0
    counter = 1
    dt = .15
    while True:        
        drawBackground(WHITE)
        drawScore(score)        
        updatePlayer(player)
        score = updateBalls(balls, score, dt)
        
        checkEvents(player)                   
        pygame.display.update()
        clock.tick(fps)
        
        totalTime = pygame.time.get_ticks()
        timeCount = totalTime - 3000*counter
        if timeCount > 0:
            addBall(balls)
            counter += 1

        if collisionOccurred(player, balls):
            break
    gameOver(score, player, balls, dt)
    pygame.display.update()
    time.sleep(5)
                    
if __name__=='__main__':
    main()
