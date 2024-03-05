# import pygame asprite package, download by typing "pip3 install pygame_aseprite_animation" into your terminal
from pygame_aseprite_animation import *
# Import the pygame module
import os, pygame

# Import random for random numbers
import random

# Import math for oscillation
import math

# Import the menu library to more easily make menu selction
import pygame_menu

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


# Import levels
import levels.level1 as level1
import levels.level2 as level2
import tutorials.tutorials_main as tutorials_main

# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


# Setup for sounds, defaults are good
pygame.mixer.init()

# Initialize pygame
pygame.init()

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))





current_level = 0

level_list = [("Mario", level1), ("Mountains", level2)]


def select_level(name, index):
    # This updates current level to the index of the selected level
    global current_level
    current_level = index

    # Flip everything to the display
    pygame.display.flip()

def redraw(widget, decos,color):
    decos.add_rect(-widget.get_width()/2,-widget.get_height()/2+1,pygame.Rect(0,0 , widget.get_width(),widget.get_height()),color)
    decos.add_line((-widget.get_width()/2,-widget.get_height()/2+1),(widget.get_width()/2,-widget.get_height()/2+1),[255,255,255],2)
    decos.add_line((-widget.get_width()/2,-widget.get_height()/2+1),(-widget.get_width()/2,widget.get_height()/2+1),[255,255,255],2)
    decos.add_line((widget.get_width()/2,-widget.get_height()/2+1),(widget.get_width()/2,widget.get_height()/2+1),[255,255,255],2)
    decos.add_line((-widget.get_width()/2,widget.get_height()/2+1),(widget.get_width()/2,widget.get_height()/2+1),[255,255,255],2)
    decos.add_circle(-widget.get_width()/2,-widget.get_height()/2+1,10,color,True)
    decos.add_circle(widget.get_width()/2,-widget.get_height()/2+1,10,color,True)
    decos.add_circle(-widget.get_width()/2,widget.get_height()/2+1,10,color,True)
    decos.add_circle(widget.get_width()/2,widget.get_height()/2+1,10,color,True)
    decos.add_circle(-widget.get_width()/2,-widget.get_height()/2+1,10,[255,255,255],False,2)
    decos.add_circle(widget.get_width()/2,-widget.get_height()/2+1,10,[255,255,255],False,2)
    decos.add_circle(-widget.get_width()/2,widget.get_height()/2+1,10,[255,255,255],False,2)
    decos.add_circle(widget.get_width()/2,widget.get_height()/2+1,10,[255,255,255],False,2)
        

def start_level():
    # This 
    level_list[current_level][1].start()



if __name__ == "__main__":

    pygame.init()   

    surface = pygame.display.set_mode((800, 600))
    mytheme = pygame_menu.themes.Theme( # transparent background
                title_background_color=(255, 187, 68),
                title_font_color=(255,255,255),
                widget_font_color=(0,0,0),
                background_color=pygame_menu.baseimage.BaseImage("Oreng.jpg"), 
                widget_selection_effect = pygame_menu.widgets.NoneSelection(),
                title_bar_style= pygame_menu.widgets.MENUBAR_STYLE_NONE,
                title_offset= (120,20),
                title_font_shadow=True,
                title_font='script',
                title_font_size=80,
                title_floating=True,
                )
    

    menu = pygame_menu.Menu('Guitar Champions', 800, 600,theme=mytheme)
    def draw_update_function(widget, menu):
        color=[0,0,0]
        widget.set_margin(0,50)
        if (widget.is_selected()):
            color=[239,159,20]
            widget.set_font_shadow(True,(0,0,0),None,1)
            widget.shadow(shadow_type='rectangular', shadow_width=20, corner_radius=0, color=(0, 0, 0), aa_amount=4)
            widget.set_padding(3*(abs(pygame.time.get_ticks() % 2000-1000)/500))
            style={
                "color": (255,255,255),
                "antialias": True
            }
        else:
            widget.set_font_shadow(False,(0,0,0),None,1)
            color=[255,187,68]
            widget.shadow(shadow_type='rectangular', shadow_width=0, corner_radius=0, color=(0, 0, 0), aa_amount=4)
            widget.set_padding(4)
            style={
                "color": (0,0,0),
                "antialias": True
            }
        widget.get_decorator().remove_all()
        redraw(widget,widget.get_decorator(),color)
        widget.update_font(style)
        
    #array that stores widgets
    widgets=[]
    
    #all widgets, must have an update function, be moved into position, and added to the array
    levbutt=menu.add.selector('Level Select:', [(level[0], index) for index, level in enumerate(level_list)],float=True, font_name='script', onchange=select_level)
    levbutt.add_draw_callback(draw_update_function)
    levbutt.translate(0,-120)
    widgets.append(levbutt)
    
    playbutt=menu.add.button('Play', start_level, float=True,font_name='script')
    playbutt.add_draw_callback(draw_update_function)
    playbutt.translate(0,-20)
    widgets.append(playbutt)
    
    tutbutt=menu.add.button('Tutorial', tutorials_main.tutorials_menu, float=True,font_name='script')
    tutbutt.add_draw_callback(draw_update_function)
    tutbutt.translate(0,90)
    widgets.append(tutbutt)
    
    quitbutt=menu.add.button('Quit', pygame_menu.events.EXIT, float=True,font_name='script')
    quitbutt.add_draw_callback(draw_update_function)
    quitbutt.translate(0,200)
    widgets.append(quitbutt)
    
    for widget in widgets:
        redraw(widget, widget.get_decorator(),[255,187,68])
    
    menu.mainloop(surface)
    
