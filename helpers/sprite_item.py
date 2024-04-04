import pygame

class SpriteItem(object):
    """
    A class to make specifying a sprite's object and it's location easier
    Used in the tutorials for the sprites that are rendered on the screen
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