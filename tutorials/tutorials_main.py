# Import the pygame module
import pygame

# Import random for random numbers
import random

# from main import draw_update_function
# 
# Import the menu library to more easily make menu selction
import pygame_menu

import helpers.redraw_helper as redraw_helper
import helpers.draw_update_function_helper as draw_update_function_helper

import tutorials.tut_level_controls as tut_level_controls
import tutorials.tut_guitar_holding as tut_guitar_holding

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
# from pygame.locals import *
from pygame.locals import (
    RLEACCEL,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

pygame.init()

# Initialize Pygame fonts
pygame.font.init()

mytheme = pygame_menu.themes.Theme( # transparent background
                title_background_color=(255, 187, 68),
                title_font_color=(255,255,255),
                widget_font_color=(0,0,0),
                background_color=pygame_menu.baseimage.BaseImage("assets/images/Oreng.jpg"), 
                widget_selection_effect = pygame_menu.widgets.NoneSelection(),
                title_bar_style= pygame_menu.widgets.MENUBAR_STYLE_NONE,
                title_offset= (120,20),
                title_font_shadow=True,
                title_font=pygame.font.Font("assets/font/Signatra.ttf",40),
                title_font_size=80,
                title_floating=True,
                )

pygame.init()

surface = pygame.display.set_mode((800, 600))

fonter=pygame.font.Font("assets/font/Signatra.ttf",40)

widgets=[]

tutorials_menu = pygame_menu.Menu('Tutorials', 800, 600,theme=mytheme)

controlsbutt=tutorials_menu.add.button('Controls', tut_level_controls.start, float=True,font_name=fonter)
controlsbutt.add_draw_callback(draw_update_function_helper.draw_update_function)
controlsbutt.translate(0,-180)
widgets.append(controlsbutt)

holdGuitarbutt=tutorials_menu.add.button('How to hold a Guitar', tut_guitar_holding.start, float=True,font_name=fonter)
holdGuitarbutt.add_draw_callback(draw_update_function_helper.draw_update_function)
holdGuitarbutt.translate(0,-100)
widgets.append(holdGuitarbutt)

backbutt=tutorials_menu.add.button('Back', pygame_menu.events.BACK, float=True,font_name=fonter)
backbutt.add_draw_callback(draw_update_function_helper.draw_update_function)
backbutt.translate(0,20)
widgets.append(backbutt)
exbutt=tutorials_menu.add.button('Quit', pygame_menu.events.EXIT, float=True,font_name=fonter)
exbutt.add_draw_callback(draw_update_function_helper.draw_update_function)
exbutt.translate(0,100)
widgets.append(exbutt)
for widget in widgets:
    redraw_helper.redraw(widget,widget.get_decorator(),[255,187,68])