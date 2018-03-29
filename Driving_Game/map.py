#create a surface that will be seen by the user
screen_width =  1700
screen_height = 1000

#Track
border = 75
obst_x = [0,                0,                      0,                  screen_width-border,    screen_width/2-5*border]
obst_y = [0,                screen_height-border,   0,                  0,                      screen_height/2-border]
obst_w = [border,           screen_width,           screen_width,       border,                 10*border]
obst_h = [screen_height,    border,                 border,             screen_height,          2*border]
# Track - Finish Line
finish = [0, screen_height/2-border, screen_width/2, 15]
