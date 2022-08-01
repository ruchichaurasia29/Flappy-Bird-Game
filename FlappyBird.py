import random
import sys
import os
from pygame.locals import *
import pygame
pygame.init()
pygame.mixer.init()

white=(255,255,255)
red=(255,0,0)
black= (0,0,0)
blue=(0,0,255)

root=pygame.display.set_mode((400,500))
pygame.display.update()

bg1 = pygame.image.load("birdbg.png")
bg1 = pygame.transform.scale(bg1, (400,500)).convert_alpha()

bg2 = pygame.image.load("over.jpg")
bg2 = pygame.transform.scale(bg2, (400,500)).convert_alpha()

bg = pygame.image.load("bg.png").convert_alpha()
gd=pygame.image.load("ground.png").convert_alpha()

b1=pygame.image.load("bird1.png").convert_alpha()
b2=pygame.image.load("bird2.png").convert_alpha()
b3=pygame.image.load("bird3.png").convert_alpha()

p1=pygame.image.load("pipe.png").convert_alpha()
p2=pygame.transform.rotate(pygame.image.load("pipe.png").convert_alpha(),180)

img=pygame.image.load("0.jpg").convert_alpha()
img1=pygame.image.load("1.jpg").convert_alpha()
img2=pygame.image.load("2.jpg").convert_alpha()
img3=pygame.image.load("3.jpg").convert_alpha()
img4=pygame.image.load("4.jpg").convert_alpha()
img5=pygame.image.load("5.jpg").convert_alpha()
img6=pygame.image.load("6.jpg").convert_alpha()
img7=pygame.image.load("7.jpg").convert_alpha()
img8=pygame.image.load("8.jpg").convert_alpha()
img9=pygame.image.load("9.jpg").convert_alpha()

font = pygame.font.SysFont(None, 30)
def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    root.blit(screen_text, [x,y])

fps=32
GROUNDY = 500 * 0.8
def welcome():
    exit_game = False
    while not exit_game:
        root.fill((black))
        root.blit(bg1, (0, 0))
        text_screen("Welcome To", blue, 160, 120)
        text_screen("Flappy Bird Game", blue, 125, 150)
        text_screen("Press Space Bar", red, 130, 210)
        text_screen("To Play", red, 170, 240)
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE):
                    pygame.mixer.music.load('sarena.mp3')
                    pygame.mixer.music.play()
                    gameloop()
        pygame.display.update()
        clock.tick(fps)

def gameloop():
    score=0
    playerx=int(400/5)
    playery=int(500/2)
    basex=0

    if (not os.path.exists("score.txt")):
        with open("score.txt", "w") as f:
            f.write("0")

    with open("score.txt", "r") as f:
        hiscore = f.read()

    newPipe1 = getRandom()
    newPipe2 = getRandom()

    upperPipes = [
        {'x': 400 + 200, 'y': newPipe1[0]['y']},
        {'x': 400 + 200 + (400 / 2), 'y': newPipe2[0]['y']},
    ]

    lowerPipes = [
        {'x': 400 + 200, 'y': newPipe1[1]['y']},
        {'x': 400 + 200 + (400 / 2), 'y': newPipe2[1]['y']},
    ]

    pipeVelX = -4

    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1

    playerFlapAccv = -8  # velocity while flapping
    playerFlapped = False


    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playerVelY = playerFlapAccv
                    playerFlapped = True

        crashTest = isCollide(playerx, playery, upperPipes,
                              lowerPipes)  # This function will return true if the player is crashed
        if crashTest:
            with open("score.txt", "w") as f:
                f.write(str(hiscore))
            return

        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY

        if playerFlapped:
            playerFlapped = False
        playerHeight = b1.get_height()
        playery = playery + min(playerVelY, GROUNDY - playery - playerHeight)

        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

            # Add a new pipe when the first is about to cross the leftmost part of the screen
        if 0 < upperPipes[0]['x'] < 5:
            newpipe = getRandom()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1]) 

        if upperPipes[0]['x'] < -p1.get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        playerMidPos = playerx + b1.get_width() / 2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + p1.get_width() / 2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                score += 10
                if score>int(hiscore):
                    hiscore=score

            # Lets blit our sprites now
        root.blit(bg, (0, 0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            root.blit(p1, (upperPipe['x'], upperPipe['y']))
            root.blit(p2, (lowerPipe['x'], lowerPipe['y']))

        root.blit(gd, (basex, GROUNDY))
        root.blit(b1, (playerx, playery))
        text_screen("Score :" + str(score),black, 10, 10)
        text_screen("High Score :" + str(hiscore), black, 10, 470)
        pygame.display.update()
        clock.tick(fps)

def isCollide(playerx, playery, upperPipes, lowerPipes):
    if playery > GROUNDY - 25 or playery < 0:
        root.blit(bg2, (0, 0))
        return True

    for pipe in upperPipes:
        pipeHeight = p1.get_height()
        if (playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < p1.get_width()):
            root.blit(bg2, (0, 0))
            return True

    for pipe in lowerPipes:
        if (playery + b1.get_height() > pipe['y']) and abs(playerx - pipe['x']) < p1.get_width():
            root.blit(bg2, (0, 0))
            return True
    return False

def getRandom():
    pipe_h=p1.get_height()
    offset=500/3
    y2=offset + random.randrange(0,int(500 - gd.get_height() - 1.2 * offset))
    pipe_x=500 + 10
    y1= pipe_h - y2 + offset
    pipe = [
        {'x': pipe_x, 'y': -y1},  # upper Pipe
        {'x': pipe_x, 'y': y2}  # lower Pipe
    ]
    return pipe


if __name__ == "__main__":
    pygame.init()
    clock=pygame.time.Clock()
    pygame.display.set_caption("Flappy Bird Game")

    while True:
        welcome()



