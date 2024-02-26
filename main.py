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
import levels.level1 as level1
import levels.level2 as level2
import tutorials.tutorials_main as tutorials_main






current_level = 0

level_list = [("Mario", level1), ("Mountains", level2)]



def select_level(name, index):
    # This updates current level to the index of the selected level
    global current_level
    current_level = index




def start_level():
    # This 
    level_list[current_level][1].start()



if __name__ == "__main__":

    pygame.init()

    surface = pygame.display.set_mode((800, 600))

    menu = pygame_menu.Menu('Guitar Champions', 800, 600,theme=pygame_menu.themes.THEME_BLUE)

    

    menu.add.selector('Level Select:', [(level[0], index) for index, level in enumerate(level_list)], onchange=select_level)
    menu.add.button('Play', start_level)
    menu.add.button('Tutorial', tutorials_main.tutorials_menu)
    menu.add.button('Quit', pygame_menu.events.EXIT)


    menu.mainloop(surface)



