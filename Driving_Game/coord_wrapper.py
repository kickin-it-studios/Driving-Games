# Graphics correction
def coord_wrap(init_degree, init_xpos, init_ypos, screen_width, screen_height, init_car_l):

    new_degree = init_degree
    new_xpos = init_xpos
    new_ypos = init_ypos

    if init_degree > 360:
        new_degree = 0 + (init_degree-360)

    if init_degree < 0:
        new_degree = (360 + init_degree)

    if init_xpos > screen_width:
        new_xpos = 0 + (init_xpos-screen_width)
    if init_xpos < 0:
        new_xpos = screen_width - init_xpos
    if init_ypos > screen_height:
        new_ypos = 0 + (init_ypos-screen_height)
    if init_ypos < 0:
        new_ypos = screen_height - (init_ypos + init_car_l)

    return(new_degree,new_xpos, new_ypos)
