# Import the pygame module
import pygame

# Import random for random numbers
import random


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



def start():

    # Define constants for the screen width and height
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600


    current_tutorial = 0

    def select_tutorial(name, index):
        # Do the job here !
        current_tutorial = index
        print(current_tutorial)


    def start_tutorial():
        match current_tutorial:
            case 1:
                # level1.start()
                pass

            case 2:
                # level2.start()
                pass

            case _:
                # level1.start()
                pass



    surface = pygame.display.set_mode((800, 600))

    menu = pygame_menu.Menu('Guitar Champions', 800, 600,theme=pygame_menu.themes.THEME_BLUE)

    menu.add.selector('Tutorial Select:', [('How the game works', 1), ('How to hold a guitar', 2),('How to hold a guitar', 3)], onchange=select_tutorial)
    menu.add.button('Start', start_tutorial)
    # menu.add.button('Tutorial', print_level)
    # menu.add.button('Quit', main)
    menu.mainloop(surface)