# Drift Racing - v2.0 (probably should be v35, but since tracking, this is v2)
# by Kyle Glackin with a hell of a lot of help from the Internet

import pygame
import math
from pygame.locals import *
import random
import time

# CONFIG FILES AND SETTINGS
# Change filename below (between /from/ and /import/) to switch files

# Color
from cool_color_scheme import *

# Track
from map import *
# Car
from base_car import *

# Initialize Things
pygame.init()
screen = pygame.display.set_mode((screen_width,screen_height))

pygame.font.init()
myfont = pygame.font.SysFont('Courier', 22)

clock = pygame.time.Clock()

# Joystick Initial Check
joystick_yn = pygame.joystick.get_count()
if joystick_yn > 0:
    pygame.joystick.init()
    pygame.joystick.Joystick(0).init()

# Start State
from start_state import *

fast_str = "--"
fastestlap = "--"
maxlaps = 0

startTime = time.time()

# Last Step
done = False

# Main Gameloop
while done == False:

    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done = True # Flag that we are done so we exit this loop

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

    dt = clock.tick(60)

    vel_x -= drag * vel_x
    vel_y -= drag * vel_y

    #change the degree of rotation via keyboard
    if keys[0]==True:
        degree += turningradius*dt*(math.sqrt(vel_x**2 + vel_y**2))
    if keys[1]==True:
        degree -= turningradius*dt*(math.sqrt(vel_x**2 + vel_y**2))

    # change direction using Joystick

    axis = 0
    if joystick_yn > 0:
        axis = pygame.joystick.Joystick(0).get_axis(0)
        trigger = pygame.joystick.Joystick(0).get_axis(3)
        # Expand the center of the axis controller so it doesn't drift
        if -.2 < pygame.joystick.Joystick(0).get_axis(0) < .2:
            axis = 0
    degree = degree - turningradius*dt*(math.sqrt(vel_x**2 + vel_y**2))*(axis/1.5)

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
        ypos = screen_height - (ypos+car_l)

    #create new surface with white BG
    surf =  pygame.Surface((car_w, car_l))
    surf.fill((PLAYER1))
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

    #rotate surf by DEGREE amount degrees
    rotatedSurf =  pygame.transform.rotate(surf, degree)

    #get the rect of the rotated surf and set it's center to the oldCenter
    rotRect = rotatedSurf.get_rect()
    rotRect.center = oldCenter

    #clear screen at the start of every frame
    # Set the screen background
    if death == 0:

        screen.fill(BACKGROUND)

    pygame.draw.rect(screen, FINISHLINE, finish)

    # Draw the obstacle
    for x in range(0,5):
        pygame.draw.rect(screen, OBSTACLES, [obst_x[x], obst_y[x], obst_w[x], obst_h[x]])

    speed = str(round((math.sqrt(vel_x**2+vel_y**2)*200), 1))
    timer = str(round((time.time() - startTime), 2))

    laps_gui = myfont.render('Laps:', 1, TEXT)
    laps_count = myfont.render(str(laps), 1, TEXT)
    most_gui = myfont.render('Most Laps:', 1, TEXT)
    most_count = myfont.render(str(maxlaps), 1, TEXT)
    time_gui = myfont.render('This Lap:', 1, TEXT)
    time_val = myfont.render(str(timer), 1, TEXT)
    fastest_gui = myfont.render('Fastest Lap:', 1, TEXT)
    fastest_val = myfont.render(str(fast_str), 1, TEXT)
    last_gui = myfont.render('Last Lap:', 1, TEXT)
    last_val = myfont.render(str(last_str), 1, TEXT)
    speed_gui = myfont.render('Speed:', 1, TEXT)
    speed_val = myfont.render(str(speed), 1, TEXT)

    if last_laptime == 0:
        last_val = myfont.render("--", 1, TEXT)
    if last_str == 0:
        last_val = myfont.render("--", 1, TEXT)


    #draw rotatedSurf with the corrected rect so it gets put in the proper spot


    screen.blit(rotatedSurf, rotRect)
    screen.blit(most_gui,   (60,40))
    screen.blit(most_count, (200,40))
    screen.blit(laps_gui,   (60,10))
    screen.blit(laps_count, (200,10))
    screen.blit(last_gui,   (275, 10))
    screen.blit(last_val,   (440, 10))
    screen.blit(fastest_gui, (275, 40))
    screen.blit(fastest_val, (440, 40))
    screen.blit(time_gui,   (560, 10))
    screen.blit(time_val,   (690, 10))
    screen.blit(speed_gui,  (560,40))
    screen.blit(speed_val,  (690,40))

    # Die  if obstacle is touched
    for x in range(0,5):
        if oldCenter[0] > obst_x[x] and oldCenter[0] < obst_x[x]+obst_w[x] and oldCenter[1] > obst_y[x] and oldCenter[1] < obst_y[x]+obst_h[x]:
            death = 1

# Scoring
    # Add a counter to the number of laps if the car crosses the finish line if SOMETHING foes from 0 - 1
    if previous_y > finish[1]+finish[3] and oldCenter[0] > finish[0] and oldCenter[0] < finish[0]+finish[2] and oldCenter[1] > finish[1] and oldCenter[1] < finish[1]+finish[3]:
        laps += 1
        last_laptime = time.time() - startTime
        if fastestlap == "--":
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
        screen.fill(DEAD)
        pygame.display.flip()

        time.sleep(1)

        #Initialize Start State
        from start_state import *
        startTime = time.time()


    #show the screen surface
    pygame.display.flip()
