import pygame
import math
from pygame.locals import *
import random
import time

#rotation code reference: http://blog.tankorsmash.com/?p=128

#necessary pygame initializing
pygame.init()

pygame.joystick.init()
pygame.joystick.Joystick(0).init()

#cont_hat = pygame.joystick.Joystick(0).get_numhats()
#print("number of hats:",cont_hat)

clock = pygame.time.Clock()

#create a surface that will be seen by the user
screen_width =  1600
screen_height = 800

screen = pygame.display.set_mode((screen_width,screen_height))

WHITE=(255,255,255)
BLACK = (0,0,0)
GRAY = (100,100,100)
RED = (255,25,25)
YELLOW = (255,255,25)

done = False
degree = 90

score = 0

car_w = 10
car_l = 20

xpos = 100
ypos = 100

accel = .002
turningradius = 1

vel_x = 0
vel_y = 0

death = 0

coinblock = 20

obst_x = [0,0,0,0,0,0,0,0,0,0]
obst_y = [0,0,0,0,0,0,0,0,0,0]
obst_w = [0,0,0,0,0,0,0,0,0,0]
obst_h = [0,0,0,0,0,0,0,0,0,0]

for x in range(0,9):
    obst_x[x] = random.randint(0,screen_width)
    obst_y[x] = random.randint(0,screen_height)
    obst_w[x] = random.randint(50,200)
    obst_h[x] = random.randint(50,200)

coin_x = [0,0,0,0,0,0,0,0,0,0]
coin_y = [0,0,0,0,0,0,0,0,0,0]
coin_w = 15
coin_h = 15

hitbox = 20

for x in range(0,9):
    coin_x[x] = random.randint(0,screen_width)
    coin_y[x] = random.randint(0,screen_height)

keys=[False,False,False,False]

while done == False:

    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done = True # Flag that we are done so we exit this loop

#        if event.type == pygame.joystick.

        if event.type == pygame.KEYDOWN:
            if event.key==pygame.K_LEFT:
                keys[0]=True
            elif event.key==pygame.K_RIGHT:
                keys[1]=True
            elif event.key==pygame.K_UP:
                keys[2]=True
            elif event.key==pygame.K_DOWN:
                keys[3]=True

        if event.type == pygame.KEYUP:
            if event.key==pygame.K_LEFT:
                keys[0]=False
            elif event.key==pygame.K_RIGHT:
                keys[1]=False
            elif event.key==pygame.K_UP:
                keys[2]=False
            elif event.key==pygame.K_DOWN:
                keys[3]=False

        if event.type == pygame.JOYBUTTONDOWN:
            if pygame.joystick.Joystick(0).get_button(0) == 1:
                keys[2]=True
            if pygame.joystick.Joystick(0).get_button(1) == 1:
                keys[3]=True

        if event.type == pygame.JOYBUTTONUP:
            if pygame.joystick.Joystick(0).get_button(0) == 0:
                keys[2]=False
            if pygame.joystick.Joystick(0).get_button(1) == 0:
                keys[3]=False

    #create new surface with white BG
    surf =  pygame.Surface((car_w, car_l))
    surf.fill((255, 255, 255))
    #set a color key for blitting
    surf.set_colorkey((255, 0, 0))

    ##ORIGINAL UNCHANGED
    #what coordinates will the static image be placed:
    where = xpos, ypos

    #draw surf to screen and catch the rect that blit returns
    blittedRect = screen.blit(surf, where)

    ##ROTATED
    #get center of surf for later
    oldCenter = blittedRect.center

    dt = clock.tick(60)

    vel_x -= .075 * vel_x
    vel_y -= .075 * vel_y

    #change the degree of rotation via keyboard
    if keys[0]==True:
        degree += turningradius*dt*(math.sqrt(vel_x**2 + vel_y**2))
    if keys[1]==True:
        degree -= turningradius*dt*(math.sqrt(vel_x**2 + vel_y**2))

    # change direction using Joystick

    axis = pygame.joystick.Joystick(0).get_axis(0)

# Expand the center of the axis controller so it doesn't drift
    if -.1 < pygame.joystick.Joystick(0).get_axis(0) < .1:
        axis = 0

    degree = degree - turningradius*dt*(math.sqrt(vel_x**2 + vel_y**2))*(axis)

    accel_x = accel*math.sin(math.radians(degree))*dt
    accel_y = accel*math.cos(math.radians(degree))*dt

    if keys[2]==True:
        vel_x += accel_x
        vel_y += accel_y

    if keys[3]==True:
        vel_x -= accel_x
        vel_y -= accel_y

    if degree > 360:
        degree = 0 + (degree-360)

    if degree < 0:
        degree = (360 + degree)

    #rotate surf by DEGREE amount degrees
    rotatedSurf =  pygame.transform.rotate(surf, degree)

    #get the rect of the rotated surf and set it's center to the oldCenter
    rotRect = rotatedSurf.get_rect()
    rotRect.center = oldCenter

    xpos += vel_x*dt
    ypos += vel_y*dt

    # Wrap around screen edge
    if xpos > screen_width:
        xpos = 0 + (xpos-screen_width)
    if xpos < 0:
        xpos = screen_width - xpos
    if ypos > screen_height:
        ypos = 0 + (ypos-screen_height)
    if ypos < 0:
        ypos = screen_height - ypos

    #clear screen at the start of every frame
    # Set the screen background
    if death == 0:

        screen.fill(BLACK)

    # Draw the coins
    for x in range(0,9):
        pygame.draw.rect(screen, YELLOW, [coin_x[x], coin_y[x], coin_w, coin_h])

    # Win if obstacle is touched
    for x in range(0,9):
        if oldCenter[0] > coin_x[x]-hitbox and oldCenter[0] < coin_x[x]+coin_w+hitbox and oldCenter[1] > coin_y[x]-hitbox and oldCenter[1] < coin_y[x]+coin_h+hitbox:
            coin_x[x] = -100
            coin_y[x] = -100
            score +=1

    # Draw the obstacle
    for x in range(0,9):
        pygame.draw.rect(screen, RED, [obst_x[x], obst_y[x], obst_w[x], obst_h[x]])

    #draw rotatedSurf with the corrected rect so it gets put in the proper spot
    screen.blit(rotatedSurf, rotRect)

    # Die  if obstacle is touched
    for x in range(0,9):
        if oldCenter[0] > obst_x[x] and oldCenter[0] < obst_x[x]+obst_w[x] and oldCenter[1] > obst_y[x] and oldCenter[1] < obst_y[x]+obst_h[x]:
            death = 1

    if death == 1:
        screen.fill(RED)
        pygame.display.flip()

        time.sleep(1)
        death = 0
        score = 0

        obst_x = [0,0,0,0,0,0,0,0,0,0]
        obst_y = [0,0,0,0,0,0,0,0,0,0]
        obst_w = [0,0,0,0,0,0,0,0,0,0]
        obst_h = [0,0,0,0,0,0,0,0,0,0]

        for x in range(0,9):
            obst_x[x] = random.randint(0,screen_width)
            obst_y[x] = random.randint(0,screen_height)
            obst_w[x] = random.randint(50,200)
            obst_h[x] = random.randint(50,200)

        coin_x = [0,0,0,0,0,0,0,0,0,0]
        coin_y = [0,0,0,0,0,0,0,0,0,0]
        coin_w = 15
        coin_h = 15

        for x in range(0,9):
            coin_x[x] = random.randint(0,screen_width)
            coin_y[x] = random.randint(0,screen_height)

        # Start position of car
        xpos = 100
        ypos = 100

        degree = 90

        vel_x = 0
        vel_y = 0

        death = 0

    #show the screen surface
    pygame.display.flip()
