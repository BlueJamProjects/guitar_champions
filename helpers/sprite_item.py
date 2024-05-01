"""
This file contains the SpriteItem class
"""

import pygame

class SpriteItem(object):
    """
    Represents a sprite object along with its rendering details.

    This class simplifies the specification of a sprite's object and its rendering location.
    It is particularly useful in tutorials for managing sprites rendered on the screen.

    Args:
        sprite (pygame.Surface, optional): The surface representing the sprite. Default is a 100x100 surface.
        location (tuple, optional): The coordinates (x, y) where the sprite should be rendered. Default is (0, 0).
        is_box (bool, optional): Specifies if the sprite is a box. Default is False.
        is_background (bool, optional): Specifies if the sprite is a background. Default is False.
        box_has_border (bool, optional): Specifies if the box has a border. Default is False.
        box_color (tuple, optional): The RGB color tuple representing the box color. Default is (0, 0, 0).
        box_border (int, optional): The thickness of the box border. Default is 10.
        box_rect (pygame.Rect, optional): The dimensions and location of the box. Default is pygame.Rect(100, 100, 100, 100).
    """

    def __init__(self, 
                 sprite=pygame.Surface([100,100]), 
                 location=(0,0), 
                 is_box=False, 
                 is_background=False,
                 box_has_border= False, 
                 box_color=(0,0,0),
                 box_border=10,
                 box_rect=pygame.Rect(100,100,100,100)
                 ):
        # These two are used if this is not a box

        # the render item
        self.sprite = sprite
        # the location on screen where it should be rendered
        self.location = location

        # Set true if this is a background sprite
        self.is_background = is_background
        # These 4 are used if this is a box
        
        # Set to true if, this is a box
        self.is_box = is_box
        # controls whether the box has a border
        self.box_has_border = box_has_border
        # controls the color of the box
        self.box_color = box_color
        # controls the dimensions and location of the box
        self.box_rect = box_rect
        # controls the thickness of the border of the box
        self.box_border = box_border