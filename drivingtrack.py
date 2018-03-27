import pygame
import math
from pygame.locals import *
import random
import time

#rotation code reference: http://blog.tankorsmash.com/?p=128

#necessary pygame initializing
pygame.init()
pygame.font.init()
pygame.joystick.init()
pygame.joystick.Joystick(0).init()

myfont = pygame.font.SysFont('Tahoma', 20)

cont_hat = pygame.joystick.Joystick(0).get_numhats()
print("number of hats:",cont_hat)

clock = pygame.time.Clock()

#create a surface that will be seen by the user
screen_width =  1600
screen_height = 800

screen = pygame.display.set_mode((screen_width,screen_height))

WHITE=(255,255,255)
BLACK = (0,0,0)
GRAY = (100,100,100)
RED = (255,25,25)
GREEN = (25,155,25)

done = False
degree = 90

car_w = 10
car_l = 20

xpos = 200
ypos = 200

accel = .0022
turningradius = 1.2

previous_y = 0
last_laptime = 0
fastestlap = "n/a"
fast_str = "n/a"

vel_x = 0
vel_y = 0

death = 0
laps = 0
border = 75
maxlaps = 0
last_str = 0


obst_x = [0,                0,                      0,                  screen_width-border,    screen_width/2-5*border]
obst_y = [0,                screen_height-border,   0,                  0,                      screen_height/2-border]
obst_w = [border,           screen_width,           screen_width,       border,                 10*border]
obst_h = [screen_height,    border,                 border,             screen_height,          2*border]

finish = [border, screen_height/2-border, screen_width/3, 15]

keys=[False,False,False,False]

startTime = time.time()

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

    vel_x -= .07 * vel_x
    vel_y -= .07 * vel_y

    #change the degree of rotation via keyboard
    if keys[0]==True:
        degree += turningradius*dt*(math.sqrt(vel_x**2 + vel_y**2))
    if keys[1]==True:
        degree -= turningradius*dt*(math.sqrt(vel_x**2 + vel_y**2))

    # change direction using Joystick

    axis = pygame.joystick.Joystick(0).get_axis(0)
    trigger = pygame.joystick.Joystick(0).get_axis(3)

# Expand the center of the axis controller so it doesn't drift
    if -.2 < pygame.joystick.Joystick(0).get_axis(0) < .2:
        axis = 0
    degree = degree - turningradius*dt*(math.sqrt(vel_x**2 + vel_y**2))*(axis/1.5)

    accel_x = accel*math.sin(math.radians(degree))*dt
    accel_y = accel*math.cos(math.radians(degree))*dt

    # for x in range (0,3):
    #     print(pygame.joystick.Joystick(0).get_numhats())
    #
    # if -.2 < pygame.joystick.Joystick(0).get_axis(4) < .2:
    #     trigger = 0
    #
    # vel_x += accel_x*trigger
    # vel_y += accel_y*trigger

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

    pygame.draw.rect(screen, GREEN, finish)

    # Draw the obstacle
    for x in range(0,5):
        pygame.draw.rect(screen, RED, [obst_x[x], obst_y[x], obst_w[x], obst_h[x]])

    speed = str(round((math.sqrt(vel_x**2+vel_y**2)*200), 1))
    timer = str(round((time.time() - startTime), 2))

    laps_gui = myfont.render('Laps:', 1, BLACK)
    laps_count = myfont.render(str(laps), 1, BLACK)
    most_gui = myfont.render('Most Laps:', 1, BLACK)
    most_count = myfont.render(str(maxlaps), 1, BLACK)
    time_gui = myfont.render('This Lap:', 1, BLACK)
    time_val = myfont.render(str(timer), 1, BLACK)
    fastest_gui = myfont.render('Fastest Lap:', 1, BLACK)
    fastest_val = myfont.render(str(fast_str), 1, BLACK)
    last_gui = myfont.render('Last Lap:', 1, BLACK)
    last_val = myfont.render(str(last_str), 1, BLACK)
    speed_gui = myfont.render('Speed:', 1, BLACK)
    speed_val = myfont.render(str(speed), 1, BLACK)

    if last_laptime == 0:
        last_val = myfont.render("n/a", 1, BLACK)
    if last_str == 0:
        last_val = myfont.render("n/a", 1, BLACK)


    #draw rotatedSurf with the corrected rect so it gets put in the proper spot


    screen.blit(rotatedSurf, rotRect)
    screen.blit(most_gui,(10,40))
    screen.blit(most_count,(110,40))
    screen.blit(laps_gui,(10,10))
    screen.blit(laps_count,(110,10))
    screen.blit(last_gui, (200, 10))
    screen.blit(last_val, (320, 10))
    screen.blit(fastest_gui, (200, 40))
    screen.blit(fastest_val, (320, 40))
    screen.blit(time_gui, (410, 10))
    screen.blit(time_val, (510, 10))
    screen.blit(speed_gui,(410,40))
    screen.blit(speed_val,(510,40))

    # Die  if obstacle is touched
    for x in range(0,5):
        if oldCenter[0] > obst_x[x] and oldCenter[0] < obst_x[x]+obst_w[x] and oldCenter[1] > obst_y[x] and oldCenter[1] < obst_y[x]+obst_h[x]:
            death = 1

    # Add a counter to the number of laps if the car crosses the finish line if SOMETHING foes from 0 - 1
    if previous_y > finish[1]+finish[3] and oldCenter[0] > finish[0] and oldCenter[0] < finish[0]+finish[2] and oldCenter[1] > finish[1] and oldCenter[1] < finish[1]+finish[3]:
        laps += 1
        last_laptime = time.time() - startTime
        if fastestlap == "n/a":
            fastestlap = last_laptime
        if fastestlap > last_laptime:
            fastestlap = last_laptime
        fast_str = round(fastestlap,2)
        last_str = round(last_laptime,2)

        startTime = time.time()

        if laps > maxlaps:
            maxlaps = laps

    if previous_y < finish[1] and oldCenter[0] > finish[0] and oldCenter[0] < finish[0]+finish[2] and oldCenter[1] > finish[1] and oldCenter[1] < finish[1]+finish[3]:
        laps -= 1

    previous_y = oldCenter[1]

    if death == 1:
        screen.fill(RED)
        pygame.display.flip()

        time.sleep(1)
        death = 0
        laps = 0
        previous_y = 0
        last_laptime = 0


        obst_x = [0,                0,                      0,                  screen_width-border,    screen_width/2-5*border]
        obst_y = [0,                screen_height-border,   0,                  0,                      screen_height/2-border]
        obst_w = [border,           screen_width,           screen_width,       border,                 10*border]
        obst_h = [screen_height,    border,                 border,             screen_height,          2*border]

        # Border variables
        #b_width = 0

        # Start position of car
        xpos = 200
        ypos = 200

        degree = 90

        vel_x = 0
        vel_y = 0

        startTime = time.time()

        keys=[False,False,False,False]

    #show the screen surface
    pygame.display.flip()
