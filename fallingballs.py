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
PLAYERCOLOR = (127,255,212)
RANDPLAYERCOLOR = (0,166,255)

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
    
    def get_top(self):    return self.position[1] - self.radius
    def get_bottom(self): return self.position[1] + self.radius
    def get_left(self):   return self.position[0] - self.radius
    def get_right(self):  return self.position[0] + self.radius

class Player():
    def __init__(self, x,y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.lastdir = rand.choice(range(0,2))

    def get_right(self):    return self.x + self.width
    def get_left(self):     return self.x
    def get_bottom(self):   return self.y
    def get_top(self):      return self.y - self.height   

def initObjects():
    global WINDOWWIDTH, WINDOWHEIGHT, PLAYERWWIDTH, PLAYERHEIGHT
    
    player = Player(int(WINDOWWIDTH/2- PLAYERWIDTH/2),
                    int(WINDOWHEIGHT- PLAYERHEIGHT),
                    PLAYERWIDTH,
                    PLAYERHEIGHT,
                    RANDPLAYERCOLOR)
    randPlayer = Player(int(WINDOWWIDTH/2- PLAYERWIDTH/2),
                    int(WINDOWHEIGHT - PLAYERHEIGHT),
                    PLAYERWIDTH,
                    PLAYERHEIGHT,
                    PLAYERCOLOR)
    balls = [Ball() for i in range(1)]
    return player,randPlayer, balls

def drawBackground(color):
    screen.fill(color)
    
def drawScore(score):
    font = pygame.font.Font(None, 36)
    scoreText = font.render('Score: {}'.format(score), 1, BLACK)
    textpos = scoreText.get_rect()
    textpos.topleft = (WINDOWWIDTH/2- 45, 50)
    screen.blit(scoreText, textpos)

def updatePlayer(player):


    
    if player.get_right() > WINDOWWIDTH:
        print('afdasdf')
        player.right = WINDOWWIDTH
    if player.get_left() < 0:              player.left = 0
    if player.get_bottom() > WINDOWHEIGHT: player.bottom = WINDOWHEIGHT
    if player.get_top() < 0:               player.top = 0

def drawPlayer(screen, player):       
    rect = pygame.Rect(player.x, player.y, player.width, player.height)
    pygame.draw.rect(screen, player.color, rect)

def updateRandomPlayer(player):    
    if player.counter  != 0:
        if player.state == 'r': player.x -= int(player.width/4)
        elif player.state == 'l': player.x += int(player.width/4)
        elif player.state == 'u': player.y -= int(player.height/4)
        elif player.state == 't': player.y += int(player.height/4)
        player.counter -= 1
            
    else:
        r = rand.choice([0,1, player.lastdir, player.lastdir, player.lastdir, player.lastdir])
        player.lastdir = r
        stepsize = int(player.width + player.height)/16

        stay = rand.choice(list(range(4)))
        stay = 1
        if stay == 0:
            return
        else:
            if r == 0: player.x -= stepsize #left
            else: player.x += stepsize #right

def checkRandomPlayerBounds(p):
    if p.get_right() > WINDOWWIDTH:
        p.state = 'r'
        p.counter = int(WINDOWWIDTH/PLAYERWIDTH)*2

    elif p.get_left() < 0:
        p.state = 'l'
        p.counter = int(WINDOWWIDTH/PLAYERWIDTH)*2

    elif p.get_bottom() > WINDOWHEIGHT:
        p.state = 'b'
        p.counter = int(WINDOWHEIGHT/PLAYERHEIGHT)*2

    elif p.get_top() < 0:
        p.state = 't'
        p.counter = int(WINDOWHEIGHT/PLAYERHEIGHT)*2

def updateBalls(balls, score, dt):
    for ball in balls:
        if ball.get_top() <= 0:
            ball.velocity[1] *= -1
        if ball.get_bottom() >= WINDOWHEIGHT:
            ball.velocity[1] *= -1
        if ball.get_left() > WINDOWWIDTH:
            score += 1
            ball.reset()
        ball.move(ball.velocity, dt)
        ball.draw(ball.position)
    return score

def collisionOccurred(player, balls):
    for ball in balls:
        if ball.get_top() > player.get_bottom(): continue #no collision    
        if ball.get_bottom() < player.get_top(): continue #no collision
        if ball.get_right() < player.get_left(): continue #no collision
        if ball.get_left() > player.get_right(): continue #no collision
        return True
    return False

def addBall(balls):
    balls.append(Ball())
    return balls

def gameOver(score, player, randPlayer, balls, dt):
    drawBackground(RED)
    updatePlayers(player, randPlayer)
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
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:  player.x += 10
    elif keys[pygame.K_LEFT] or keys[pygame.K_a]: player.x -= 10

def main():
    pygame.init()
    global screen
    screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))    
    pygame.display.set_caption('Falling Balls')
    clock = pygame.time.Clock()
    fps = 30

    player, randPlayer, balls = initObjects()
    randPlayer.counter = 0
    randPlayer.state = 'n'
    score = 0

    timeCount = 0
    counter = 1
    dt = .15
    while True:        
        drawBackground(WHITE)
        drawScore(score)

        checkEvents(player)
        checkRandomPlayerBounds(randPlayer)
        score = updateBalls(balls, score, dt)

        updatePlayer(player)
        updateRandomPlayer(randPlayer)
        
        drawPlayer(screen, player)
        drawPlayer(screen, randPlayer)
        
        pygame.display.update()
        clock.tick(fps)
        
        totalTime = pygame.time.get_ticks()
        timeCount = totalTime - 3000*counter
        if timeCount > 0:
            addBall(balls)
            counter += 1

        if collisionOccurred(player, balls):
            parker = 64
            #break
    gameOver(score, player, randPlayer, balls, dt)
    pygame.display.update()
    time.sleep(5)
                    
if __name__=='__main__':
    main()
