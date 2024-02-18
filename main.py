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


# Import levels
import level1
import level2



current_level = 2

def select_level(name, index):
        # Do the job here !
    current_level = 2
    print(current_level)


def start_level():
    print(current_level)
    match current_level:
        case 1:
            level1.start()

        case 2:
            level2.start()

        case _:
            level1.start()

pygame.init()

surface = pygame.display.set_mode((600, 400))

menu = pygame_menu.Menu('Guitar Champions', 400, 300,theme=pygame_menu.themes.THEME_BLUE)

menu.add.selector('Level Select:', [('One', 1), ('Two', 2)], onchange=select_level)
menu.add.button('Play', start_level)
menu.add.button('Tutorial', level1.start)
menu.add.button('Quit', pygame_menu.events.EXIT)
menu.mainloop(surface)
