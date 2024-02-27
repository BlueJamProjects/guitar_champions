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

pygame.init()

surface = pygame.display.set_mode((800, 600))

tutorials_menu = pygame_menu.Menu('Tutorials', 800, 600,theme=pygame_menu.themes.THEME_ORANGE)
tutorials_menu.add.button('Back', pygame_menu.events.BACK)
tutorials_menu.add.button('Quit', pygame_menu.events.EXIT)