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
from config_files.colorways.pacsun_color_scheme import *

# Track
from map import *

# Car
from base_car import *

# Coordinate Wrapper
import coord_wrapper

# Initialize Things
pygame.init()
screen = pygame.display.set_mode((screen_width,screen_height))

pygame.font.init()
myfont = pygame.font.SysFont('Courier', 22)

# Joystick Initial Check
joystick_yn = pygame.joystick.get_count()
if joystick_yn == 1:
    pygame.joystick.init()
    pygame.joystick.Joystick(0).init()
if joystick_yn == 2:
    pygame.joystick.init()
    pygame.joystick.Joystick(0).init()
    pygame.joystick.Joystick(1).init()


# Start State
from start_state import *

fast_str_1p = "--"
fastestlap_1p = "--"
maxlaps_1p = 0

fast_str_2p = "--"
fastestlap_2p = "--"
maxlaps_2p = 0

clock = pygame.time.Clock()

screen.fill(BACKGROUND)
countdown = myfont.render('3', 1, TEXT)
screen.blit(countdown, (screen_width/2, screen_height/2))
pygame.display.flip()
time.sleep(1)

screen.fill(BACKGROUND)
countdown = myfont.render('2', 1, TEXT)
screen.blit(countdown, (screen_width/2, screen_height/2))
pygame.display.flip()
time.sleep(1)

screen.fill(BACKGROUND)
countdown = myfont.render('1', 1, TEXT)
screen.blit(countdown, (screen_width/2, screen_height/2))
pygame.display.flip()
time.sleep(1)

startTime_1p = time.time()
startTime_2p = time.time()
racestart = time.time()

# Last Step
done = False

# Main Gameloop
while done == False:

# Pull Data From Inputs
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done = True # Flag that we are done so we exit this loop

        if event.type == pygame.KEYDOWN:
            if event.key==pygame.K_LEFT:
                keys_1p[0]=True
            elif event.key==pygame.K_RIGHT:
                keys_1p[1]=True
            elif event.key==pygame.K_UP:
                keys_1p[2]=True
            elif event.key==pygame.K_DOWN:
                keys_1p[3]=True

        if event.type == pygame.KEYUP:
            if event.key==pygame.K_LEFT:
                keys_1p[0]=False
            elif event.key==pygame.K_RIGHT:
                keys_1p[1]=False
            elif event.key==pygame.K_UP:
                keys_1p[2]=False
            elif event.key==pygame.K_DOWN:
                keys_1p[3]=False

        if joystick_yn == 0:
            axis_1p = 0
            axis_2p = 0

        if joystick_yn == 1:
            if event.type == pygame.JOYBUTTONDOWN:
                if pygame.joystick.Joystick(0).get_button(0) == 1:
                    keys_1p[2]=True
                if pygame.joystick.Joystick(0).get_button(1) == 1:
                    keys_1p[3]=True

            if event.type == pygame.JOYBUTTONUP:
                if pygame.joystick.Joystick(0).get_button(0) == 0:
                    keys_1p[2]=False
                if pygame.joystick.Joystick(0).get_button(1) == 0:
                    keys_1p[3]=False

            axis_1p = pygame.joystick.Joystick(0).get_axis(0)
            if -.2 < pygame.joystick.Joystick(0).get_axis(0) < .2:
                axis_1p = 0

            axis_2p = 0

        if joystick_yn == 2:
            if event.type == pygame.JOYBUTTONDOWN:
                if pygame.joystick.Joystick(0).get_button(0) == 1:
                    keys_1p[2]=True
                if pygame.joystick.Joystick(0).get_button(1) == 1:
                    keys_1p[3]=True

            if event.type == pygame.JOYBUTTONUP:
                if pygame.joystick.Joystick(0).get_button(0) == 0:
                    keys_1p[2]=False
                if pygame.joystick.Joystick(0).get_button(1) == 0:
                    keys_1p[3]=False

            axis_1p = pygame.joystick.Joystick(0).get_axis(0)
            if -.2 < pygame.joystick.Joystick(0).get_axis(0) < .2:
                axis_1p = 0

            if event.type == pygame.JOYBUTTONDOWN:
                if pygame.joystick.Joystick(1).get_button(0) == 1:
                    keys_2p[2]=True
                if pygame.joystick.Joystick(1).get_button(1) == 1:
                    keys_2p[3]=True

            if event.type == pygame.JOYBUTTONUP:
                if pygame.joystick.Joystick(1).get_button(0) == 0:
                    keys_2p[2]=False
                if pygame.joystick.Joystick(1).get_button(1) == 0:
                    keys_2p[3]=False

            axis_2p = pygame.joystick.Joystick(1).get_axis(0)
            if -.2 < pygame.joystick.Joystick(1).get_axis(0) < .2:
                axis_2p = 0

# Game Engine

    dt = clock.tick(60)

    vel_x_1p -= drag * vel_x_1p
    vel_y_1p -= drag * vel_y_1p

    vel_x_2p -= drag * vel_x_2p
    vel_y_2p -= drag * vel_y_2p

    #change the degree of rotation via keyboard
    if keys_1p[0]==True:
        degree_1p += turningradius*(math.sqrt(vel_x_1p**2 + vel_y_1p**2))
    if keys_1p[1]==True:
        degree_1p -= turningradius*(math.sqrt(vel_x_1p**2 + vel_y_1p**2))

    if keys_2p[0]==True:
        degree_2p += turningradius*(math.sqrt(vel_x_2p**2 + vel_y_2p**2))
    if keys_2p[1]==True:
        degree_2p -= turningradius*(math.sqrt(vel_x_2p**2 + vel_y_2p**2))

    # change direction using Joystick
    degree_1p = degree_1p - turningradius*(math.sqrt(vel_x_1p**2 + vel_y_1p**2))*(axis_1p/1.75)

    degree_2p = degree_2p - turningradius*(math.sqrt(vel_x_2p**2 + vel_y_2p**2))*(axis_2p/1.75)

    # Add the effect of the turn
    accel_x_1p = accel*math.sin(math.radians(degree_1p))
    accel_y_1p = accel*math.cos(math.radians(degree_1p))

    accel_x_2p = accel*math.sin(math.radians(degree_2p))
    accel_y_2p = accel*math.cos(math.radians(degree_2p))

    # Add the acceleration to the current speed vectors
    if keys_1p[2]==True:
        vel_x_1p += accel_x_1p
        vel_y_1p += accel_y_1p

    if keys_1p[3]==True:
        vel_x_1p -= accel_x_1p
        vel_y_1p -= accel_y_1p

    if keys_2p[2]==True:
        vel_x_2p += accel_x_2p
        vel_y_2p += accel_y_2p

    if keys_2p[3]==True:
        vel_x_2p -= accel_x_2p
        vel_y_2p -= accel_y_2p

    xpos_1p += vel_x_1p
    ypos_1p += vel_y_1p

    xpos_2p += vel_x_2p
    ypos_2p += vel_y_2p

    # Wrapping and correction
    new_coords = coord_wrapper.coord_wrap(degree_1p, xpos_1p, ypos_1p, screen_width, screen_height, car_l)
    degree_1p = new_coords[0]
    xpos_1p = new_coords[1]
    ypos_1p = new_coords[2]

    new_coords = coord_wrapper.coord_wrap(degree_2p, xpos_2p, ypos_2p, screen_width, screen_height, car_l)
    degree_2p = new_coords[0]
    xpos_2p = new_coords[1]
    ypos_2p = new_coords[2]

    #create new surface with white BG
    car_1p =  pygame.Surface((car_w, car_l))
    car_1p.fill((PLAYER1))
    #set a color key for blitting
    car_1p.set_colorkey((255, 0, 0))

    if joystick_yn == 2:
        car_2p =  pygame.Surface((car_w, car_l))
        car_2p.fill((PLAYER2))
        #set a color key for blitting
        car_2p.set_colorkey((255, 0, 0))

    ##ORIGINAL UNCHANGED
    #what coordinates will the static image be placed:
    where_1p = xpos_1p, ypos_1p
    if joystick_yn == 2:
        where_2p = xpos_2p, ypos_2p

    #draw surf to screen and catch the rect that blit returns
    blittedRect_1p = screen.blit(car_1p, where_1p)
    if joystick_yn == 2:
        blittedRect_2p = screen.blit(car_2p, where_2p)

    ##ROTATED
    #get center of surf for later
    oldCenter_1p = blittedRect_1p.center
    if joystick_yn == 2:
        oldCenter_2p = blittedRect_2p.center


    #rotate surf by DEGREE amount degrees
    rotatedSurf_1p =  pygame.transform.rotate(car_1p, degree_1p)
    if joystick_yn == 2:
        rotatedSurf_2p =  pygame.transform.rotate(car_2p, degree_2p)

    #get the rect of the rotated surf and set it's center to the oldCenter
    rotRect_1p = rotatedSurf_1p.get_rect()
    rotRect_1p.center = oldCenter_1p

    if joystick_yn == 2:
        rotRect_2p = rotatedSurf_2p.get_rect()
        rotRect_2p.center = oldCenter_2p

    speed_1p = str(round((math.sqrt(vel_x_1p**2+vel_y_1p**2)*10), 1))
    timer_1p = str(round((time.time() - startTime_1p), 2))

    if joystick_yn == 2:
        speed_2p = str(round((math.sqrt(vel_x_2p**2+vel_y_2p**2)*10), 1))
        timer_2p = str(round((time.time() - startTime_2p), 2))

    #clear screen at the start of every frame
    # Set the screen background

    # Die  if obstacle is touched
    for x in range(0,5):
        if oldCenter_1p[0] > obst_x[x] and oldCenter_1p[0] < obst_x[x] + obst_w[x] and oldCenter_1p[1] > obst_y[x] and oldCenter_1p[1] < obst_y[x] + obst_h[x] and death_1p == 0:
            death_1p = 30
            grow_1p = 0

    if joystick_yn == 2:
        for x in range(0,5):
            if oldCenter_2p[0] > obst_x[x] and oldCenter_2p[0] < obst_x[x] + obst_w[x] and oldCenter_2p[1] > obst_y[x] and oldCenter_2p[1] < obst_y[x] + obst_h[x] and death_2p == 0:
                death_2p = 30
                grow_2p = 0

    # Scoring
    # Add a counter to the number of laps if the car crosses the finish line if SOMETHING foes from 0 - 1
    if previous_y_1p > finish[1]+finish[3] and oldCenter_1p[0] > finish[0] and oldCenter_1p[0] < finish[0]+finish[2] and  oldCenter_1p[1] <= finish[1]+finish[3]:
        if penalty_1p > 0:
            penalty_1p -= 1
            laps_1p += 1

        elif penalty_1p == 0:
            laps_1p += 1
            last_laptime_1p = time.time() - startTime_1p
            if fastestlap_1p == "--":
                fastestlap_1p = last_laptime_1p
            if fastestlap_1p > last_laptime_1p:
                fastestlap_1p = last_laptime_1p
            fast_str_1p = round(fastestlap_1p,2)
            last_str_1p = round(last_laptime_1p,2)

            startTime_1p = time.time()

        if laps_1p > maxlaps_1p:
            maxlaps_1p = laps_1p

    if previous_y_1p < finish[1]+finish[3] and oldCenter_1p[0] > finish[0] and oldCenter_1p[0] < finish[0]+finish[2] and oldCenter_1p[1] >= finish[1]+finish[3]:
        laps_1p -= 1
        penalty_1p += 1

    previous_y_1p = oldCenter_1p[1]

    if joystick_yn == 2:
        if previous_y_2p > finish[1]+finish[3] and oldCenter_2p[0] > finish[0] and oldCenter_2p[0] < finish[0]+finish[2] and  oldCenter_2p[1] <= finish[1]+finish[3]:
            if penalty_2p > 0:
                penalty_2p -= 1
                laps_2p += 1

            elif penalty_2p == 0:
                laps_2p += 1
                last_laptime_2p = time.time() - startTime_2p
                if fastestlap_2p == "--":
                    fastestlap_2p = last_laptime_2p
                if fastestlap_2p > last_laptime_2p:
                    fastestlap_2p = last_laptime_2p
                fast_str_2p = round(fastestlap_2p,2)
                last_str_2p = round(last_laptime_2p,2)

                startTime_2p = time.time()

            if laps_2p > maxlaps_2p:
                maxlaps_2p = laps_2p

        if previous_y_2p < finish[1]+finish[3] and oldCenter_2p[0] > finish[0] and oldCenter_2p[0] < finish[0]+finish[2] and oldCenter_2p[1] >= finish[1]+finish[3]:
            laps_2p -= 1
            penalty_2p += 1

        previous_y_2p = oldCenter_2p[1]

    screen.fill(BACKGROUND)

    if death_1p > 0:
        grave_1p = oldCenter_1p
        keys_1p=[False,False,False,False]
        vel_x_1p = 0
        vel_y_1p = 0
        pygame.draw.circle(screen, PLAYER1, grave_1p, 1+grow_1p)
        grow_1p += 8
        death_1p -= 1
        lastloop_1p = death_1p

        if lastloop_1p == 0:
            degree_1p = 90

            # Starting Position
            xpos_1p = 200
            ypos_1p = 200

            vel_x_1p = 0
            vel_y_1p = 0

            # Score
            previous_y_1p = 0
            last_laptime_1p = 0
            laps_1p = 0
            last_str_1p = 0
            penalty_1p = 0

            # Inputs turned off to start
            keys_1p=[False,False,False,False]
            startTime_1p = time.time()
    if joystick_yn == 2:
        if death_2p > 0:
            grave_2p = oldCenter_2p
            vel_x_2p = 0
            vel_y_2p = 0
            keys_2p=[False,False,False,False]
            pygame.draw.circle(screen, PLAYER2, grave_2p, 1+grow_2p)
            grow_2p += 8
            death_2p -= 1
            lastloop_2p = death_2p

            if lastloop_2p == 0:
                degree_2p = 90

                # Starting Position
                xpos_2p = 200
                ypos_2p = 200

                vel_x_2p = 0
                vel_y_2p = 0

                # Score
                previous_y_2p = 0
                last_laptime_2p = 0
                laps_2p = 0
                last_str_2p = 0
                penalty_2p = 0

                # Inputs turned off to start
                keys_2p=[False,False,False,False]
                startTime_1p = time.time()

    if joystick_yn == 2:
        # First to 5 laps wins
        if laps_1p == 5:
            wintime= time.time() - racestart
            screen.fill(PLAYER1)
            victory_1p = myfont.render('Player 1 Wins in          seconds!!!', 1, TEXT)
            screen.blit(victory_1p, (screen_width/2-100, screen_height/2-50))
            wintime_val = myfont.render(str(round(wintime,2)), 1, TEXT)
            screen.blit(wintime_val, (screen_width/2+150, screen_height/2-50))
            pygame.display.flip()
            time.sleep(3)
            from start_state import *
            racestart = time.time()
            startTime_1p = time.time()
            startTime_2p = time.time()

        if laps_2p == 5:
            wintime= time.time() - racestart
            screen.fill(PLAYER2)
            victory_2p = myfont.render('Player 2 Wins in          seconds!!!', 1, TEXT)
            screen.blit(victory_2p, (screen_width/2-100, screen_height/2-50))
            wintime_val = myfont.render(str(round(wintime,2)), 1, TEXT)
            screen.blit(wintime_val, (screen_width/2+150, screen_height/2-50))
            pygame.display.flip()
            time.sleep(3)
            from start_state import *
            racestart = time.time()
            startTime_1p = time.time()
            startTime_2p = time.time()

    pygame.draw.rect(screen, FINISHLINE, finish)

    # Draw the obstacle
    for x in range(0,5):
        pygame.draw.rect(screen, OBSTACLES, [obst_x[x], obst_y[x], obst_w[x], obst_h[x]])

    if joystick_yn < 2:
        laps_gui_1p = myfont.render('Laps:', 1, TEXT)
    laps_count_1p = myfont.render(str(laps_1p), 1, TEXT)
    most_gui_1p = myfont.render('Most Laps:', 1, TEXT)
    most_count_1p = myfont.render(str(maxlaps_1p), 1, TEXT)
    time_gui_1p = myfont.render('This Lap:', 1, TEXT)
    time_val_1p = myfont.render(str(timer_1p), 1, TEXT)
    fastest_gui_1p = myfont.render('Fastest Lap:', 1, TEXT)
    fastest_val_1p = myfont.render(str(fast_str_1p), 1, TEXT)
    last_gui_1p = myfont.render('Last Lap:', 1, TEXT)
    last_val_1p = myfont.render(str(last_str_1p), 1, TEXT)
    speed_gui_1p = myfont.render('Speed:', 1, TEXT)
    speed_val_1p = myfont.render(str(speed_1p), 1, TEXT)

    if last_laptime_1p == 0:
        last_val_1p = myfont.render("--", 1, TEXT)
    if last_str_1p == 0:
        last_val_1p = myfont.render("--", 1, TEXT)

    if joystick_yn == 2:
        laps_gui_1p = myfont.render('Laps:     /5', 1, TEXT)
        laps_gui_2p = myfont.render('Laps:     /5', 1, TEXT)
        laps_count_2p = myfont.render(str(laps_2p), 1, TEXT)
        most_gui_2p = myfont.render('Most Laps:', 1, TEXT)
        most_count_2p = myfont.render(str(maxlaps_2p), 1, TEXT)
        time_gui_2p = myfont.render('This Lap:', 1, TEXT)
        time_val_2p = myfont.render(str(timer_2p), 1, TEXT)
        fastest_gui_2p = myfont.render('Fastest Lap:', 1, TEXT)
        fastest_val_2p = myfont.render(str(fast_str_2p), 1, TEXT)
        last_gui_2p = myfont.render('Last Lap:', 1, TEXT)
        last_val_2p = myfont.render(str(last_str_2p), 1, TEXT)
        speed_gui_2p = myfont.render('Speed:', 1, TEXT)
        speed_val_2p = myfont.render(str(speed_2p), 1, TEXT)

        if last_laptime_2p == 0:
            last_val_2p = myfont.render("--", 1, TEXT)
        if last_str_2p == 0:
            last_val_2p = myfont.render("--", 1, TEXT)
    if joystick_yn == 2:
        if death_1p == 0 and death_2p == 0:
            screen.blit(rotatedSurf_1p, rotRect_1p)
            screen.blit(rotatedSurf_2p, rotRect_2p)

        if death_2p == 0:
            screen.blit(rotatedSurf_2p, rotRect_2p)

    if death_1p == 0:
        screen.blit(rotatedSurf_1p, rotRect_1p)

    if joystick_yn == 2:
        pygame.draw.rect(screen, PLAYER1, [0, 0, screen_width/2, border])
        pygame.draw.rect(screen, PLAYER2, [screen_width/2, 0, screen_width/2, border])
        screen.blit(most_gui_2p,   (860,40))
        screen.blit(most_count_2p, (1000,40))
        screen.blit(laps_gui_2p,   (860,10))
        screen.blit(laps_count_2p, (970,10))
        screen.blit(last_gui_2p,   (1075, 10))
        screen.blit(last_val_2p,   (1240, 10))
        screen.blit(fastest_gui_2p, (1075, 40))
        screen.blit(fastest_val_2p, (1240, 40))
        screen.blit(time_gui_2p,   (1360, 10))
        screen.blit(time_val_2p,   (1490, 10))
        screen.blit(speed_gui_2p,  (1360,40))
        screen.blit(speed_val_2p,  (1490,40))

    if joystick_yn == 2:
        screen.blit(laps_count_1p, (170,10))

    if joystick_yn < 2:
        screen.blit(laps_count_1p, (200,10))


    screen.blit(most_gui_1p,   (60,40))
    screen.blit(most_count_1p, (200,40))
    screen.blit(laps_gui_1p,   (60,10))
    screen.blit(last_gui_1p,   (275, 10))
    screen.blit(last_val_1p,   (440, 10))
    screen.blit(fastest_gui_1p, (275, 40))
    screen.blit(fastest_val_1p, (440, 40))
    screen.blit(time_gui_1p,   (560, 10))
    screen.blit(time_val_1p,   (690, 10))
    screen.blit(speed_gui_1p,  (560,40))
    screen.blit(speed_val_1p,  (690,40))

    #show the screen surface
    pygame.display.flip()
