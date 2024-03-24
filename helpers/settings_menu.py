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
import helpers.settings_helper as settings_helper

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


user_settings = settings_helper.get_settings()

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

# pygame.init()

surface = pygame.display.set_mode((800, 600))

fonter=pygame.font.Font("assets/font/Signatra.ttf",40)

widgets=[]

settings_menu = pygame_menu.Menu('Settings', 800, 600,theme=mytheme)


if user_settings.enable_metronome == False:
    default_metronome_value = 0
elif user_settings.enable_metronome == True:
    default_metronome_value = 1
else:
    default_metronome_value = 1

enable_metronome_options = [
             ('False', False),
             ("True", True)
             ]

    # Create selector with 3 difficulty options
metronome_butt = settings_menu.add.selector(
        'Enable Metronome:\t',
        enable_metronome_options,
        selector_id='difficulty',
        default= default_metronome_value,
        onchange=settings_helper.update_enable_metronome
    )

metronome_butt.add_draw_callback(draw_update_function_helper.draw_update_function)
metronome_butt.translate(0,-90)

volume_slider = settings_menu.add.range_slider('Volume', user_settings.volume, (0, 100), 1,
                                             rangeslider_id='range_slider',
                                             value_format=lambda x: str(int(x)),
                                             onchange=settings_helper.update_volume
                                             )



volume_slider.add_draw_callback(draw_update_function_helper.draw_update_function)

volume_slider.translate(0,-120)

backbutt=settings_menu.add.button('Back', pygame_menu.events.BACK, float=True,font_name=fonter)
backbutt.add_draw_callback(draw_update_function_helper.draw_update_function)
backbutt.translate(0,-20)
widgets.append(backbutt)
exbutt=settings_menu.add.button('Quit', pygame_menu.events.EXIT, float=True,font_name=fonter)
exbutt.add_draw_callback(draw_update_function_helper.draw_update_function)
exbutt.translate(0,90)
widgets.append(exbutt)
for widget in widgets:
    redraw_helper.redraw(widget,widget.get_decorator(),[255,187,68])