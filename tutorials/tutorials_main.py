"""
This file sets up the menu for selecting tutorial modules after the user presses "Tutorials" from the main menu.
"""

import pygame

import random

import pygame_menu

import helpers.redraw_helper as redraw_helper
import helpers.draw_update_function_helper as draw_update_function_helper

import tutorials.tut_level_controls as tut_level_controls
import tutorials.tut_guitar_holding as tut_guitar_holding
import tutorials.tut_level_playing_notes as tut_level_playing_notes

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

pressed_playing_notes = False


def playing_notes_function():
    """
    Toggle the state of playing notes and start or stop the tutorial level accordingly.

    This function checks the global boolean flag `pressed_playing_notes`. If the flag is False, it sets the flag
    to True and starts the tutorial level for playing notes. If the flag is already True, it sets the flag to False,
    effectively stopping the tutorial level. This function is typically used to control the start and stop actions
    of a tutorial level in a music-related application.
    """
    global pressed_playing_notes
    if pressed_playing_notes == False:
        pressed_playing_notes = True
        tut_level_playing_notes.start()

    else:
        pressed_playing_notes = False




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
                title_offset= (300,40),
                title_font_shadow=True,
                title_font=pygame.font.Font("assets/font/Signatra.ttf",80),
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
controlsbutt.translate(0,-120)
widgets.append(controlsbutt)

holdGuitarbutt=tutorials_menu.add.button('How to hold a Guitar', tut_guitar_holding.start, float=True,font_name=fonter)
holdGuitarbutt.add_draw_callback(draw_update_function_helper.draw_update_function)
holdGuitarbutt.translate(0,-20)
widgets.append(holdGuitarbutt)

playingnotesbutt=tutorials_menu.add.button('Playing Notes', playing_notes_function, float=True,font_name=fonter)
playingnotesbutt.add_draw_callback(draw_update_function_helper.draw_update_function)
playingnotesbutt.translate(0,80)
widgets.append(playingnotesbutt)

backbutt=tutorials_menu.add.button('Back', pygame_menu.events.BACK, float=True,font_name=fonter)
backbutt.add_draw_callback(draw_update_function_helper.draw_update_function)
backbutt.translate(0,180)
widgets.append(backbutt)
for widget in widgets:
    redraw_helper.redraw(widget,widget.get_decorator(),[255,187,68])