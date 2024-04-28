"""
This is the main file where our program starts. It will begin our PyGame module and setup the main menu window with all necessary assets
including level select, settings, and tutorials.

Files Affected - 
main.py
AudioTest.py
tutorials_main.py
setup.py
settings_menu.py
"""

from pygame_aseprite_animation import *
import os, pygame
import random
import math
import json
import pygame_menu

from pygame.locals import (
    RLEACCEL,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

import levels.twinkle_little_star as level1
import levels.level_happy_birthday as level2
import levels.greensleeves as level3



import helpers.redraw_helper as redraw_helper
import helpers.draw_update_function_helper as draw_update_function_helper
import tutorials.tutorials_main as tutorials_main
import helpers.settings_menu as settings_menu

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

 

pygame.mixer.init()

pygame.init()
pygame.display.set_caption("Guitar Champions")

Icon = pygame.image.load("assets/images/items/guitar.png")

pygame.display.set_icon(Icon)

pygame.font.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))





current_level = 0

level_list = [("Twinkle Little Star", level1),("Happy Birthday", level2),  ("Greensleeves", level3)]



def select_level(name, index):
    """
    Apply a bandpass filter to the audio data.
    """
    global current_level
    current_level = index

    pygame.display.flip()

def start_level():
    level_list[current_level][1].start()





if __name__ == "__main__":

    pygame.init()   

    surface = pygame.display.set_mode((800, 600))
    
    mytheme = pygame_menu.themes.Theme( # transparent background
                title_background_color=(255, 187, 68),
                title_font_color=(255,255,255),
                widget_font_color=(0,0,0),
                background_color=pygame_menu.baseimage.BaseImage("assets/images/Oreng.jpg"), 
                widget_selection_effect = pygame_menu.widgets.NoneSelection(),
                title_bar_style= pygame_menu.widgets.MENUBAR_STYLE_NONE,
                title_offset= (120,20),
                title_font_shadow=True,
                title_font=pygame.font.Font("assets/font/Cultural.ttf",80),
                title_floating=True,
                )
    

    menu = pygame_menu.Menu('Guitar Champions', 800, 600,theme=mytheme)
    
    fonter=pygame.font.Font("assets/font/Signatra.ttf",40)
    
    #array that stores widgets
    
    widgets=[]


    
    
    #all widgets, must have an update function, be moved into position, and added to the array
    
    
    levbutt=menu.add.selector('Level Select:', [(level[0], index) for index, level in enumerate(level_list)],float=True, font_name=fonter, onchange=select_level)
    levbutt.add_draw_callback(draw_update_function_helper.draw_update_function)
    levbutt.translate(0,-130)
    widgets.append(levbutt)
    
    playbutt=menu.add.button('Play', start_level, float=True,font_name=fonter)
    playbutt.add_draw_callback(draw_update_function_helper.draw_update_function)
    playbutt.translate(0,-40)
    widgets.append(playbutt)
    
    tutbutt=menu.add.button('Tutorial', tutorials_main.tutorials_menu, float=True,font_name=fonter)
    tutbutt.add_draw_callback(draw_update_function_helper.draw_update_function)
    tutbutt.translate(0,50)
    widgets.append(tutbutt)


    settbutt=menu.add.button('Settings', settings_menu.settings_menu, float=True,font_name=fonter)
    settbutt.add_draw_callback(draw_update_function_helper.draw_update_function)
    settbutt.translate(0,140)
    widgets.append(settbutt)
    
    quitbutt=menu.add.button('Quit', pygame_menu.events.EXIT, float=True,font_name=fonter)
    quitbutt.add_draw_callback(draw_update_function_helper.draw_update_function)
    quitbutt.translate(0,230)
    widgets.append(quitbutt)
    
    for widget in widgets:
        redraw_helper.redraw(widget, widget.get_decorator(),[255,187,68])
    
    menu.mainloop(surface)
    
